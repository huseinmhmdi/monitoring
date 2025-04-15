from app.types.api_response import ApiResponse
from app.types.test_query_requests import TestQueryRequest
from app.types.test_exec_requests import TestExecRequest, TestProjectRequest
from app.data_source.mysql import Mysql
from app.data_source.rest import Rest
from app.data_source.elasticsearch import Elasticsearch
from app import send_data_source_param
from app.models import DataSource, MontitorResult, Project
from app import get_path_dict, condition_convert_to_dict

import datetime
from datetime import timezone

from fastapi import APIRouter
from jinja2 import Template


router = APIRouter(prefix="/test", tags=["User Test"])


DATA_SOURCE = {
    "mysql": Mysql,
    "rest": Rest,
    "elasticsearch": Elasticsearch,
}


@router.post("/query", response_model=ApiResponse)
async def test_query(params: TestQueryRequest):
    status = False
    message = None
    data = None
    try:
        data_source = await DataSource.get(id=params.data_source_id)
        param = send_data_source_param(data_source)
        conn = DATA_SOURCE[data_source.type.value](param)
        conn.connect()
        data = conn.execute(params.query)
        conn.disconnect()
        status = True
    except TimeoutError:
        message = "Time Out Error"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.post("/exec/{monitor_id}", response_model=ApiResponse)
async def test_exec(monitor_id: int, params: TestExecRequest):
    status = False
    message = None
    data = None
    try:
        now = datetime.datetime.now(tz=timezone.utc)
        convert_time = now - datetime.timedelta(seconds=params.duration)
        monitor_result_data = await MontitorResult.filter(
            monitor_id=monitor_id, created_at__gt=convert_time
        ).values_list("data", flat=True)
        path_dict = await get_path_dict(params.condition)
        count = 0
        for data in monitor_result_data:
            tpl = Template("{{" + path_dict + "}}")
            count += int(tpl.render(data=data))
        condition_dict = await condition_convert_to_dict(params.condition, count)
        data = condition_dict
        condition = params.condition.replace("$", "")
        tpl = Template("{{" + condition + "}}")
        is_passed = eval(tpl.render(data=data))
        data = {"is_passed": is_passed, "count": count}
        status = True
    except TimeoutError:
        message = "Time Out Error"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.post("/project/{project_id}", response_model=ApiResponse)
async def test_by_project(project_id: int, params: TestProjectRequest):
    status = False
    message = None
    data = None
    try:
        condition_text = f"{params.count} < $data.count"
        now = datetime.datetime.now(tz=timezone.utc)
        convert_time = now - datetime.timedelta(seconds=params.duration)
        monitor_result_data = await MontitorResult.filter(
            monitor__project_id=project_id, created_at__gt=convert_time
        ).values_list("data", flat=True)
        path_dict = await get_path_dict(condition_text)
        count = 0
        for data in monitor_result_data:
            tpl = Template("{{" + path_dict + "}}")
            count += int(tpl.render(data=data))
        condition_dict = await condition_convert_to_dict(condition_text, count)
        data = condition_dict
        condition = condition_text.replace("$", "")
        tpl = Template("{{" + condition + "}}")
        is_passed = eval(tpl.render(data=data))
        project = await Project.get(id=project_id).values()
        project_name = project["name"]
        data = {"is_passed": is_passed, "count": count, "project_name": project_name}
        status = True
    except TimeoutError:
        message = "Time Out Error"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)
