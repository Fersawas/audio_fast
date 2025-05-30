from datetime import datetime, timedelta
from enum import StrEnum

from sqlalchemy import Integer, DateTime, String, Float, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import ENUM, JSONB


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower() + "s"


class User(Base):
    username: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(20), unique=True)

    is_active: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_super_admin: Mapped[bool] = mapped_column(default=False)

    user_subscription: Mapped["UserSubscription"] = relationship(
        "UserSubscription", back_populates="user", uselist=False, lazy="joined"
    )
    audio_files: Mapped[list["AudioFile"]] = relationship(
        "AudioFile",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class SubscriptionRights(StrEnum):
    base: str = "Стандартная"
    extended: str = "Расширенная"

    @classmethod
    def list(cls):
        return [e.value for e in cls]


class Subscription(Base):
    title: Mapped[str] = mapped_column(String(150))
    price: Mapped[float] = mapped_column(Float, default=0.0)
    is_shown: Mapped[bool] = mapped_column(default=False)
    durability: Mapped[int] = mapped_column(Integer, default=0)


class UserSubscription(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"))
    is_active: Mapped[bool] = mapped_column(default=False)
    rights: Mapped[SubscriptionRights] = mapped_column(
        ENUM(SubscriptionRights, name="subscription_right", create_type=True),
        default=SubscriptionRights.base,
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="user_subscription", uselist=False
    )
    subscription: Mapped["Subscription"] = relationship("Subscription")

    @hybrid_property
    def end_date(self):
        return self.created_at + timedelta(days=self.subscription.durability)

    @hybrid_property
    def days_left(self):
        delta = self.end_date - datetime.now()
        return max(delta.days, 0)


class AudioFile(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(150))
    file_size: Mapped[int] = mapped_column(Integer, default=0)

    audio_result: Mapped["AudioResult"] = relationship(
        "AudioResult", back_populates="audio_file", uselist=False
    )
    user: Mapped["User"] = relationship("User", back_populates="audio_files")


class AudioResultStatus(StrEnum):
    on_process: str = "В обработке"
    ready: str = "Готово"
    error: str = "Ошибка"

    @classmethod
    def list(cls):
        return [e.value for e in cls]


class AudioResult(Base):
    audio_file_id: Mapped[int] = mapped_column(ForeignKey("audiofiles.id"))
    transcription: Mapped[JSONB] = mapped_column(JSONB)
    status: Mapped[AudioResultStatus] = mapped_column(
        ENUM(AudioResultStatus, name="audio_result_status", create_type=True),
        default=AudioResultStatus.on_process,
    )

    audio_file: Mapped["AudioFile"] = relationship(
        "AudioFile", back_populates="audio_result", uselist=False
    )
