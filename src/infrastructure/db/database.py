from contextlib import asynccontextmanager
from logging import getLogger

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.shared.config import ASYNC_DATABASE_URL

logger = getLogger(__name__)

engine = create_async_engine(
    url=ASYNC_DATABASE_URL
)
logger.info("Database Engine Initialized")


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
logger.info("Create Async Session Generator")

@asynccontextmanager
async def get_async_db():
    logger.debug("Database Create Session")
    async with AsyncSessionLocal() as session:
        yield session

class Base(DeclarativeBase):
    pass