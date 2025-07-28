from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Category, Transaction, User, BudgetGoal


class HouseholdBase(SQLModel):
    name: str = Field(max_length=255)
    country: str = Field(max_length=90)
    city: str = Field(max_length=189)
    address: str = Field(max_length=255)
    zip_code: str = Field(max_length=18)


class Household(HouseholdBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    categories: list["Category"] = Relationship(back_populates="household")
    transactions: list["Transaction"] = Relationship(back_populates="household")
    users: list["User"] = Relationship(back_populates="household")
    budget_goals: list["BudgetGoal"] = Relationship(back_populates="household")

    def __repr__(self) -> str:
        return f"<Household(id={self.id}, name={self.name})>"
