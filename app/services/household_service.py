from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas import HouseholdCreate
from app.models.household import Household
from app.repositories import HouseholdRepository, UserRepository
from app.exceptions import DuplicateEmailError
from app.models import User
from app.core import hash_password
from uuid import UUID


class HouseholdService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.household_repo = HouseholdRepository(session)

    async def create_household_and_admin(
        self, household_data: HouseholdCreate
    ) -> Household:
        """Create household and admin user, send verification email"""
        user_repo = UserRepository(self.session)
        user_exists = await user_repo.get_user_by_email(household_data.email)
        if user_exists:
            raise DuplicateEmailError(household_data.email)
        household = await self.household_repo.create_household(household_data)
        household_data.household_id = household.id
        household_data.password = hash_password(household_data.password)
        await user_repo.create_user(
            User(
                **household_data.model_dump(),
            ),
        )
        await self.session.commit()
        household_and_admin = await self.get_household_by_id(
            household.id, include_users=True
        )

        return household_and_admin

    async def get_household_by_id(
        self, household_id: UUID, include_users: bool = False
    ) -> Household:
        return await self.household_repo.get_household_by_id(
            household_id, include_users
        )
