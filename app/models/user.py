from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List
from pydantic import EmailStr
from app.constants import UserRole
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP

if TYPE_CHECKING:
    from . import Household, Transaction, BudgetGoal, Category, RefreshToken


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    password: str = Field(max_length=255)
    age: int = Field(ge=0, le=120)
    role: UserRole = Field(default=UserRole.USER)
    household_id: UUID = Field(foreign_key="household.id", ondelete="CASCADE")
    is_verified: bool = Field(default=False)


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(TIMESTAMP(timezone=True)))
    updated_at: datetime = Field(default_factory=datetime.now)

    household: "Household" = Relationship(back_populates="users")
    transactions: List["Transaction"] = Relationship(back_populates="user")
    budget_goals: List["BudgetGoal"] = Relationship(back_populates="user")
    categories: List["Category"] = Relationship(back_populates="user")
    refresh_tokens: List["RefreshToken"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.first_name} {self.last_name})>"
