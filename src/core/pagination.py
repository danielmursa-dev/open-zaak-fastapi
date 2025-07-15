from __future__ import annotations

from collections.abc import Sequence
from typing import Optional

from fastapi import Query
from fastapi_pagination.customization import (
    CustomizedPage,
    UseParamsFields,
)
from fastapi_pagination.default import Page as BasePage
from fastapi_pagination.links.default import TAny, resolve_default_links
from pydantic import Field


class CustomBasePage(BasePage):
    items: Sequence[TAny] = Field(alias="results")
    total: int = Field(alias="count")
    size: int = Field(exclude=True)
    page: int = Field(exclude=True)
    pages: int = Field(exclude=True)
    previous: Optional[str] = Field(default=None)
    next: Optional[str] = Field(default=None)

    def __init__(self, **data):
        super().__init__(**data)
        links = resolve_default_links(self, only_path=True)

        self.previous = getattr(links, "prev", None)
        self.next = getattr(links, "next", None)


Page = CustomizedPage[
    CustomBasePage[TAny],
    UseParamsFields(
        size=Query(100, ge=1, le=1000, alias="pageSize"),
    ),
]
