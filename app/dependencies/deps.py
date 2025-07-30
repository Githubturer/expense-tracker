from app.core import async_session
from sqlmodel.ext.asyncio.session import AsyncSession
from collections.abc import AsyncGenerator

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


