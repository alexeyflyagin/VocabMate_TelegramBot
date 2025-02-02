from pydantic import BaseModel

from src.services.models.entities import CardItemEntity, CardGroupEntity


class TrainingLevelData(BaseModel):
    level_id: int | None
    training_id: int
    total_answered: int
    total_answered_wrong: int
    total_levels: int
    is_completed: bool
    card_group: CardGroupEntity
    card_item: CardItemEntity | None


class AnswerLevelRequest(BaseModel):
    training_id: int
    is_right: bool


class AnswerLevelResponse(BaseModel):
    training_id: int
    total_added: int
    card_item: CardItemEntity


class StartTrainingRequest(BaseModel):
    card_group_id: int


class StartTrainingResponse(BaseModel):
    total_levels: int
    training_id: int
    card_group: CardGroupEntity
