from fastapi import APIRouter, Request, Response, Depends

from subscriptions.schemas import (
    SubscriptionOut,
    UserSubscriptionOut,
    UserSubscriptionCreate,
)
from subscriptions.services import SubscriptionService, get_subscription_service
from users.services import UserService, get_user_service
from exceptions.http import handle_exceptions

router = APIRouter()


@router.get("subscriptions/all")
async def get_all_subscriptions(
    request: Request,
    service: SubscriptionService = Depends(get_subscription_service),
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = await user_service.get_current_user(
            token=request.cookies.get("access_token")
        )
        subscriptions = await service.get_subscriptions(user_id=user.id)
        return subscriptions
    except Exception as e:
        handle_exceptions(e)


@router.get("subscriptions/{subscription_id}")
async def get_subscription(
    request: Request,
    subscription_id: int,
    service: SubscriptionService = Depends(get_subscription_service),
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = await user_service.get_current_user(
            token=request.cookies.get("access_token")
        )
        subscription = await service.get_subscription(
            user_id=user.id, subscription_id=subscription_id
        )
        return subscription
    except Exception as e:
        handle_exceptions(e)


@router.post("subscriptions/my_subscription")
async def get_user_subsctiption(
    request: Request,
    new_subscription: UserSubscriptionCreate,
    service: SubscriptionService = Depends(get_subscription_service),
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = await user_service.get_current_user(
            token=request.cookies.get("access_token")
        )
        subscription = await service.get_subscription(
            subscription_id=new_subscription.subscription_id
        )
        new_subscription = await service.create_user_subscription(
            user_id=user.id,
            subscription_id=subscription.id,
            rights=new_subscription.rights,
        )
        return new_subscription
    except Exception as e:
        handle_exceptions(e)
