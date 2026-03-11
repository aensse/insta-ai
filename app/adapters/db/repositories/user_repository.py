from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import models
from app.domain.models import InstagramMessage


class UsersDB:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def _get_user_by_user_id(self, user_id: int) -> str | models.User:
        stmt = select(models.User).where(models.User.instagram_user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_user_status_by_user_id(self, user_id: int) -> str | None:
        stmt = select(models.User).where(models.User.instagram_user_id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalars().first()
        if user:
            return user.status
        return None

    async def add_user(self, message: InstagramMessage) -> None:
        user = models.User(
            instagram_user_id = message.sender_id,
            instagram_thread_id = message.thread_id,
            name=message.sender_username,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

    async def update_user_status(self, user_id: int, new_status: str) -> None:
        user: models.User = await self._get_user_by_user_id(user_id)
        user.status = new_status
        await self.db.commit()
        await self.db.refresh(user)


