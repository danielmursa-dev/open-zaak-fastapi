from datetime import date, datetime
from uuid import uuid4

from geoalchemy2 import Geometry
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Interval,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from src.core.database import Base


class Zaak(Base):
    __tablename__ = "zaken_zaak"

    identificatie_ptr_id = Column(
        Integer, ForeignKey("zaken_zaakidentificatie.id"), primary_key=True
    )

    zaak_identificatie = relationship("ZaakIdentificatie", backref="zaak")

    uuid = Column(UUID(as_uuid=True), default=uuid4, index=True, nullable=False)

    hoofdzaak_id = Column(
        Integer, ForeignKey("zaken_zaak.identificatie_ptr_id"), nullable=True
    )
    hoofdzaak = relationship(
        "Zaak", remote_side=[identificatie_ptr_id], back_populates="deelzaken"
    )
    deelzaken = relationship(
        "Zaak", back_populates="hoofdzaak", foreign_keys=[hoofdzaak_id]
    )

    omschrijving = Column(String(80), nullable=True)
    toelichting = Column(String(1000), nullable=True)

    zaaktype_id = Column(
        Integer,
        ForeignKey("catalogi_zaaktype.id"),
        name="_zaaktype_id",
    )
    zaaktype = relationship("ZaakType")

    rollen = relationship("Rol", back_populates="zaak")
    eigenschappen = relationship("ZaakEigenschap", back_populates="zaak")
    zaakobjecten = relationship("ZaakObject", back_populates="zaak")
    kenmerken = relationship("ZaakKenmerk", back_populates="zaak")
    status = relationship("Status", back_populates="zaak")

    relevante_andere_zaken = relationship(
        "RelevanteZaakRelatie",
        back_populates="zaak",
        foreign_keys="[RelevanteZaakRelatie.zaak_id]",
    )

    resultaat = relationship("Resultaat", back_populates="zaak")
    zaakinformatieobjecten = relationship("ZaakInformatieObject", back_populates="zaak")
    registratiedatum = Column(Date, default=date.today, nullable=False)
    verantwoordelijke_organisatie = Column(String(9), nullable=False)
    producten_of_diensten = Column(JSON, nullable=True, default=list)
    startdatum = Column(Date, index=True, nullable=False)
    einddatum = Column(Date, nullable=True)
    einddatum_gepland = Column(Date, nullable=True)
    uiterlijke_einddatum_afdoening = Column(Date, nullable=True)
    publicatiedatum = Column(Date, nullable=True)
    communicatiekanaal = Column(String(1000), nullable=True)
    vertrouwelijkheidaanduiding = Column(String, nullable=True)
    betalingsindicatie = Column(String, nullable=True, default=None)
    laatste_betaaldatum = Column(DateTime, nullable=True)
    zaakgeometrie = Column(Geometry(geometry_type="GEOMETRY", srid=4326), nullable=True)
    verlenging_reden = Column(String(200), nullable=True)
    verlenging_duur = Column(Interval, nullable=True)
    opschorting_indicatie = Column(Boolean, default=False, nullable=False)
    opschorting_reden = Column(String(200), nullable=True)
    opschorting_eerdere_opschorting = Column(Boolean, default=False, nullable=False)
    selectielijstklasse = Column(String(1000), nullable=True)
    archiefnominatie = Column(String(40), index=True, nullable=True)
    archiefstatus = Column(
        String(40), index=True, default="nog_te_archiveren", nullable=False
    )
    archiefactiedatum = Column(Date, index=True, nullable=True)
    opdrachtgevende_organisatie = Column(String, nullable=True)
    processobjectaard = Column(String(200), nullable=True)
    startdatum_bewaartermijn = Column(Date, nullable=True)
    processobject_datumkenmerk = Column(String(250), nullable=True)
    processobject_identificatie = Column(String(250), nullable=True)
    processobject_objecttype = Column(String(250), nullable=True)
    processobject_registratie = Column(String(250), nullable=True)
    communicatiekanaal_naam = Column(String(250), nullable=True)
    created_on = Column(DateTime, default=datetime.utcnow, nullable=False)


class Rol(Base):
    __tablename__ = "zaken_rol"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, index=True, nullable=False)

    zaak_id = Column(Integer, ForeignKey("zaken_zaak.identificatie_ptr_id"))
    zaak = relationship("Zaak", back_populates="rollen")


class ZaakEigenschap(Base):
    __tablename__ = "zaken_zaakeigenschap"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, index=True, nullable=False)

    zaak_id = Column(Integer, ForeignKey("zaken_zaak.identificatie_ptr_id"))
    zaak = relationship("Zaak", back_populates="eigenschappen")


class ZaakInformatieObject(Base):
    __tablename__ = "zaken_zaakinformatieobject"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, index=True, nullable=False)

    zaak_id = Column(Integer, ForeignKey("zaken_zaak.identificatie_ptr_id"))
    zaak = relationship("Zaak", back_populates="zaakinformatieobjecten")


class ZaakObject(Base):
    __tablename__ = "zaken_zaakobject"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, index=True, nullable=False)

    zaak_id = Column(Integer, ForeignKey("zaken_zaak.identificatie_ptr_id"))
    zaak = relationship("Zaak", back_populates="zaakobjecten")


class ZaakKenmerk(Base):
    __tablename__ = "zaken_zaakkenmerk"

    id = Column(Integer, primary_key=True)
    zaak_id = Column(Integer, ForeignKey("zaken_zaak.identificatie_ptr_id"))
    zaak = relationship("Zaak", back_populates="kenmerken")

    kenmerk = Column(String(40), nullable=False)
    bron = Column(String(40), nullable=False)


class Resultaat(Base):
    __tablename__ = "zaken_resultaat"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, index=True, nullable=False)

    zaak_id = Column(Integer, ForeignKey("zaken_zaak.identificatie_ptr_id"))
    zaak = relationship("Zaak", back_populates="resultaat")


class Status(Base):
    __tablename__ = "zaken_status"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, index=True, nullable=False)

    zaak_id = Column(Integer, ForeignKey("zaken_zaak.identificatie_ptr_id"))
    zaak = relationship("Zaak", back_populates="status")


class RelevanteZaakRelatie(Base):
    __tablename__ = "zaken_relevantezaakrelatie"

    id = Column(Integer, primary_key=True)

    zaak_id = Column(Integer, ForeignKey("zaken_zaak.identificatie_ptr_id"))
    zaak = relationship(
        "Zaak", back_populates="relevante_andere_zaken", foreign_keys=[zaak_id]
    )

    relevant_zaak_id = Column(
        "_relevant_zaak_id",
        Integer,
        ForeignKey("zaken_zaak.identificatie_ptr_id"),
        nullable=True,
    )
    relevant_zaak = relationship("Zaak", foreign_keys=[relevant_zaak_id])

    aard_relatie = Column(String(20))
    overige_relatie = Column(String(100))
    toelichting = Column(String(255))
