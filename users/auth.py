from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from pydantic import EmailStr

from users.repository import UserRepository
from core.config import get_auth_data


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(
        days=int(get_auth_data("ACCESS_TOKEN_EXPIRE_DAYS"))
    )
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(
        to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"]
    )
    return encode_jwt


async def authentificate_user(email: EmailStr, password: str):
    user = await UserRepository.get_user(email=email)
    if not user or verify_password(password, user.password) is False:
        return None
    return user
