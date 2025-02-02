from datetime import datetime
from typing import Any

from sqlalchemy import BIGINT, VARCHAR, JSON, DateTime, ForeignKey, TEXT, BOOLEAN
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

CASCADE = "CASCADE"
SET_NULL = "SET NULL"


class UserStateOrm(Base):
    __tablename__ = 'user_state'
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    bot_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    chat_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    thread_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True)
    business_connection_id: Mapped[str | None] = mapped_column(VARCHAR, nullable=True)
    destiny: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    state: Mapped[str | None] = mapped_column(VARCHAR, default=None, nullable=True)


class CardGroupOrm(Base):
    __tablename__ = 'card_group'
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    title: Mapped[str] = mapped_column(VARCHAR, nullable=False)


class CardItemOrm(Base):
    __tablename__ = 'card_item'
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    group_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('card_group.id', ondelete=CASCADE), nullable=False)
    term: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    definition: Mapped[str] = mapped_column(TEXT, nullable=False)


class TrainingLevelOrm(Base):
    __tablename__ = 'training_level'
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    training_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('training.id', ondelete=CASCADE), nullable=False)
    card_item_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('card_item.id', ondelete=CASCADE), nullable=False)
    answer_is_right: Mapped[bool | None] = mapped_column(BOOLEAN, default=None, nullable=True)
    answered_at: Mapped[datetime | None] = mapped_column(DateTime, default=None, nullable=True)


class TrainingOrm(Base):
    __tablename__ = 'training'
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    card_group_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('card_group.id', ondelete=CASCADE), nullable=False)
    current_level_id: Mapped[int | None] = mapped_column(BIGINT, ForeignKey('training_level.id', ondelete=SET_NULL),
                                                         default=None, nullable=True)
