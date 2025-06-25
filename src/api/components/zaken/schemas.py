from datetime import date, datetime, timedelta
from src.api.fields import HyperlinkedRelatedField
from src.api.components.zaken.models import (
    Rol,
    ZaakIdentificatie,
    ZaakType,
    Zaak,
    ZaakInformatieObject,
    ZaakEigenschap,
    ZaakKenmerk,
    ZaakObject,
    Resultaat,
)
from typing import Union, Annotated, List, Optional
from pydantic import computed_field, BaseModel, AnyUrl
from uuid import UUID
from sqlalchemy import JSON
from sqlmodel import Field


class ZaakSchema(BaseModel):
    zaak_identificatie: ZaakIdentificatie = Field(exclude=True, sa_type=JSON)
    processobject_datumkenmerk: str = Field(exclude=True)
    processobject_identificatie: str = Field(exclude=True)
    processobject_objecttype: str = Field(exclude=True)
    processobject_registratie: str = Field(exclude=True)
    uuid: UUID
    omschrijving: str
    toelichting: str
    registratiedatum: date
    verantwoordelijke_organisatie: str
    startdatum: date
    einddatum: date | None
    einddatum_gepland: date | None
    uiterlijke_einddatum_afdoening: date | None
    publicatiedatum: date | None
    communicatiekanaal: AnyUrl | str
    communicatiekanaal_naam: str | None
    # producten_of_diensten TODO
    vertrouwelijkheidaanduiding: str
    betalingsindicatie: str  # TODO choice field check text
    # get_betalingsindicatie_display TODO
    laatste_betaaldatum: datetime | None  # chekc format date
    zaakgeometrie: str | None  # check geometry coordinates
    verlenging_reden: str
    archiefnominatie: str | None
    archiefstatus: str | None
    archiefactiedatum: date | None
    verlenging_duur: timedelta | None
    # opschorting_indicatie TODO external or not check ?
    selectielijstklasse: AnyUrl | str  # check this url or none or str ?
    opdrachtgevende_organisatie: str
    processobjectaard: str
    startdatum_bewaartermijn: date | None
    # status: str # to be finished
    # relevante_andere_zaken extern
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
    kenmerken: ZaakKenmerk  # check fields
    # betalingsindicatie_weergave  # TODO method
    # verlenging  # TODO method

    class Config:
        from_attributes = True
        validate_by_name = True

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
