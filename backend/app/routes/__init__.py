from fastapi import APIRouter
from .base import router as base_router
from .programs import router as programs_router

router = APIRouter()

router.include_router(base_router)
router.include_router(programs_router)