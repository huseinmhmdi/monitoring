from app.api.user import router as user_router
from app.api.admin import router as admin_router

from fastapi import APIRouter


router = APIRouter()

router.include_router(user_router)
router.include_router(admin_router)
