from datetime import date, datetime, timedelta
from typing import Annotated, List, Optional, Union
from uuid import UUID

from pydantic import AnyUrl, BaseModel, computed_field
from sqlalchemy import JSON
from sqlmodel import Field

from src.api.components.catalogi.models.zaaktype import ZaakType
from src.api.components.zaken.models.constants import BetalingsIndicatie
from src.api.components.zaken.models.identification import ZaakIdentificatie
from src.api.components.zaken.models.zaken import (
    Rol,
    Zaak,
    ZaakEigenschap,
    ZaakInformatieObject,
    ZaakObject,
)
from src.api.fields import (
    GeoJSONGeometry,
    HyperlinkedRelatedField,
    NestedHyperlinkedRelatedField,
)
from src.api.mixins import BaseMixin


class UUIDZaakSchema(BaseModel):
    uuid: UUID


class RelevanteZaakSchema(BaseMixin):
    aard_relatie: Optional[str]
    overige_relatie: Optional[str]
    toelichting: Optional[str]

    @computed_field
    @property
    def url(self) -> Union[List, str]:
        field = HyperlinkedRelatedField(view_name="zaak-detail", lookup_field="uuid")
        return field.serialize_field(self.relevant_zaak)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        validate_by_name = True
        exclude_fields = {
            "relevant_zaak": UUIDZaakSchema,
        }


class ZaakKenmerkSchema(BaseMixin):
    kenmerk: str
    bron: str


class ZaakSchema(BaseMixin):
    zaak_identificatie: ZaakIdentificatie = Field(exclude=True, sa_type=JSON)

    uuid: UUID
    omschrijving: str
    toelichting: str
    registratiedatum: date
    verantwoordelijke_organisatie: str
    startdatum: date
    einddatum: Optional[date]
    einddatum_gepland: Optional[date]
    uiterlijke_einddatum_afdoening: Optional[date]
    publicatiedatum: Optional[date]
    communicatiekanaal: AnyUrl | str
    communicatiekanaal_naam: Optional[str]
    producten_of_diensten: List[AnyUrl]
    vertrouwelijkheidaanduiding: str
    betalingsindicatie: BetalingsIndicatie | str
    zaakgeometrie: Optional[GeoJSONGeometry]
    laatste_betaaldatum: Optional[datetime]
    verlenging_reden: str
    archiefnominatie: Optional[str]
    archiefstatus: Optional[str]
    archiefactiedatum: Optional[date]
    verlenging_duur: Optional[timedelta]
    selectielijstklasse: AnyUrl | str
    opdrachtgevende_organisatie: str
    processobjectaard: str
    startdatum_bewaartermijn: Optional[date]
    relevante_andere_zaken: List[RelevanteZaakSchema]
    kenmerken: List[ZaakKenmerkSchema]

    zaaktype: Annotated[
        ZaakType,
        HyperlinkedRelatedField(view_name="zaaktype-detail", lookup_field="uuid"),
    ]
    rollen: Annotated[
        List[Rol],
        HyperlinkedRelatedField(view_name="rol-detail", lookup_field="uuid"),
    ]
    hoofdzaak: Annotated[
        Optional[Zaak],
        HyperlinkedRelatedField(view_name="zaak-detail", lookup_field="uuid"),
    ]
    deelzaken: Annotated[
        List[Zaak],
        HyperlinkedRelatedField(view_name="zaak-detail", lookup_field="uuid"),
    ]

    eigenschappen: Annotated[
        List[ZaakEigenschap],
        NestedHyperlinkedRelatedField(
            view_name="eigenschappen-detail", lookup_fields=("uuid", "zaak_uuid")
        ),
    ]

    zaakinformatieobjecten: Annotated[
        List[ZaakInformatieObject],
        HyperlinkedRelatedField(
            view_name="zaakinformatieobject-detail", lookup_field="uuid"
        ),
    ]
    zaakobjecten: Annotated[
        List[ZaakObject],
        HyperlinkedRelatedField(
            view_name="zaakobjecttypen-detail", lookup_field="uuid"
        ),
    ]

    class Config:
        exclude_fields = {
            "processobject_datumkenmerk": Optional[str],
            "processobject_identificatie": Optional[str],
            "processobject_objecttype": Optional[str],
            "processobject_registratie": Optional[str],
            "opschorting_indicatie": bool,
            "opschorting_reden": Optional[str],
            "opschorting_eerdere_opschorting": bool,
            "verlenging_reden": Optional[str],
            "verlenging_duur": Optional[timedelta],
            "current_status_uuid": Optional[UUID],
            "current_resultaat_uuid": Optional[UUID],
        }

    @computed_field
    @property
    def url(self) -> Union[List, str]:
        field = HyperlinkedRelatedField(view_name="zaak-detail", lookup_field="uuid")
        return field.serialize_field(self)

    @computed_field
    @property
    def status(self) -> Optional[Union[List, str]]:
        if self.current_status_uuid:
            field = HyperlinkedRelatedField(
                view_name="statustypen-detail",
                value_field="current_status_uuid",
                lookup_field="uuid",
            )
            return field.serialize_field(self)
        return None

    @computed_field
    @property
    def resultaat(self) -> Optional[Union[List, str]]:
        if self.current_resultaat_uuid:
            field = HyperlinkedRelatedField(
                view_name="resultaattypen-detail",
                value_field="current_resultaat_uuid",
                lookup_field="uuid",
            )
            return field.serialize_field(self)
        return None

    @computed_field
    @property
    def identificatie(self) -> str:
        return self.zaak_identificatie.identificatie if self.zaak_identificatie else ""

    @computed_field
    @property
    def bronorganisatie(self) -> str:
        return (
            self.zaak_identificatie.bronorganisatie if self.zaak_identificatie else ""
        )

    @computed_field
    @property
    def processobject(self) -> dict:
        return {
            "datumkenmerk": self.processobject_datumkenmerk,
            "identificatie": self.processobject_identificatie,
            "objecttype": self.processobject_objecttype,
            "registratie": self.processobject_registratie,
        }

    @computed_field
    @property
    def opschorting(self) -> dict:
        return {
            "indicatie": self.opschorting_indicatie,
            "eerdereOpschorting": self.opschorting_eerdere_opschorting,
            "reden": self.opschorting_reden,
        }

    @computed_field
    @property
    def verlenging(self) -> Optional[dict]:
        if self.verlenging_reden:
            return {
                "reden": self.verlenging_reden,
                "duur": self.verlenging_duur,
            }
        return None

    @computed_field
    @property
    def betalingsindicatie_weergave(self) -> str:
        return (
            BetalingsIndicatie(self.betalingsindicatie).label
            if self.betalingsindicatie in BetalingsIndicatie
            else ""
        )
