from typing import Any, List

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

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
from src.core.database import get_session
from src.core.pagination import Page as CustomPage


zaken_router = APIRouter()

# import logging

# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

QUERY = (
    select(Zaak)
    .options(
        joinedload(Zaak.zaak_identificatie),
        selectinload(Zaak.zaaktype),
        selectinload(Zaak.kenmerken),
        selectinload(Zaak.rollen).load_only(Rol.uuid),
        selectinload(Zaak.eigenschappen).selectinload(ZaakEigenschap.zaak),
        selectinload(Zaak.status).load_only(Status.uuid),
        selectinload(Zaak.relevante_andere_zaken),
        selectinload(Zaak.zaakinformatieobjecten).load_only(ZaakInformatieObject.uuid),
        selectinload(Zaak.zaakobjecten).load_only(ZaakObject.uuid),
        selectinload(Zaak.resultaat).load_only(Resultaat.uuid),
        selectinload(Zaak.hoofdzaak).load_only(Zaak.uuid),
        selectinload(Zaak.deelzaken).load_only(Zaak.uuid),
    )
    .order_by(desc(Zaak.identificatie_ptr_id))
)


@zaken_router.get("/zaken", name="zaken-list", response_model=CustomPage[ZaakSchema])
async def list_zaken(
    session: AsyncSession = Depends(get_session),
) -> Page[ZaakSchema]:
    return await paginate(session, QUERY)


@zaken_router.get("/zaken-no-page", name="zaken-list", response_model=List[ZaakSchema])
async def list_zaken_no_page(
    session: AsyncSession = Depends(get_session),
) -> list[ZaakSchema]:
    result = await session.execute(QUERY.limit(100).offset(100))
    zaken = result.scalars().all()
    return zaken


@zaken_router.get(
    "/zaken-cursor-page", name="zaken-list", response_model=CursorPage[ZaakSchema]
)
async def list_zaken_cursor(
    params: CursorParams = Depends(),
    session: AsyncSession = Depends(get_session),
) -> CursorPage[ZaakSchema]:
    return await paginate(session, QUERY, params)


@zaken_router.get(
    "/zaken-base-page", name="zaken-list", response_model=Page[ZaakSchema]
)
async def list_zaken_base_page(
    session: AsyncSession = Depends(get_session),
) -> Page[ZaakSchema]:
    return await paginate(session, QUERY)


@zaken_router.get("/zaken/{uuid}", name="zaak-detail")
async def detail_zaken(uuid: str, session: AsyncSession = Depends(get_session)) -> Any:
    return []


@zaken_router.get("/rollen/{uuid}", name="rol-detail")
async def detail_rol(uuid: str, session: AsyncSession = Depends(get_session)) -> Any:
    return []


@zaken_router.get(
    "/zaken/{zaak_uuid}/zaakeigenschappen/{uuid}", name="eigenschappen-detail"
)
async def detail_eigenschappen(
    zaak_uuid: str, uuid: str, session: AsyncSession = Depends(get_session)
) -> Any:
    return []


@zaken_router.get("/resultaten/{uuid}", name="resultaattypen-detail")
async def detail_resultaattypen(
    uuid: str, session: AsyncSession = Depends(get_session)
) -> Any:
    return []


@zaken_router.get("/informatieobjecttypen/{uuid}", name="zaakinformatieobject-detail")
async def detail_informatieobjecttypen(
    uuid: str, session: AsyncSession = Depends(get_session)
) -> Any:
    return []


@zaken_router.get("/zaakobjecten/{uuid}", name="zaakobjecttypen-detail")
async def detail_zaakobjecttypen(
    uuid: str, session: AsyncSession = Depends(get_session)
) -> Any:
    return []


@zaken_router.get("/statussen/{uuid}", name="statustypen-detail")
async def detail_statustypen(
    uuid: str, session: AsyncSession = Depends(get_session)
) -> Any:
    return []
