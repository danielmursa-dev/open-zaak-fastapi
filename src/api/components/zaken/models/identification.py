from sqlalchemy import Column, Integer, String

from src.core.database import Base


class ZaakIdentificatie(Base):
    __tablename__ = "zaken_zaakidentificatie"
    id = Column(Integer, primary_key=True)
    identificatie = Column(String(40))
    bronorganisatie = Column(String(9))
