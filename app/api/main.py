from fastapi import APIRouter
from app.api.routes import zaken

api_router = APIRouter()
api_router.include_router(zaken.router)
