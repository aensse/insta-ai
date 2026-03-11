from typing import Any, Protocol


class LLMPort(Protocol):
    async def get_ai_response(self, thread: list[Any]) -> Any: ...
