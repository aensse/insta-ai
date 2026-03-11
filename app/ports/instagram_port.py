from typing import Any, Protocol


class InstagramPort(Protocol):
    async def get_thread(self, thread_id: int) -> list[Any]: ...

    async def send_message(self, bot_message: str, thread_id: int) -> None: ...

