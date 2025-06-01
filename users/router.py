from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from users.schemas import UserCreate, UserOut, UserLogin
from users.services import UserService, get_user_service
from users.auth import set_tokens
from exceptions.exceptions import PasswordNotMatchException
from exceptions.http import handle_exceptions


router = APIRouter()


@router.post("/register/")
async def register_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserOut:
    new_user = await service.create_user(user=user_in)
    return new_user


@router.post("/login/")
async def login_user(
    response: Response,
    user_in: UserLogin,
    service: UserService = Depends(get_user_service),
):
    user = await service.authentificate_user(
        email=user_in.email, password=user_in.password
    )
    if not user:
        return PasswordNotMatchException
    set_tokens(response, user_id=user.id)
    return {"ok": True, "message": "You are logged in"}


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"ok": True, "message": "You are logged out"}


@router.get("/me/")
async def get_me(
    request: Request,
    service: UserService = Depends(get_user_service),
):
    try:
        user = await service.get_current_user(token=request.cookies.get("access_token"))
        return user
    except Exception as e:
        handle_exceptions(e)


@router.post("/refresh/")
async def process_refresh_token(
    request: Request,
    response: Response,
    service: UserService = Depends(get_user_service),
):
    try:
        user = await service.check_refresh_token(
            token=request.cookies.get("refresh_token")
        )
        set_tokens(response, user_id=user.id)
        return {"ok": True, "message": "You are logged in"}
    except Exception as e:
        handle_exceptions(e)
