from typing import Optional, List
from uuid import UUID, uuid4
from datetime import date, datetime, timedelta
from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import Integer, ForeignKey
from .identification import ZaakIdentificatie
from src.api.components.catalogi.models.zaaktype import ZaakType


class Zaak(SQLModel, table=True):
    __tablename__ = "zaken_zaak"

    identificatie_ptr_id: int = Field(
        primary_key=True,
        foreign_key="zaken_zaakidentificatie.id",
        description=(
            "Zaak identification details are tracked in a separate table so numbers "
            "can be generated/reserved before the zaak is actually created."
        ),
    )
    zaak_identificatie: Optional[ZaakIdentificatie] = Relationship()

    uuid: UUID = Field(
        default_factory=uuid4,
        index=True,
        description="Unieke resource identifier (UUID4)",
    )

    hoofdzaak_id: Optional[int] = Field(
        default=None,
        foreign_key="zaken_zaak.identificatie_ptr_id",
        description=(
            "URL-referentie naar de ZAAK, waarom verzocht is door de "
            "initiator daarvan, die behandeld wordt in twee of meer "
            "separate ZAAKen waarvan de onderhavige ZAAK er één is."
        ),
    )
    deelzaken: List["Zaak"] = Relationship(back_populates="hoofdzaak")

    hoofdzaak: Optional["Zaak"] = Relationship(
        back_populates="deelzaken",
        sa_relationship_kwargs={"remote_side": "Zaak.identificatie_ptr_id"},
    )

    omschrijving: Optional[str] = Field(
        default=None,
        max_length=80,
        description="Een korte omschrijving van de zaak.",
    )
    toelichting: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Een toelichting op de zaak.",
    )
    zaaktype_id: int = Field(
        sa_column=Column(
            "_zaaktype_id",
            Integer,
            ForeignKey("catalogi_zaaktype.id"),
        )
    )
    zaaktype: Optional["ZaakType"] = Relationship()

    eigenschappen: List["ZaakEigenschap"] = Relationship(back_populates="zaak")
    zaakobjecten: List["ZaakObject"] = Relationship(back_populates="zaak")
    kenmerken: List["ZaakKenmerk"] = Relationship(back_populates="zaak")
    resultaat: List["Resultaat"] = Relationship(
        back_populates="zaak"
    )  # TODO group all per type
    zaakinformatieobjecten: List["ZaakInformatieObject"] = Relationship(
        back_populates="zaak"
    )

    registratiedatum: date = Field(
        default_factory=date.today,
        description=(
            "De datum waarop de zaakbehandelende organisatie de ZAAK "
            "heeft geregistreerd. Indien deze niet opgegeven wordt, "
            "wordt de datum van vandaag gebruikt."
        ),
    )
    verantwoordelijke_organisatie: str = Field(
        min_length=9,
        max_length=9,
        description=(
            "Het RSIN van de Niet-natuurlijk persoon zijnde de organisatie "
            "die eindverantwoordelijk is voor de behandeling van de "
            "zaak. Dit moet een geldig RSIN zijn van 9 nummers en voldoen aan "
            "https://nl.wikipedia.org/wiki/Burgerservicenummer#11-proef"
        ),
    )

    startdatum: date = Field(
        index=True,
        description="De datum waarop met de uitvoering van de zaak is gestart",
    )
    einddatum: Optional[date] = Field(
        default=None,
        description="De datum waarop de uitvoering van de zaak afgerond is.",
    )

    einddatum_gepland: Optional[date] = Field(
        default=None,
        description="De datum waarop volgens de planning verwacht wordt dat de zaak afgerond wordt.",
    )
    uiterlijke_einddatum_afdoening: Optional[date] = Field(
        default=None,
        description="De laatste datum waarop volgens wet- en regelgeving de zaak afgerond dient te zijn.",
    )
    publicatiedatum: Optional[date] = Field(
        default=None,
        description="Datum waarop (het starten van) de zaak gepubliceerd is of wordt.",
    )

    communicatiekanaal: Optional[str] = Field(
        default=None,
        max_length=1000,
        description=(
            "Het medium waarlangs de aanleiding om een zaak te starten is ontvangen. "
            "URL naar een communicatiekanaal in de VNG-Referentielijst van communicatiekanalen."
        ),
    )

    vertrouwelijkheidaanduiding: Optional[str] = Field(
        default=None,
        description=(
            "Aanduiding van de mate waarin het zaakdossier van de ZAAK voor de openbaarheid bestemd is."
        ),
    )

    betalingsindicatie: Optional[str] = Field(
        default=None,
        max_length=20,
        description=(
            "Indicatie of de, met behandeling van de zaak gemoeide, "
            "kosten betaald zijn door de desbetreffende betrokkene."
        ),
    )
    laatste_betaaldatum: Optional[datetime] = Field(
        default=None,
        description=(
            "De datum waarop de meest recente betaling is verwerkt "
            "van kosten die gemoeid zijn met behandeling van de zaak."
        ),
    )

    zaakgeometrie: Optional[str] = Field(
        default=None,
        description="Punt, lijn of (multi-)vlak geometrie-informatie.",
    )

    verlenging_reden: Optional[str] = Field(
        default=None,
        max_length=200,
        description=(
            "Omschrijving van de reden voor het verlengen van de behandeling van de zaak."
        ),
    )
    verlenging_duur: Optional[timedelta] = Field(
        default=None,
        description=(
            "Het aantal werkbare dagen waarmee de doorlooptijd van de "
            "behandeling van de ZAAK is verlengd (of verkort) ten opzichte "
            "van de eerder gecommuniceerde doorlooptijd."
        ),
    )

    opschorting_indicatie: bool = Field(
        default=False,
        description=(
            "Aanduiding of de behandeling van de ZAAK tijdelijk is opgeschort."
        ),
    )
    opschorting_reden: Optional[str] = Field(
        default=None,
        max_length=200,
        description=(
            "Omschrijving van de reden voor het opschorten van de behandeling van de zaak."
        ),
    )
    opschorting_eerdere_opschorting: bool = Field(
        default=False,
        description=(
            "Aanduiding of de behandeling van de ZAAK in het verleden is opgeschort."
        ),
    )

    selectielijstklasse: Optional[str] = Field(
        default=None,
        max_length=1000,
        description=(
            "URL-referentie naar de categorie in de gehanteerde 'Selectielijst Archiefbescheiden' die, gezien "
            "het zaaktype en het resultaattype van de zaak, bepalend is voor het archiefregime van de zaak."
        ),
    )

    archiefnominatie: Optional[str] = Field(
        default=None,
        max_length=40,
        description=(
            "Aanduiding of het zaakdossier blijvend bewaard of na een bepaalde termijn vernietigd moet worden."
        ),
        index=True,
    )
    archiefstatus: str = Field(
        default="nog_te_archiveren",
        max_length=40,
        description=(
            "Aanduiding of het zaakdossier blijvend bewaard of na een bepaalde termijn vernietigd moet worden."
        ),
        index=True,
    )
    archiefactiedatum: Optional[date] = Field(
        default=None,
        description=(
            "De datum waarop het gearchiveerde zaakdossier vernietigd moet worden dan wel overgebracht moet "
            "worden naar een archiefbewaarplaats. Wordt automatisch berekend bij het aanmaken of wijzigen van "
            "een RESULTAAT aan deze ZAAK indien nog leeg."
        ),
        index=True,
    )

    opdrachtgevende_organisatie: Optional[str] = Field(
        default=True,
        description=(
            "De krachtens publiekrecht ingestelde rechtspersoon dan wel "
            "ander niet-natuurlijk persoon waarbinnen het (bestuurs)orgaan zetelt "
            "dat opdracht heeft gegeven om taken uit te voeren waaraan de zaak "
            "invulling geeft."
        ),
    )

    processobjectaard: Optional[str] = Field(
        default=None,
        max_length=200,
        description=(
            "Omschrijving van het object, subject of gebeurtenis waarop, vanuit"
            " archiveringsoptiek, de zaak betrekking heeft."
        ),
    )
    startdatum_bewaartermijn: Optional[date] = Field(
        default=None,
        description=(
            "De datum die de start markeert van de termijn waarop het zaakdossier"
            " vernietigd moet worden."
        ),
    )
    processobject_datumkenmerk: Optional[str] = Field(
        default=None,
        max_length=250,
        description=(
            "De naam van de attribuutsoort van het procesobject dat bepalend is "
            "voor het einde van de procestermijn."
        ),
    )
    processobject_identificatie: Optional[str] = Field(
        default=None,
        max_length=250,
        description=("De unieke aanduiding van het procesobject."),
    )
    processobject_objecttype: Optional[str] = Field(
        default=None,
        max_length=250,
        description=("Het soort object dat het procesobject representeert."),
    )
    processobject_registratie: Optional[str] = Field(
        default=None,
        max_length=250,
        description=(
            "De naam van de registratie waarvan het procesobject deel uit maakt."
        ),
    )
    communicatiekanaal_naam: Optional[str] = Field(
        default=None,
        max_length=250,
        description=(
            "De naam van het medium waarlangs de aanleiding om een zaak te starten is ontvangen."
        ),
    )

    rollen: List["Rol"] = Relationship(back_populates="zaak")

    created_on: datetime = Field(default_factory=datetime.utcnow)


class Rol(SQLModel, table=True):
    __tablename__ = "zaken_rol"

    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(
        default_factory=uuid4,
        index=True,
        description="Unieke resource identifier (UUID4)",
    )

    zaak_id: int | None = Field(
        default=None,
        foreign_key="zaken_zaak.identificatie_ptr_id",
    )
    zaak: Zaak | None = Relationship(back_populates="rollen")


class ZaakEigenschap(SQLModel, table=True):
    __tablename__ = "zaken_zaakeigenschap"
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(
        default_factory=uuid4,
        index=True,
        description="Unieke resource identifier (UUID4)",
    )
    zaak_id: int | None = Field(
        default=None,
        foreign_key="zaken_zaak.identificatie_ptr_id",
    )
    zaak: Zaak | None = Relationship(back_populates="eigenschappen")


class ZaakInformatieObject(SQLModel, table=True):
    __tablename__ = "zaken_zaakinformatieobject"
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(
        default_factory=uuid4,
        index=True,
        description="Unieke resource identifier (UUID4)",
    )
    zaak_id: int | None = Field(
        default=None,
        foreign_key="zaken_zaak.identificatie_ptr_id",
    )
    zaak: Zaak | None = Relationship(back_populates="zaakinformatieobjecten")


class ZaakObject(SQLModel, table=True):
    __tablename__ = "zaken_zaakobject"
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(
        default_factory=uuid4,
        index=True,
        description="Unieke resource identifier (UUID4)",
    )
    zaak_id: int | None = Field(
        default=None,
        foreign_key="zaken_zaak.identificatie_ptr_id",
    )
    zaak: Zaak | None = Relationship(back_populates="zaakobjecten")


class ZaakKenmerk(SQLModel, table=True):
    __tablename__ = "zaken_zaakkenmerk"
    id: Optional[int] = Field(default=None, primary_key=True)
    zaak_id: int | None = Field(
        default=None,
        foreign_key="zaken_zaak.identificatie_ptr_id",
    )
    zaak: Zaak | None = Relationship(back_populates="kenmerken")


class Resultaat(SQLModel, table=True):
    __tablename__ = "zaken_resultaat"
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(
        default_factory=uuid4,
        index=True,
        description="Unieke resource identifier (UUID4)",
    )
    zaak_id: int | None = Field(
        default=None,
        foreign_key="zaken_zaak.identificatie_ptr_id",
    )

    zaak: Zaak | None = Relationship(back_populates="resultaat")
