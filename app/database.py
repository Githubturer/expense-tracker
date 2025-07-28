from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings
from collections.abc import AsyncGenerator
import logging

logger = logging.getLogger(__name__)

engine = create_async_engine(settings.database_url, echo=settings.sql_echo, pool_pre_ping=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# def ensure_database_exists() -> None:
#     """Mainstreamanje kreiranja baze podataka"""
#     parsed_url = up.urlparse(settings.database_url)
#     db_name = parsed_url.path[1:]
#     #konstruiraj sync connection string
#     admin_db_url = f"dbname=postgres user={parsed_url.username} password={parsed_url.password} host={parsed_url.hostname} port={parsed_url.port}"
#     try:
#         conn = psycopg2.connect(admin_db_url)
#         conn.autocommit = True
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
#             exists = cursor.fetchone()
#             if not exists:
#                 logger.info(f"Database '{db_name}' not found. Creating it...")
#                 cursor.execute(f"CREATE DATABASE {db_name};")
#             else:
#                 logger.info(f"Database '{db_name}' already exists.")
#     except Exception as e:
#         logger.error(f"Error checking/creating database: {e}")
#         raise
#     finally:
#         if conn:
#             conn.close()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        
