from app.api.user.alert import router as alert_router
from app.api.user.data_source import router as data_source_router
from app.api.user.monitor import router as monitor_router
from app.api.user.operator import router as operator_router
from app.api.user.test import router as test_router
from app.api.user.project import router as project_router

from fastapi import APIRouter


router = APIRouter(prefix="/user")


# Version 1
router.include_router(alert_router, prefix='/v1')
router.include_router(data_source_router, prefix='/v1')
router.include_router(monitor_router, prefix='/v1')
router.include_router(operator_router, prefix='/v1')
router.include_router(test_router, prefix='/v1')
router.include_router(project_router, prefix='/v1')
