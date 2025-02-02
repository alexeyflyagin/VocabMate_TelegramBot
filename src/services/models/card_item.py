from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from src.services.models.checks import validate__str_is_not_empty


class AddCardItemRequest(BaseModel):
    group_id: int
    term: str
    definition: str

    @field_validator('term', 'definition')
    def str_is_not_empty__validator(cls, v, info: ValidationInfo):
        validate__str_is_not_empty(v, info.field_name)
        return v.strip()
