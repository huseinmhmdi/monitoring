from tortoise.expressions import Q
from dataclasses import dataclass

from app.types.data_source_types import (
    MysqlDataSource,
    RestDataSource,
    ElasticsearchDataSource,
)
from app.models import DataSource


# Filter Set config


@dataclass
class TupleVal:
    KEY: int = 0
    VALUE: int = 1


def filters(params) -> Q:
    q = Q()
    for param in params:
        if param[TupleVal.VALUE]:
            context = {param[TupleVal.KEY]: param[TupleVal.VALUE]}
            q = q & Q(**context)
    return q


# Test Api Config


async def get_path_dict(condition: str):
    path_dict = None
    value = condition.split(" ")
    for val in value:
        if val.startswith("$"):
            path_dict = val[1:]
            break
    if path_dict is None:
        raise Exception("path dict Not valid !!!")

    return path_dict


async def condition_convert_to_dict(condition: str, monitor_result_count: str):
    path_dict = await get_path_dict(condition)
    keys = path_dict.split(".")
    nested_dict = {}
    current_level = nested_dict

    for key in keys[:-1]:
        current_level[key] = {}
        current_level = current_level[key]

    current_level[keys[-1]] = int(monitor_result_count)
    return nested_dict["data"]


def convert_type_of_models(types: str):
    types = types.lower()
    value_type = None
    if "list" in types:
        value_type = "list"
    elif "dict" in types:
        value_type = "dict"
    elif "str" in types:
        value_type = "str"
    elif "enum" in types:
        value_type = "enum"
    elif "int" in types:
        value_type = "int"
    elif "bool" in types:
        value_type = "bool"
    elif "float" in types:
        value_type = "float"
    return value_type


def send_data_source_param(source: DataSource):
    match source.type.value:
        case "mysql":
            param = MysqlDataSource(**source.args)
        case "rest":
            param = RestDataSource(**source.args)
        case "elasticsearch":
            param = ElasticsearchDataSource(**source.args)
        case _:
            raise Exception("type not valid !!!")
    return param
