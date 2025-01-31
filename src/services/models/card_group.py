from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from src.services.models.checks import validate__str_is_not_empty


class CreateCardGroupRequest(BaseModel):
    title: str

    @field_validator('title')
    def title__validator(cls, v, info: ValidationInfo):
        validate__str_is_not_empty(v, info.field_name)
        return v.strip()