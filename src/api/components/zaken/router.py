from typing import Any

from fastapi import APIRouter
from fastapi_pagination.ext.sqlmodel import paginate
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select

from src.api.components.catalogi.models.zaaktype import ZaakType
from src.api.components.zaken.models.zaken import (
    Resultaat,
    Rol,
    Status,
    Zaak,
    ZaakEigenschap,
    ZaakInformatieObject,
    ZaakObject,
)
from src.api.components.zaken.schemas import ZaakSchema
from src.core.deps import SessionDep
from src.core.pagination import Page

zaken_router = APIRouter()


@zaken_router.get("/zaken", name="zaken-list", response_model=Page[ZaakSchema])
async def list_zaken(session: SessionDep) -> Page[ZaakSchema]:
    statement = select(Zaak).options(
        selectinload(Zaak.zaak_identificatie),
        joinedload(Zaak.zaaktype).load_only(ZaakType.uuid),
        selectinload(Zaak.rollen).load_only(Rol.uuid),
        selectinload(Zaak.eigenschappen).load_only(ZaakEigenschap.uuid),
        selectinload(Zaak.status).load_only(Status.uuid),
        selectinload(Zaak.relevante_andere_zaken),
        selectinload(Zaak.zaakinformatieobjecten).load_only(ZaakInformatieObject.uuid),
        selectinload(Zaak.zaakobjecten).load_only(ZaakObject.uuid),
        joinedload(Zaak.kenmerken),
        selectinload(Zaak.resultaat).load_only(Resultaat.uuid),
    )

    return await paginate(session, statement)


@zaken_router.get("/zaken/{uuid}", name="zaak-detail")
async def detail_zaken(uuid: str, session: SessionDep) -> Any:
    return []


@zaken_router.get("/rollen/{uuid}", name="rol-detail")
async def detail_rol(uuid: str, session: SessionDep) -> Any:
    return []


@zaken_router.get("/zaaktype/{uuid}", name="zaaktype-detail")
async def detail_zaaktype(uuid: str, session: SessionDep) -> Any:
    return []


@zaken_router.get(
    "/zaakeigenschap-detail/{uuid}", name="zaakeigenschap-detail"
)  # check all url # TODO
async def detail_zaakeigenschap(uuid: str, session: SessionDep) -> Any:
    return []


@zaken_router.get(
    "/zaakinformatieobject-detail/{uuid}", name="zaakinformatieobject-detail"
)  # check all url
async def detail_zaakinformatieobject(uuid: str, session: SessionDep) -> Any:
    return []


@zaken_router.get("/resultaat-detail/{uuid}", name="resultaat-detail")  # check all url
async def detail_resultaat(uuid: str, session: SessionDep) -> Any:
    return []
