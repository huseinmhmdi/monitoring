from app.types.api_response import ApiResponse
from app.types.project_request import CreateProjectRequest
from app.types.project_filter import ProjectFilter
from app.models import Project
from app import filters

from fastapi import APIRouter, Depends


router = APIRouter(prefix="/project", tags=["User Project"])


@router.post("", response_model=ApiResponse)
async def create_project(params: CreateProjectRequest):
    status = False
    data = None
    message = None
    param = dict(params).copy()
    try:
        project = await Project.create(**param)
        data = project.__dict__
        status = True
    except TimeoutError:
        message = "Time out error !!!"
    except Exception as e:
        message = "Not Found: " + e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.patch("/{pk}", response_model=ApiResponse)
async def update_project(params: CreateProjectRequest, pk: int):
    message = None
    status = False
    data = None
    param = dict(params).copy()
    try:
        is_project = await Project.filter(id=pk).exists()
        if not is_project:
            return ApiResponse(
                status=status, message="Project Not Found !!!", data=data
            )
        await Project.filter(id=pk).update(**param)
        data = await Project.get(id=pk).values()
        status = True
    except Exception as e:
        message = "Not Found: " + e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.delete("/{pk}", response_model=ApiResponse)
async def delete_project(pk: int):
    status = False
    message = None
    data = None
    try:
        await Project.filter(id=pk).delete()
        status = True
    except TimeoutError:
        message = "Time Out Error !!!"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)


@router.get("", response_model=ApiResponse)
async def get_projects(
    params: ProjectFilter = Depends(), page: int = 1, size: int = 10
):
    status = False
    message = None
    data = None
    try:
        offset = size * (page - 1)
        data = await Project.filter(filters(params)).offset(offset).limit(size).values()
        status = True
    except TimeoutError:
        message = "Time Out Error !!!"
    except Exception as e:
        message = e.__str__()
    return ApiResponse(status=status, message=message, data=data)
