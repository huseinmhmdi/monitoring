from app.types.alert_requests import CreateAlert, UpdateAlert
from app.types.alert_filters import AlertFilter, AlertResultFilter
from app.types.api_response import ApiResponse
from app.models import Monitor, Operator, Alert, AlertResult
from app import filters

from fastapi import APIRouter, Depends


router = APIRouter(prefix="/alert", tags=["User Alert"])


@router.post("", response_model=ApiResponse)
async def create_alert(params: CreateAlert):
    print(params)
    param = dict(params).copy()
    status = False
    message = None
    data = None
    try:
        is_monitor = await Monitor.filter(id=params.monitor_id).exists()
        if not is_monitor:
            return ApiResponse(
                status=status, message="Monitor Not Found !!!", data=data
            )
        is_operator = await Operator.filter(id=params.operator_id).exists()
        if not is_operator:
            return ApiResponse(
                status=status, message="Operator Not Found !!!", data=data
            )
        is_alert = await Alert.filter(
            monitor_id=params.monitor_id, level=params.level
        ).exists()
        if is_alert:
            return ApiResponse(
                status=status,
                message="This Alert with this level and monitor Exists",
                data=data,
            )
        alert = await Alert.create(**param)
        data = alert.__dict__
        status = True
    except TimeoutError:
        message = "Time Out Error !!!"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.patch("/{pk}", response_model=ApiResponse)
async def update_alert(pk: int, params: UpdateAlert):
    param = dict(params)
    param = {k: v for k, v in param.items() if v is not None and v != ""}
    print(param)
    status = False
    message = None
    data = None
    try:
        if params.monitor_id:
            is_monitor = await Monitor.filter(id=params.monitor_id).exists()
            if not is_monitor:
                return ApiResponse(
                    status=status, message="Monitor Not Found !!!", data=data
                )
        if params.operator_id:
            is_operator = await Operator.filter(id=params.operator_id).exists()
            if not is_operator:
                return ApiResponse(
                    status=status, message="Operator Not Found !!!", data=data
                )
        await Alert.filter(id=pk).update(**param)
        data = await Alert.get(id=pk).values()
        status = True
    except TimeoutError:
        message = "Time Out Error !!!"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.delete("/{pk}", response_model=ApiResponse)
async def delete_alert(pk: int):
    status = False
    message = None
    data = None
    try:
        await Alert.filter(id=pk).delete()
        status = True
    except TimeoutError:
        message = "Time Out Error !!!"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.get("", response_model=ApiResponse)
async def get_alerts(params: AlertFilter = Depends(), page: int = 1, size: int = 10):
    status = False
    message = None
    data = None
    try:
        offset = size * (page - 1)
        data = await Alert.filter(filters(params)).offset(offset).limit(size).values()
        status = True
    except TimeoutError:
        message = "Time Out Error !!!"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.get("/result", response_model=ApiResponse)
async def get_alert_result(
    params: AlertResultFilter = Depends(), page: int = 1, size: int = 10
):
    status = False
    message = None
    data = None
    try:
        offset = size * (page - 1)
        data = (
            await AlertResult.filter(filters(params))
            .offset(offset)
            .limit(size)
            .values()
        )
        status = True
    except TimeoutError:
        message = "Time Out Error !!!"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)
