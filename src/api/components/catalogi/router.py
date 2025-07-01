from typing import Any

from fastapi import APIRouter

from src.core.deps import SessionDep

catalogi_router = APIRouter()


@catalogi_router.get("/zaaktypen/{uuid}", name="zaaktype-detail")
async def detail_zaaktype(uuid: str, session: SessionDep) -> Any:
    return []
