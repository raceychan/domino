import typing

IMMUTABLE_NONCONTAINER_TYPES = {
    int,
    float,
    complex,
    bool,
    str,
    bytes,
    True,
    False,
    None,
}

IMMUTABLE_CONTAINER_TYPES = {tuple, frozenset, typing.Union, typing.Literal}


def is_field_immutable(field):
    # Base case: if this is a non-container type, it is immutable
    if field in IMMUTABLE_NONCONTAINER_TYPES:
        return True

    # Get the original type for types from the typing module
    origin = getattr(field, "__origin__", None)

    # If this is a container type, it is immutable if all its contained types are
    if origin and origin in IMMUTABLE_CONTAINER_TYPES:
        return all(is_field_immutable(arg) for arg in field.__args__)

    # If this is a class, it is immutable if all its fields are
    if isinstance(field, type) and hasattr(field, "__annotations__"):
        return is_class_immutable(field)

    # TODO: should return information about field that is mutable

    # If this is an unknown type, we can't determine its mutability
    return False


def is_class_immutable(cls):
    # BUG: cosnsider class T(tuple): ...
    # class B(T): ...
    # both are subclass of immutable,
    # yet would be assert to be mutable in current impl

    annotations = typing.get_type_hints(cls)
    namespace = annotations.items()
    for attr_name, attr_type in namespace:
        if not is_field_immutable(attr_type):
            print(f"Attribute {attr_name} of {cls} is mutable")
            return False
    return True