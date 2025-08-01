from app.core import async_session
from sqlmodel.ext.asyncio.session import AsyncSession
from collections.abc import AsyncGenerator
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.security import verify_token, TokenType
from app.models.user import User

bearer = HTTPBearer()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_current_user(
    authorization: HTTPAuthorizationCredentials = Security(bearer),
) -> User:
    token = authorization.credentials
    payload = verify_token(token, TokenType.ACCESS)
    return payload
