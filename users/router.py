from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from users.schemas import UserCreate, UserOut, UserLogin, UserUpdate, PasswordUpdate
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
    try:
        user = await service.authentificate_user(
            email=user_in.email, password=user_in.password
        )
        set_tokens(response, user_id=user.id)
        return {"ok": True, "message": "You are logged in"}
    except Exception as e:
        handle_exceptions(e)


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


@router.get("/users/")
async def get_users(
    request: Request,
    service: UserService = Depends(get_user_service),
):
    try:
        await service.get_current_user(token=request.cookies.get("access_token"))
        users = await service.get_users()
        return users
    except Exception as e:
        handle_exceptions(e)


@router.patch("/update_me")
async def update_user(
    request: Request, data: UserUpdate, service: UserService = Depends(get_user_service)
):
    try:
        user = await service.get_current_user(token=request.cookies.get("access_token"))
        updated_data = data.model_dump(exclude_none=True)
        updated_user = await service.update_user(user.id, updated_data)
        return updated_user
    except Exception as e:
        handle_exceptions(e)


@router.patch("/change_password/")
async def update_password(
    request: Request,
    data: PasswordUpdate,
    service: UserService = Depends(get_user_service),
):
    try:
        user = await service.get_current_user(token=request.cookies.get("access_token"))
        updated_data = data.model_dump(exclude_none=True)
        user = await service.update_password(user.id, updated_data)
        return user
    except Exception as e:
        handle_exceptions(e)
