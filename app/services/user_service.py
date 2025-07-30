from app.repositories import UserRepository
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas import UserCreate
from app.models import User
from app.exceptions.exceptions import DuplicateEmailError
from app.core import hash_password

class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)
        self.session = session

    async def create_user(self, user_data: UserCreate) -> User:
        user_exists = await self.user_repo.get_user_by_email(user_data.email)
        if user_exists:
            raise DuplicateEmailError(user_data.email)
        user_data.password = hash_password(user_data.password)
        user = await self.user_repo.create_user(user_data)
        await self.session.commit()
        return user

