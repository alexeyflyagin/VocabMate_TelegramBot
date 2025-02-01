from pydantic import BaseModel, field_validator, Field
from pydantic_core.core_schema import ValidationInfo

from src.services.models.checks import validate__str_is_not_empty
from src.services.models.entities import CardGroupEntity


class CreateCardGroupRequest(BaseModel):
    title: str

    @field_validator('title')
    def title__validator(cls, v, info: ValidationInfo):
        validate__str_is_not_empty(v, info.field_name)
        return v.strip()


class GetCardGroupsRequest(BaseModel):
    page: int = Field(default=0)
    limit: int = Field(default=10, ge=1, le=100)
    loop_pages: bool = True


class GetCardGroupsResponse(BaseModel):
    total_items: int
    page: int
    total_pages: int
    limit: int
    items: list[CardGroupEntity]

