from uuid import UUID
from pydantic import BaseModel, EmailStr
from app.constants import UserRole
from typing import Optional


class UserBaseInfo(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    age: int


class UserBaseInternal(UserBaseInfo):
    role: UserRole


class UserCreate(UserBaseInfo):
    household_id: Optional[UUID] = None  # dobiva se iz JWT tokena
    password: str


class UserRead(UserBaseInternal):
    id: UUID
    household_id: UUID


class UserUpdate(BaseModel):
    id: Optional[UUID] = None  # dobiva se iz JWT tokena
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserBalance(BaseModel):
    balance: float
    income_current_month: float
    spending_current_month: float
