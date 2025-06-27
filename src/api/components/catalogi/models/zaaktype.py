from uuid import uuid4

from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.core.database import Base


class ZaakType(Base):
    __tablename__ = "catalogi_zaaktype"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, index=True, nullable=False)
