from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator


class ActionParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    thread_id: Annotated[str, Field(alias="id")]


class InstagramMessageIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    message: Annotated[str, Field(min_length=2, max_length=5000)]
    action_params: ActionParams
    category: Annotated[str, Field(alias="pushCategory")]

    sender_id: Annotated[int, Field(alias="sourceUserId")]
    chatbot_id: Annotated[int, Field(alias="intendedRecipientUserId")]

    sender_username: Annotated[str, Field(min_length=2, max_length=100)]

    @model_validator(mode="before")
    @classmethod
    def check_if_message_as_expected(cls, data: dict) -> dict:
        if "message" in data:
            expected_parts = 2
            parts = data.get("message").split(":", 1)
            if len(parts) < expected_parts:
                raise ValueError("Invalid message format")
            data["sender_username"] = parts[0]
            data["message"] = parts[1].replace(" ", "", 1)
        return data

    @computed_field
    @property
    def thread_id(self) -> str:
        return self.action_params.thread_id
