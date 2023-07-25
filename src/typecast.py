from typing import get_type_hints, Protocol, ClassVar


class Dataclass(Protocol):
    __dataclass_fields__: ClassVar[dict]


class TypeCoerceError(Exception):
    def __init__(self, attr_name: str, attr_type: type):
        self.attr_name = attr_name
        self.attr_type = attr_type

    def __str__(self):
        return f"Value {self.attr_name} cannot be coerced into type {self.attr_type}"


class ValueNotFoundError(Exception):
    def __init__(self, missed_val):
        self.missed_val = missed_val

    def __str__(self):
        return f"Value {self.missed_val} is not found"


def parse_config(config: Dataclass, values: dict) -> dict:
    attrs = get_type_hints(config).items()
    if not attrs:
        return {}

    config_dict = dict()
    for attr_name, attr_type in attrs:
        if (val := values.get(attr_name)) == None:
            raise ValueNotFoundError(attr_name)
        try:
            config_dict[attr_name] = attr_type(val)
        except ValueError as ve:
            raise TypeCoerceError(attr_name, attr_type)
    return config_dict