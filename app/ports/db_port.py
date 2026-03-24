from typing import Protocol

from app.domain.models import InstagramMessage


class UsersDBPort(Protocol):
    async def get_user_status_by_user_id(self, user_id: int) -> str | None: ...

    async def add_user(self, message: InstagramMessage) -> None: ...

    async def update_user_status(self, user_id: int, new_status: str) -> None: ...
