from app.types.api_response import ApiResponse
from app.models import Operator
from app.types.operator_requests import UpsetOperator
from app.types.operator_filters import OperatorFilter
from app import filters

from fastapi import APIRouter, Depends


router = APIRouter(prefix="/operator", tags=["User Operator"])


@router.post("", response_model=ApiResponse)
async def create_operator(params: UpsetOperator):
    params.type = params.type.value
    param = dict(params).copy()
    status = False
    message = None
    data = None
    try:
        data_source = await Operator.create(**param)
        data = data_source.__dict__
        status = True
    except TimeoutError:
        message = "Time Out Error !!!"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.patch("/{pk}", response_model=ApiResponse)
async def update_operator(pk: int, params: UpsetOperator):
    params.type = params.type.value
    param = dict(params).copy()
    status = False
    message = None
    data = None
    try:
        await Operator.filter(id=pk).update(**param)
        data = await Operator.get(id=pk).values()
        status = True
    except TimeoutError:
        message = "Time out error"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.delete("/{pk}", response_model=ApiResponse)
async def delete_operator(pk: int):
    status = False
    message = None
    data = None
    try:
        is_monitor = await Operator.filter(id=pk).exists()
        if not is_monitor:
            return ApiResponse(
                status=status, message="Operator Not Found !!!", data=data
            )
        await Operator.filter(id=pk).delete()
        status = True
    except TimeoutError:
        message = "Time out error"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.get("", response_model=ApiResponse)
async def get_operators(
    params: OperatorFilter = Depends(), page: int = 1, size: int = 10
):
    status = False
    message = None
    data = None
    try:
        offset = size * (page - 1)
        data = (
            await Operator.filter(filters(params)).offset(offset).limit(size).values()
        )
        status = True
    except TimeoutError:
        message = "Time Out Error !!!"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)
