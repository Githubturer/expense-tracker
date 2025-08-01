from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.user import UserCreate
from app.models.user import User
from sqlmodel import select
from uuid import UUID
from pydantic import EmailStr
import logging

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserCreate) -> User:
        db_user = User(
            **user.model_dump(),
        )
        self.session.add(db_user)
        return db_user

    async def get_user_by_id(self, user_id: UUID) -> User:
        return await self.session.get(User, user_id)

    async def get_user_by_email(self, email: EmailStr) -> User:
        statement = select(User).where(User.email == email)
        result = await self.session.exec(statement)
        return result.first()

    async def update_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()
