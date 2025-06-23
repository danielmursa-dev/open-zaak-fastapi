from typing import Any
from src.api.components.zaken.models import Zaak
from sqlmodel import select
from fastapi import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from src.core.deps import SessionDep
from src.api.components.zaken.schemas import ZaakSerializer

zaken_router = APIRouter(prefix="/zaken/api/v1", tags=["zaken"])


@zaken_router.get("/zaken", response_model=Page[ZaakSerializer])
async def read_items(session: SessionDep) -> Any:
    statement = select(Zaak)
    return await paginate(session, statement)
