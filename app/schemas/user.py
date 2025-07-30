from app.models.user import UserBase
from uuid import UUID
from pydantic import BaseModel, EmailStr
from app.constants import UserRole
from typing import Optional

class UserBaseInfo(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    age: int
    role: UserRole

class UserCreate(UserBase):
    household_id: Optional[UUID] = None

class UserRead(UserBaseInfo):
    id: UUID
    household_id: UUID
