from pydantic import BaseModel, ConfigDict
from enum import StrEnum
from datetime import datetime


class Subscription(BaseModel):
    title: str
    price: float
    durability: int


class SubscriptionOut(Subscription):
    is_shown: bool
    model_config = ConfigDict(from_attributes=True)


class SubscriptionRights(StrEnum):
    base: str = "Стандартная"
    extended: str = "Расширенная"


class UserSubscriptionBase(BaseModel):
    user_id: int
    subscription_id: int
    rights: SubscriptionRights


class UserSubscriptionCreate(UserSubscriptionBase):
    pass


class UserSubscriptionOut(UserSubscriptionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
