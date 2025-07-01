from fastapi import APIRouter

from src.api.components.zaken.router import zaken_router
from src.api.components.catalogi.router import catalogi_router

api_router = APIRouter()
api_router.include_router(router=zaken_router, prefix="/zaken/api/v1", tags=["zaken"])
api_router.include_router(
    router=catalogi_router, prefix="/catalogi/api/v1", tags=["zaken"]
)
