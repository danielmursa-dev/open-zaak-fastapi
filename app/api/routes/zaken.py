from typing import Any
from app.api.models import Zaak
from sqlmodel import select
from fastapi import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from app.api.deps import SessionDep

router = APIRouter(prefix="/zaken/api/v1", tags=["zaken"])


@router.get("/zaken", response_model=Page[Zaak])
async def read_items(session: SessionDep) -> Any:
    statement = select(Zaak)
    return await paginate(session, statement)
