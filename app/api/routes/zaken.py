from typing import Any

from fastapi import APIRouter

from app.api.deps import SessionDep

router = APIRouter(prefix="/zaken/api/v1", tags=["items"])


@router.get("/zaken")
def read_items(session: SessionDep) -> Any:
    return ["test"]
