from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from . import Household, Transaction, BudgetGoal


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserBase(SQLModel):
    name: str = Field(max_length=255)
    surname: str = Field(max_length=255)
    password: str = Field(max_length=255)
    age: int = Field(ge=0, le=120)
    role: UserRole = Field(default=UserRole.USER)
    household_id: UUID = Field(foreign_key="household.id")


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    household: "Household" = Relationship(back_populates="users", sa_relationship_kwargs={"cascade": "all, delete"})
    transactions: List["Transaction"] = Relationship(back_populates="user")
    budget_goals: List["BudgetGoal"] = Relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name})>"
