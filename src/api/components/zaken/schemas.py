from datetime import date, datetime, timedelta
from src.api.fields import HyperlinkedRelatedField, GeoJSONGeometry
from src.api.components.catalogi.models.zaaktype import ZaakType
from src.api.components.zaken.models.identification import ZaakIdentificatie
from src.api.components.zaken.models.zaken import (
    Rol,
    Zaak,
    ZaakInformatieObject,
    ZaakEigenschap,
    ZaakObject,
    Resultaat,
    Status,
    BetalingsIndicatie,
)
from src.api.mixins import BaseMixin
from typing import Union, Annotated, List, Optional
from pydantic import computed_field, AnyUrl
from uuid import UUID
from sqlalchemy import JSON
from sqlmodel import Field


class RelevanteZaakSchema(BaseMixin):
    aard_relatie: Optional[str]
    overige_relatie: Optional[str]
    toelichting: Optional[str]


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
        HyperlinkedRelatedField(view_name="zaaktype-detail", lookup_field="uuid"),
    ]
    deelzaken: Annotated[
        List[Zaak],
        HyperlinkedRelatedField(view_name="zaaktype-detail", lookup_field="uuid"),
    ]
    eigenschappen: Annotated[
        List[ZaakEigenschap],
        HyperlinkedRelatedField(
            view_name="rol-detail", lookup_field="uuid"
        ),  # TODO check all url
    ]
    zaakinformatieobjecten: Annotated[
        List[ZaakInformatieObject],
        HyperlinkedRelatedField(view_name="rol-detail", lookup_field="uuid"),
    ]
    zaakobjecten: Annotated[
        List[ZaakObject],
        HyperlinkedRelatedField(view_name="rol-detail", lookup_field="uuid"),
    ]
    resultaat: Annotated[
        List[Resultaat],
        HyperlinkedRelatedField(view_name="rol-detail", lookup_field="uuid"),
    ]
    status: Annotated[
        List[Status],
        HyperlinkedRelatedField(view_name="rol-detail", lookup_field="uuid"),
    ]

    # verlenging  # TODO method

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        validate_by_name = True
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
        }

    @computed_field
    @property
    def url(self) -> Union[List, str]:
        field = HyperlinkedRelatedField(view_name="zaak-detail", lookup_field="uuid")
        return field.serialize_field(self)

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
    def verlenging(self) -> dict:
        return {
            "reden": self.verlenging_reden,
            "duur": self.verlenging_duur,
        }

    @computed_field
    @property
    def betalingsindicatie_weergave(self) -> str:
        return (
            BetalingsIndicatie(self.betalingsindicatie).label
            if self.betalingsindicatie in BetalingsIndicatie
            else ""
        )
