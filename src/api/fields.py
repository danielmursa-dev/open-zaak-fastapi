from typing import Any, List, Optional, Union

from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from pydantic._internal._generate_schema import GetCoreSchemaHandler
from pydantic_core import core_schema
from shapely.geometry import mapping

from src.core.middleware import request_contextvar


class HyperlinkedRelatedField:
    def __init__(
        self,
        view_name: str,
        lookup_field: str = "uuid",
        value_field: Any = None,
    ):
        self.view_name = view_name
        self.lookup_field = lookup_field
        self.value_field = value_field

    def get_url(self, obj: Any) -> Optional[str]:
        """
        Given an object, return the URL that hyperlinks to the object.
        """
        if not obj:
            return None
        # Unsaved objects will not yet have a valid URL.
        if hasattr(obj, "pk") and obj.pk in (None, ""):
            return None
        request = request_contextvar.get()
        if self.value_field:
            value = getattr(obj, self.value_field)
        else:
            value = getattr(obj, self.lookup_field)
        return str(request.url_for(self.view_name, **{self.lookup_field: value}))

    def serialize_field(self, value: Any) -> Union[List, str]:
        if isinstance(value, list):
            return [self.get_url(obj) for obj in value]
        else:
            return self.get_url(value)

    def _validate(self, value: Any, _info) -> Any:
        return value

    def _serialize(
        self, value: Any, _serializer, info: core_schema.SerializationInfo
    ) -> Any:
        return self.serialize_field(value)

    def __get_pydantic_core_schema__(
        self, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        source_schema = handler(source_type)

        return core_schema.with_info_after_validator_function(
            self._validate,
            source_schema,
            serialization=core_schema.wrap_serializer_function_ser_schema(
                self._serialize,
                info_arg=True,
                return_schema=core_schema.chain_schema(
                    [
                        core_schema.union_schema(
                            [
                                core_schema.list_schema(core_schema.any_schema()),
                                core_schema.str_schema(),
                            ]
                        )
                    ]
                ),
                when_used="json",
            ),
        )


class NestedHyperlinkedRelatedField(HyperlinkedRelatedField):
    def __init__(
        self,
        view_name: str,
        lookup_fields: tuple[str, str],
    ):
        super().__init__(view_name=view_name)
        self.lookup_fields = lookup_fields

    def get_url(self, obj: Any) -> Optional[str]:
        if not obj:
            return None

        try:
            lookup_values = {field: getattr(obj, field) for field in self.lookup_fields}
        except AttributeError:
            return None

        if any(v in (None, "") for v in lookup_values.values()):
            return None

        request = request_contextvar.get()
        return str(request.url_for(self.view_name, **lookup_values))


class GeoJSONGeometry:
    def __init__(self, value: WKBElement):
        if not isinstance(value, WKBElement):
            raise TypeError(f"Expected WKBElement, got {type(value)}")
        self._value = value
        self._shape = to_shape(value)

    def to_geojson(self) -> dict:
        return mapping(self._shape)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls._validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize, return_schema=core_schema.any_schema()
            ),
        )

    @classmethod
    def _validate(cls, value: Any) -> "GeoJSONGeometry":
        return cls(value)

    @classmethod
    def _serialize(cls, value: "GeoJSONGeometry") -> dict:
        return value.to_geojson()
