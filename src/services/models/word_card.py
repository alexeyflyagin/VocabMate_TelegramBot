from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from src.services.models.checks import validate__str_is_not_empty, validate__is_not_empty


class AddWordCardRequest(BaseModel):
    group_id: int
    word: str
    transcription: str
    translation: list[str]
    pos: list[str]

    @field_validator('word', 'transcription', )
    def str_is_not_empty__validator(cls, v, info: ValidationInfo):
        validate__str_is_not_empty(v, info.field_name)
        return v.strip()

    @field_validator('translation', 'pos', )
    def is_not_empty__validator(cls, v, info: ValidationInfo):
        validate__is_not_empty(v, info.field_name)
        return v.strip()
