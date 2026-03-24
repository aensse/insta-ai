from dataclasses import dataclass
from typing import Literal


@dataclass
class InstagramMessage:
    message: str
    thread_id: str
    sender_id: int
    sender_username: str


@dataclass
class InstagramThread:
    is_sent_by_viewer: bool
    text: str | None


@dataclass
class LLMResponse:
    message: str
    status: Literal["active", "blocked"]
