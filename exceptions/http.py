from exceptions.exceptions import (
    UserNotFoundException,
    MainException,
    PasswordNotMatchException,
    JWTException,
    ExpitedTokenException,
)
from fastapi import HTTPException


def handle_exceptions(e: MainException):
    if isinstance(e, UserNotFoundException):
        raise HTTPException(status_code=400, detail="User not found")
    if isinstance(e, PasswordNotMatchException):
        raise HTTPException(status_code=401, detail="Password not match")
    if isinstance(e, JWTException):
        raise HTTPException(status_code=401, detail="Plese log in")
    if isinstance(e, ExpitedTokenException):
        raise HTTPException(status_code=401, detail="Token expired")
