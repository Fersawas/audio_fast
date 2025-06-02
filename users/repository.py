from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from users.schemas import UserCreate
from database.models import User
from database.db_helper import get_db_session
from users.auth import get_password, verify_password
from exceptions.exceptions import DataBaseException, UserNotFoundException


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserCreate) -> User:
        try:
            db_user = User(**user.model_dump(exclude_none=True))
            db_user.password = get_password(db_user.password)

            self.session.add(db_user)
            await self.session.flush()
            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            raise DataBaseException

    async def get_user(self, user_id):
        try:
            result = await self.session.execute(
                select(User).where(User.id == int(user_id))
            )
            user = result.scalar_one_or_none()
            if not user:
                return None
            return user
        except SQLAlchemyError as e:
            raise DataBaseException

    async def get_user_by_email(self, email) -> User:
        try:
            result = await self.session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            if not user:
                return None
            return user
        except SQLAlchemyError as e:
            raise DataBaseException

    async def get_users(self) -> List[User]:
        try:
            result = await self.session.execute(
                select(User)  # .where(User.is_active == True)
            )
            users = result.scalars().all()
            return users
        except SQLAlchemyError as e:
            raise DataBaseException

    async def update_user(self, user) -> User:
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except SQLAlchemyError as e:
            raise DataBaseException
