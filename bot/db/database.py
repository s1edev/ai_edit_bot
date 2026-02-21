from typing import AsyncGenerator
from pathlib import Path

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from db.models import Base

# Ensure data directory exists
DATA_DIR = Path(__file__).parent.parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# SQLite URL для async драйвера
DATABASE_URL = f"sqlite+aiosqlite:///{DATA_DIR / 'bot.db'}"


async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def init_db() -> None:
    """Инициализация базы данных - создание таблиц."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Закрытие подключения к БД."""
    await async_engine.dispose()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Получить async сессию для работы с БД."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
