from sqlmodel import SQLModel, Field
from typing import Optional


class ZaakIdentificatie(SQLModel, table=True):
    __tablename__ = "zaken_zaakidentificatie"
    id: Optional[int] = Field(default=None, primary_key=True)
    identificatie: Optional[str] = Field(
        default="",
        max_length=40,
        description=(
            "De unieke identificatie van de ZAAK binnen de organisatie "
            "die verantwoordelijk is voor de behandeling van de ZAAK."
        ),
    )
    bronorganisatie: str = Field(
        min_length=9,
        max_length=9,
        description=(
            "Het RSIN van de Niet-natuurlijk persoon zijnde de "
            "organisatie die de zaak heeft gecreeerd. Dit moet een geldig "
            "RSIN zijn van 9 nummers en voldoen aan "
            "https://nl.wikipedia.org/wiki/Burgerservicenummer#11-proef"
        ),
    )
