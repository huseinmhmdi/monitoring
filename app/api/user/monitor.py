from app.types.api_response import ApiResponse
from app.types.monitor_requests import UpsertMonitor, UpdateDurationRequest, MonitorResultCreate
from app.types.monitor_filters import MonitorFilter
from app.models import Monitor, Alert, Project, MontitorResult
from app import filters

from fastapi import APIRouter, Depends


router = APIRouter(prefix="/monitor", tags=["User Monitor"])


@router.post("", response_model=ApiResponse)
async def create_monitor(params: UpsertMonitor):
    param = dict(params).copy()
    status = False
    message = None
    data = None
    try:
        is_project = await Project.filter(id=params.project_id).exists()
        if not is_project:
            return ApiResponse(
                status=status, message="Project Not Found !!!", data=data
            )
        is_monitor = await Monitor.filter(project_id=params.project_id).exists()
        if is_monitor:
            return ApiResponse(
                status=status,
                message="This Monitor with this Project exists !!!",
                data=data,
            )
        monitor = await Monitor.create(**param)
        data = monitor.__dict__
        status = True
    except TimeoutError:
        message = "Time out error"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.patch("/{pk}", response_model=ApiResponse)
async def update_monitor(pk: int, params: UpsertMonitor):
    param = dict(params).copy()
    status = False
    message = None
    data = None
    try:
        is_project = await Project.filter(id=params.project_id).exists()
        if not is_project:
            return ApiResponse(
                status=status, message="Project Not Found !!!", data=data
            )
        await Monitor.filter(id=pk).update(**param)
        data = await Monitor.get(id=pk).values()
        status = True
    except TimeoutError:
        message = "Time out error"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.delete("/{pk}", response_model=ApiResponse)
async def delete_monitor(pk: int):
    status = False
    message = None
    data = None
    try:
        is_monitor = await Monitor.filter(id=pk).exists()
        if not is_monitor:
            return ApiResponse(
                status=status, message="Monitor Not Found !!!", data=data
            )
        await Monitor.filter(id=pk).delete()
        status = True
    except TimeoutError:
        message = "Time out error"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.get("", response_model=ApiResponse)
async def get_monitors(
    params: MonitorFilter = Depends(), page: int = 1, size: int = 100
):
    status = False
    message = None
    data = None
    try:
        offset = size * (page - 1)
        data = await Monitor.filter(filters(params)).offset(offset).limit(size).values()
        status = True
    except TimeoutError:
        message = "Time out error"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.get("/{pk}/metric", response_model=ApiResponse)
async def get_monitor_result_metric():
    pass


@router.patch("/{monitor_id}/duration", response_model=ApiResponse)
async def update_duration_monitor(monitor_id: int, params: UpdateDurationRequest):
    status = False
    message = None
    data = None
    try:
        await Alert.filter(monitor_id=monitor_id, level=params.level).update(
            duration=params.duration
        )
        status = True
    except TimeoutError:
        message = "Time out error"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.post("/result", response_model=ApiResponse)
async def create_monitor_result(params: MonitorResultCreate):
    data = None
    status = False
    message = None
    param = dict(params).copy()
    try:
        is_monitor = await Monitor.filter(id=params.monitor_id).exists()
        if not is_monitor:
            return ApiResponse(
                status=status, message="Monitor Not Found !!!", data=data
            )
        monitor = await MontitorResult.create(**param)
        data = monitor.__dict__
        status = True
    except TimeoutError:
        message = "Time out error"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)
