from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class ZaakType(SQLModel, table=True):
    __tablename__ = "catalogi_zaaktype"
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(
        default_factory=uuid4,
        index=True,
        description="Unieke resource identifier (UUID4)",
    )
