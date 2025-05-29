from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    phone: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    phone: str | None = None
    password: str | None = None
