from enum import Enum


class BetalingsIndicatie(str, Enum):
    NVT = "nvt"
    NOG_NIET = "nog_niet"
    GEDEELTELIJK = "gedeeltelijk"
    GEHEEL = "geheel"

    @property
    def label(self) -> dict:
        labels = {
            self.NVT: "Er is geen sprake van te betalen, met de zaak gemoeide, kosten.",
            self.NOG_NIET: "De met de zaak gemoeide kosten zijn (nog) niet betaald.",
            self.GEDEELTELIJK: "De met de zaak gemoeide kosten zijn gedeeltelijk betaald.",
            self.GEHEEL: "De met de zaak gemoeide kosten zijn geheel betaald.",
        }
        return labels[self.value] if self.value in labels else ""
