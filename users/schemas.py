import re

from pydantic import BaseModel, ConfigDict, field_validator, ValidationError
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    phone: str


class UserCreate(UserBase):
    password: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str):
        pattern = r"7\d{10}$"
        value = "".join([char for char in value if char.isdigit()])
        if len(value) < 10:
            raise ValueError()
        value = "7" + value[1:]
        clean_phone = re.search(pattern, value)
        if not clean_phone:
            raise ValueError()
        return clean_phone.group()


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class UserOutPrivate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    id: int


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    phone: str | None = None
    password: str | None = None


class UserLogin(BaseModel):
    email: str
    password: str


class PasswordUpdate(BaseModel):
    new_password: str
    old_password: str
