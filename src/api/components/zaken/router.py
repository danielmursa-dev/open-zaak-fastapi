from typing import Any

from fastapi import APIRouter
from fastapi_pagination.ext.sqlmodel import paginate
from sqlalchemy import desc
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select

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
    statement = (
        select(Zaak)
        .options(
            joinedload(Zaak.zaak_identificatie),
            joinedload(Zaak.zaaktype),
            selectinload(Zaak.kenmerken),
            selectinload(Zaak.rollen).load_only(Rol.uuid),
            selectinload(Zaak.eigenschappen).selectinload(ZaakEigenschap.zaak),
            selectinload(Zaak.status).load_only(Status.uuid),
            selectinload(Zaak.relevante_andere_zaken),
            selectinload(Zaak.zaakinformatieobjecten).load_only(
                ZaakInformatieObject.uuid
            ),
            selectinload(Zaak.zaakobjecten).load_only(ZaakObject.uuid),
            selectinload(Zaak.resultaat).load_only(Resultaat.uuid),
            selectinload(Zaak.hoofdzaak).load_only(Zaak.uuid),
            selectinload(Zaak.deelzaken).load_only(Zaak.uuid),
        )
        .order_by(desc(Zaak.identificatie_ptr_id))
        # .where(Zaak.uuid == "fdc97bac-4ec0-44df-bb7e-efaff23da325")
    )
    return await paginate(session, statement)


@zaken_router.get("/zaken/{uuid}", name="zaak-detail")
async def detail_zaken(uuid: str, session: SessionDep) -> Any:
    return []


@zaken_router.get("/rollen/{uuid}", name="rol-detail")
async def detail_rol(uuid: str, session: SessionDep) -> Any:
    return []


@zaken_router.get(
    "/zaken/{zaak_uuid}/zaakeigenschappen/{uuid}", name="eigenschappen-detail"
)
async def detail_eigenschappen(zaak_uuid: str, uuid: str, session: SessionDep) -> Any:
    return []


@zaken_router.get("/resultaten/{uuid}", name="resultaattypen-detail")
async def detail_resultaattypen(uuid: str, session: SessionDep) -> Any:
    return []


@zaken_router.get("/informatieobjecttypen/{uuid}", name="zaakinformatieobject-detail")
async def detail_informatieobjecttypen(uuid: str, session: SessionDep) -> Any:
    return []


@zaken_router.get("/zaakobjecten/{uuid}", name="zaakobjecttypen-detail")
async def detail_zaakobjecttypen(uuid: str, session: SessionDep) -> Any:
    return []


@zaken_router.get("/statussen/{uuid}", name="statustypen-detail")
async def detail_statustypen(uuid: str, session: SessionDep) -> Any:
    return []
