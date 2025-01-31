from datetime import datetime
from typing import Any

from sqlalchemy import BIGINT, VARCHAR, JSON, DateTime, ForeignKey
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
    date_create: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    title: Mapped[str] = mapped_column(VARCHAR, nullable=False)


class WordCardOrm(Base):
    __tablename__ = 'word_card'
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    date_create: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    group_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('card_group.id', ondelete=CASCADE), nullable=False)
    word: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    transcription: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    translations: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    pos: Mapped[list[str]] = mapped_column(JSON, nullable=False)
