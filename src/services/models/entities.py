from datetime import datetime

from pydantic import BaseModel


class CardGroupEntity(BaseModel):
    id: int
    date_create: datetime
    title: str

    class Config:
        from_attributes = True
