from fastapi import Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError, ExpiredSignatureError

from users.dependencies import get_access_token

from subscriptions.schemas import SubscriptionOut, UserSubscriptionOut
from subscriptions.repository import SubscriptionRepository
from database.db_helper import get_db_session


def get_subscription_service(session: AsyncSession = Depends(get_db_session)):
    repo = SubscriptionRepository(session)
    return SubscriptionService(repo)


class SubscriptionService:
    def __init__(self, repository: SubscriptionRepository):
        self.repo = repository

    async def get_subscription(self, subscription_id) -> SubscriptionOut:
        subscription = await self.repo.get_subscription(subscription_id=subscription_id)
        return SubscriptionOut.model_validate(subscription)

    async def get_subscriptions(self) -> List[SubscriptionOut]:
        subscriptions = await self.repo.get_subscriptions()
        subscriptions = [
            SubscriptionOut.model_validate(subscription)
            for subscription in subscriptions
        ]
        return subscriptions

    async def get_user_subscription(self, user_id) -> UserSubscriptionOut:
        user_subscriptions = await self.repo.get_user_subscription(user_id)
        return UserSubscriptionOut.model_validate(user_subscriptions)

    async def create_user_subscription(
        self, user_id, subscription_id, rights
    ) -> UserSubscriptionOut:
        user_subscription = await self.repo.create_user_subscription(
            user_id, subscription_id, rights
        )
        return UserSubscriptionOut.model_validate(user_subscription)
