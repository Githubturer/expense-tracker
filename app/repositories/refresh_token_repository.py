from app.models import RefreshToken
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

class RefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        self.session.add(refresh_token)
        await self.session.commit()
        await self.session.refresh(refresh_token)
        return refresh_token

    async def revoke_refresh_token(self, refresh_token: RefreshToken) -> None:
        refresh_token.revoked = True
        await self.session.commit()

    async def get_refresh_token_by_token(self, token_hash: str) -> RefreshToken | None:
        statement = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        result = await self.session.exec(statement)
        return result.first()
