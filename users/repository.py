from typing import List

from sqlalchemy.orm import Session

from users.schemas import UserCreate, UserOut, UserBase, UserUpdate
from database.models import User
from users.auth import get_password, verify_password


class UserRepository:
    def __init__(self, session: Session) -> User | None:
        self.session = session

    async def create_user(self, user: UserCreate) -> UserOut:
        user.password = get_password(user.password)
        db_user = User(**user.model_dump(exclude_none=True))
        await self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return UserOut.model_validate(db_user)

    async def get_user(self):
        pass
