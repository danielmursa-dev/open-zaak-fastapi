from fastapi import APIRouter
from src.api.components.zaken.router import zaken_router

api_router = APIRouter()
api_router.include_router(zaken_router)
