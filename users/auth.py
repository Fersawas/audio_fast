from fastapi import Response

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from core.config import get_auth_data


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def get_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    auth_data = get_auth_data()
    access_payload = data.copy()
    access_expire = datetime.now() + timedelta(
        days=int(get_auth_data("ACCESS_TOKEN_EXPIRE_DAYS"))
    )
    access_payload.update({"exp": access_expire})
    access_jwt = jwt.encode(
        access_payload, auth_data["secret_key"], algorithm=auth_data["algorithm"]
    )

    refresh_payload = data.copy()
    refresh_expire = datetime.now() + timedelta(
        days=int(get_auth_data("REFRESH_TOKEN_EXPIRE_DAYS"))
    )
    refresh_payload.update({"exp": refresh_expire})
    refresh_jwt = jwt.encode(
        refresh_payload, auth_data["secret_key"], algorithm=auth_data["algorithm"]
    )
    return {"access_token": access_jwt, "refresh_token": refresh_jwt}


def set_tokens(response: Response, user_id: int):
    tokens = create_access_token({"sub": user_id})
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=True,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=True,
    )
