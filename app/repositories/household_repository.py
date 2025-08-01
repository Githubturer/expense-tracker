from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.household import Household, HouseholdBase
from sqlmodel import select
from sqlalchemy.orm import selectinload
from uuid import UUID


class HouseholdRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_household(self, household_in: HouseholdBase) -> Household:
        """
        NOTE: Does not commit, because it is used in a service layer.
        """
        db_household = Household.model_validate(household_in)

        self.session.add(db_household)

        return db_household

    async def get_household_by_id(
        self, household_id: UUID, include_users: bool = False
    ) -> Household:
        statement = select(Household).where(Household.id == household_id)
        if include_users:
            statement = statement.options(selectinload(Household.users))
        result = await self.session.exec(statement)
        return result.first()

    async def delete_household(self, household: Household) -> None:
        await self.session.delete(household)
        await self.session.commit()
