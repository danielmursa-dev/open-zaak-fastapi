from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from dataclasses import dataclass

from fastapi import Query
from fastapi_pagination.customization import (
    ClsNamespace,
    CustomizedPage,
    PageCls,
    UseParamsFields,
)
from fastapi_pagination.default import Page as BasePage
from fastapi_pagination.links.bases import BaseLinksCustomizer, Links, TPage_contra
from fastapi_pagination.links.default import (
    DefaultLinksCustomizer,
    TAny,
    resolve_default_links,
)
from pydantic import Field


@dataclass
class BaseUseLinks(BaseLinksCustomizer[TPage_contra], ABC):
    previous_page: str = "previous_page"
    next_page: str = "next_page"

    def customize_page_ns(self, page_cls: PageCls, ns: ClsNamespace) -> None:
        from pydantic import computed_field

        ns[self.previous_page] = computed_field(return_type=str, alias="previous")(
            lambda _self: self.resolve_links(_self, "prev")
        )
        ns[self.next_page] = computed_field(return_type=str, alias="next")(
            lambda _self: self.resolve_links(_self, "next")
        )


class CustomDefaultLinksCustomizer(DefaultLinksCustomizer):
    def resolve_links(self, _page: BasePage, key: str) -> Links:
        links = resolve_default_links(_page, only_path=False)
        return getattr(links, key, "")


class UseLinks(CustomDefaultLinksCustomizer, BaseUseLinks):
    pass


class CustomBasePage(BasePage):
    items: Sequence[TAny] = Field(alias="results")
    total: int = Field(alias="count")
    size: int = Field(exclude=True)
    page: int = Field(exclude=True)
    pages: int = Field(exclude=True)


Page = CustomizedPage[
    CustomBasePage[TAny],
    UseParamsFields(
        size=Query(100, ge=1, le=1000, alias="pageSize"),
    ),
    UseLinks(),
]
