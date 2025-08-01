from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core import settings
import logging

logger = logging.getLogger(__name__)

engine = create_async_engine(
    settings.database_url, echo=settings.sql_echo, pool_pre_ping=True
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
