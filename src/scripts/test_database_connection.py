# ./src/scripts/test_database_connection.py
import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from ..app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_database_connection():
    # Using settings to build the DATABASE_URL
    DATABASE_URL = f"{settings.POSTGRES_ASYNC_PREFIX}{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"
    # DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost/postgres"

    print(f"DATABASE_URL: {DATABASE_URL}")

    # Create the Async Engine
    engine = create_async_engine(DATABASE_URL, echo=True)

    # Create a sessionmaker
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Begin a new session and try a simple SELECT query
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(text("SELECT 1"))
            print(result.scalar())
            logger.info("Database connection test succeeded.")

    # Dispose the engine
    await engine.dispose()


async def main():
    await test_database_connection()


if __name__ == "__main__":
    asyncio.run(main())
