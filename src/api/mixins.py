import humps
from pydantic import BaseModel
from sqlmodel import Field


def alias_keys(string):
    return humps.camelize(string)


class BaseMixin(BaseModel):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "Config") and hasattr(cls.Config, "exclude_fields"):
            exclude_fields = cls.Config.exclude_fields
            if not hasattr(cls, "__annotations__"):
                cls.__annotations__ = {}
            for field_name, field_type in exclude_fields.items():
                cls.__annotations__[field_name] = field_type
                setattr(cls, field_name, Field(exclude=True))

    class Config:
        alias_generator = alias_keys
        validate_by_name = True
        from_attributes = True
        arbitrary_types_allowed = True
