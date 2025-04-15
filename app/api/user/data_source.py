from app.types.data_source_requests import UpsetDataSource
from app.types.api_response import ApiResponse
from app.models import DataSource
from app.types.data_source_filters import DataSourceFilter
from app.types.data_source_types import (
    MysqlDataSource,
    ElasticsearchDataSource,
    RestDataSource,
)
from app import filters, convert_type_of_models

from fastapi import APIRouter, Depends


router = APIRouter(prefix="/data_source", tags=["User Data Source"])


@router.post("", response_model=ApiResponse)
async def create_data_source(params: UpsetDataSource):
    params.type = params.type.value
    context = {}
    param = dict(params)
    param = {k: v for k, v in param.items() if v is not None and v != ""}
    status = False
    message = None
    data = None
    try:
        context.update({
            "name": params.name,
            "type": params.type
        })
        param.pop("name")
        param.pop("type")
        args = {}
        for p in param:
            args.update({p: param[p]})
        context.update({
            "args": args
        })
        data_source = await DataSource.create(**context)
        data = data_source.__dict__
        status = True
    except TimeoutError:
        message = "Time Out Error !!!"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.patch("/{pk}", response_model=ApiResponse)
async def update_data_source(pk: int, params: UpsetDataSource):
    params.type = params.type.value
    context = {}
    param = dict(params)
    param = {k: v for k, v in param.items() if v is not None and v != ""}
    status = False
    message = None
    data = None
    try:
        context.update({
            "name": params.name,
            "type": params.type
        })
        param.pop("name")
        param.pop("type")
        args = {}
        for p in param:
            args.update({p: param[p]})
        context.update({
            "args": args
        })
        await DataSource.filter(id=pk).update(**context)
        data = await DataSource.get(id=pk).values()
        status = True
    except TimeoutError:
        message = "Time out error"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.delete("/{pk}", response_model=ApiResponse)
async def delete_data_source(pk: int):
    status = False
    message = None
    data = None
    try:
        is_monitor = await DataSource.filter(id=pk).exists()
        if not is_monitor:
            return ApiResponse(
                status=status, message="Data Source Not Found !!!", data=data
            )
        await DataSource.filter(id=pk).delete()
        status = True
    except TimeoutError:
        message = "Time out error"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.get("", response_model=ApiResponse)
async def get_data_sources(
    params: DataSourceFilter = Depends(), page: int = 1, size: int = 10
):
    status = False
    message = None
    data = None
    try:
        offset = size * (page - 1)
        data = (
            await DataSource.filter(filters(params)).offset(offset).limit(size).values()
        )
        status = True
    except TimeoutError:
        message = "Time Out Error !!!"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.get("/types", response_model=ApiResponse)
async def get_data_source_type():
    status = False
    message = None
    data = []
    try:
        base_models = [MysqlDataSource, ElasticsearchDataSource, RestDataSource]
        # print(RestDataSource.__fields__["type"].annotation.__dict__)
        for model in base_models:
            context = {}
            fields = model.__fields__
            context.update({"type": model.Config.title, "fields": []})
            for field in fields:
                default = str(fields[field].default)
                model_type = fields[field].annotation
                value_type = convert_type_of_models(str(model_type))
                context_field = {
                    "name": field,
                    "type": value_type,
                    "required": bool(fields[field].is_required()),
                    "placeholder": field,
                    "default": ("None" if default == "PydanticUndefined" else default),
                }
                if "enum" == value_type:
                    context_field.update(
                        {"items": model_type.__dict__["_member_names_"]}
                    )
                context["fields"].append(context_field)
            data.append(context)
        status = True
    except TimeoutError:
        message = "Time Out Error !!!"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)
