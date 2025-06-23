from typing import Optional
from uuid import UUID
from datetime import date, datetime, timedelta
from sqlmodel import SQLModel
from .models import Zaak

from pydantic import computed_field

from pydantic import BaseModel, AnyUrl, TypeAdapter
from fastapi import Request


url_adapter = TypeAdapter(AnyUrl)


class ZaakSerializer(Zaak):
    @computed_field
    @property
    def url(self) -> AnyUrl:
        url_str = f"http://localhost:8000/zaken/api/v1/zaken/{self.uuid}"
        return url_adapter.validate_python(url_str)
