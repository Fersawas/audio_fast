from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from users.schemas import UserCreate, UserOut
from users.services import UserService, get_user_service


router = APIRouter()


@router.post("/register/")
async def register_user(
    user_in: UserCreate, service: UserService = Depends(get_user_service)
) -> UserOut:
    new_user = await service.create_user(user=user_in)
    return new_user
