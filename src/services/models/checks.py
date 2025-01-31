def validate__str_is_not_empty(v: str, field_name: str):
    if not v.strip():
        raise ValueError(f"The {field_name} value cannot be empty")
    return v


def validate__is_not_empty(v, field_name: str):
    if not v:
        raise ValueError(f"The {field_name} value cannot be empty")
    return v
