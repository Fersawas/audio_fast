from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError, ExpiredSignatureError

from pydantic import EmailStr

from users.dependencies import get_access_token, get_refresh_token

from users.schemas import UserCreate, UserOut
from users.repository import UserRepository
from database.db_helper import get_db_session
from exceptions.exceptions import UserExistsException
from core.config import get_auth_data
from users.auth import verify_password
from exceptions.exceptions import (
    UserNotFoundException,
    ExpitedTokenException,
    JWTException,
)


def get_user_service(session: AsyncSession = Depends(get_db_session)):
    repo = UserRepository(session)
    return UserService(repo)


class UserService:
    def __init__(self, repository: UserRepository):
        self.repo = repository

    async def create_user(self, user: UserCreate) -> UserOut:
        existing_user = await self.repo.get_user_by_email(email=user.email)
        if existing_user:
            raise UserExistsException
        new_user = await self.repo.create_user(user=user)
        return UserOut.model_validate(new_user)

    async def check_refresh_token(
        self,
        token: str = Depends(get_refresh_token),
    ):
        try:
            payload = jwt.decode(
                token,
                get_auth_data().get("secret_key"),
                algorithms=[get_auth_data().get("algorithm")],
            )
            user_id = payload.get("sub")
            if not user_id:
                raise UserNotFoundException
            user = await self.repo.get_user(user_id=user_id)
            if not user:
                raise UserNotFoundException
            return user
        except JWTError:
            raise JWTException

    async def get_current_user(
        self,
        token: str = Depends(get_access_token),
    ) -> UserOut:
        try:
            if not token:
                raise JWTException
            payload = jwt.decode(
                token,
                get_auth_data().get("secret_key"),
                algorithms=[get_auth_data().get("algorithm")],
            )
            user_id = payload.get("sub")
            print("here")
        except ExpiredSignatureError:
            raise ExpitedTokenException
        except JWTError:
            raise JWTException

        user = await self.repo.get_user(user_id=user_id)
        if not user:
            raise UserNotFoundException
        return UserOut.model_validate(user)

    async def authentificate_user(self, email: EmailStr, password: str) -> UserOut:
        user = await self.repo.get_user_by_email(email=email)
        if not user or verify_password(password, user.password) is False:
            return None
        return UserOut.model_validate(user)
