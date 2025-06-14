from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from subscriptions.schemas import SubscriptionOut, UserSubscriptionOut
from database.models import User, Subscription, UserSubscription, SubscriptionRights
from exceptions.exceptions import DataBaseException


class SubscriptionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_subscription(self, subscription_id) -> Subscription:
        try:
            result = await self.session.execute(
                select(Subscription).where(Subscription.id == subscription_id)
            )
            subscription = result.scalar_one_or_none()
            if not subscription:
                return None
            return subscription
        except SQLAlchemyError as e:
            raise DataBaseException

    async def get_subscriptions(self) -> List[Subscription]:
        try:
            result = await self.session.execute(
                select(Subscription).where(Subscription.is_shown == True)
            )
            subscriptons = result.scalars().all()
            if not subscriptons:
                return None
            return subscriptons
        except SQLAlchemyError as e:
            raise DataBaseException

    async def get_user_subscription(self, user_id) -> UserSubscription:
        try:
            result = await self.session.execute(
                select(UserSubscription).where(UserSubscription.user_id == user_id)
            )
            user_subscription = result.scalar_one_or_none()
            if not user_subscription:
                return None
            return user_subscription
        except SQLAlchemyError as e:
            raise DataBaseException

    async def create_user_subscription(
        self, user_id, subscription_id, rights
    ) -> UserSubscription:
        try:
            subscription = await self.get_subscription(subscription_id=subscription_id)
            user_subscription = UserSubscription(
                user_id=user_id,
                subscription_id=subscription.id,
                rights=rights if rights else SubscriptionRights.base,
                is_active=True,
            )
            self.session.add(user_subscription)
            await self.session.commit()
            await self.session.refresh(user_subscription)
            return user_subscription
        except SQLAlchemyError as e:
            raise DataBaseException
