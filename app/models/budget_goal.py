from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone
from app.constants import BudgetPeriod
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP

if TYPE_CHECKING:
    from . import Household, User, Category


class BudgetGoalBase(SQLModel):
    name: str
    description: Optional[str] = None
    amount: float
    period: BudgetPeriod
    start_date: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True)))
    end_date: Optional[datetime] = None
    household_id: UUID = Field(
        foreign_key="household.id", ondelete="CASCADE", nullable=False
    )
    # pratimo tko je stvorio budzet, omogućava auditiranje budžeta.
    user_id: UUID = Field(foreign_key="user.id", ondelete="SET NULL", nullable=True)
    category_id: UUID = Field(
        foreign_key="category.id", ondelete="CASCADE", nullable=False
    )


class BudgetGoal(BudgetGoalBase, table=True):
    __tablename__ = "budget_goal"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(TIMESTAMP(timezone=True)))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(TIMESTAMP(timezone=True)))

    household: "Household" = Relationship(back_populates="budget_goals")
    user: "User" = Relationship(back_populates="budget_goals")
    category: "Category" = Relationship(back_populates="budget_goals")
