from app.models.household import HouseholdBase
from app.models.user import UserBase
from app.constants import UserRole
from app.schemas.user import UserRead
from uuid import UUID
from typing import Optional


class HouseholdCreate(HouseholdBase, UserBase):
    role: UserRole = UserRole.ADMIN
    household_id: Optional[UUID] = (
        None  # inheritance nam trazi household_id, pa je optional
    )


class HouseholdRead(HouseholdBase):
    id: UUID
    users: list[UserRead]
