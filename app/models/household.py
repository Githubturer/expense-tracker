from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP

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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(TIMESTAMP(timezone=True)))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(TIMESTAMP(timezone=True)))

    categories: list["Category"] = Relationship(
        back_populates="household",
        sa_relationship_kwargs={"cascade": "all, delete", "passive_deletes": True},
    )
    transactions: list["Transaction"] = Relationship(
        back_populates="household",
        sa_relationship_kwargs={"cascade": "all, delete", "passive_deletes": True},
    )
    users: list["User"] = Relationship(
        back_populates="household",
        sa_relationship_kwargs={"cascade": "all, delete", "passive_deletes": True},
    )
    budget_goals: list["BudgetGoal"] = Relationship(
        back_populates="household",
        sa_relationship_kwargs={"cascade": "all, delete", "passive_deletes": True},
    )

    def __repr__(self) -> str:
        return f"<Household(id={self.id}, name={self.name})>"
