from app.repositories import UserRepository, HouseholdRepository
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas import UserCreate, UserUpdate
from app.models import User
from app.exceptions.exceptions import DuplicateEmailError, UserNotFoundError
from app.core import hash_password
from app.constants import UserRole
from uuid import UUID


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)
        self.session = session

    async def create_user(self, user_data: UserCreate) -> User:
        # Dodati provjeru za admin role za kreiranje usera.
        user_exists = await self.user_repo.get_user_by_email(user_data.email)
        if user_exists:
            raise DuplicateEmailError(user_data.email)
        user_data.password = hash_password(user_data.password)
        user = await self.user_repo.create_user(user_data)
        await self.session.commit()
        return user

    async def update_user(self, user_data: UserUpdate) -> User:
        """Kasnije se može dodati još neki atribut za update, kao npr mjenjanje iz korisnika u admina"""
        user = await self.user_repo.get_user_by_id(user_data.id)
        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        user = await self.user_repo.update_user(user)
        return user

    async def delete_user(self, id: UUID) -> None:
        """Za jednostavnost koristimo isti endpoint za brisanje korisnika i admina i cijelog kućanstva.
        Inace bi trebalo napraviti endpoint za brisanje korisnika i admina, ako hoćemo pratiti Restful princip."""
        user = await self.user_repo.get_user_by_id(id)
        if not user:
            raise UserNotFoundError
        if user.role == UserRole.ADMIN:
            household_repo = HouseholdRepository(self.session)
            household = await household_repo.get_household_by_id(user.household_id)
            await household_repo.delete_household(household)
        else:
            await self.user_repo.delete_user(user)
