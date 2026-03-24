from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends

from app.adapters.db.repositories.user_repository import UsersDB
from app.api.deps import get_aiograpi_adapter, get_llm_adapter, get_users_db
from app.api.dto import InstagramMessageIn
from app.domain.message_handler import handle_message
from app.domain.models import InstagramMessage
from app.ports.instagram_port import InstagramPort
from app.ports.llm_port import LLMPort

type DBDep = Annotated[UsersDB, Depends(get_users_db)]
type LLMDep = Annotated[LLMPort, Depends(get_llm_adapter)]
type InstagramDep = Annotated[InstagramPort, Depends(get_aiograpi_adapter)]


router = APIRouter()


@router.post("")
async def process_message(
    data: InstagramMessageIn,
    background_tasks: BackgroundTasks,
    db: DBDep,
    llm: LLMDep,
    instagram: InstagramDep,
):
    message = data.model_dump(exclude={"action_params", "category", "chatbot_id"})
    background_tasks.add_task(
        handle_message, InstagramMessage(**message), db, llm, instagram
    )
    return {"message": "Notification sent to bot in background."}
