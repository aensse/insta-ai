from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.adapters.db.session import Base, engine
from app.adapters.external.instagram.aiograpi_adapter import AiograpiAdapter
from app.adapters.external.instagram.aiograpi_client_factory import create_client
from app.api import message
from app.core.config import settings
from app.core.logger import setup_logging

setup_logging()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    cl = await create_client(
        settings.ig_session_file, settings.username, settings.password, settings.secret
    )
    _app.state.aiograpi = AiograpiAdapter(cl)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(message.router, prefix="/api/v1/messages")
