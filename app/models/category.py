from sqlmodel import SQLModel, Field, Relationship
from app.constants import TransactionCategory
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from . import User, Household, Transaction, BudgetGoal

class CategoryBase(SQLModel):
    name: str
    description: str
    category_type: TransactionCategory
    household_id: Optional[UUID] = Field(default=None, foreign_key="household.id", ondelete="CASCADE", nullable=True)
    parent_id: Optional[UUID] = Field(default=None, foreign_key="category.id", ondelete="CASCADE", nullable=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id", ondelete="SET NULL", nullable=True)


class Category(CategoryBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: datetime | None = Field(default=None)

    parent: Optional["Category"] = Relationship(back_populates="subcategories", sa_relationship_kwargs={'remote_side': 'Category.id'})
    subcategories: list["Category"] = Relationship(back_populates="parent")

    #since users will be able to create custom categories, creating a custom join condition to get only non-deleted categories.
    #still will enable us to delete but audit the deleted categories and their transactions.
    user: Optional["User"] = Relationship(back_populates="categories", sa_relationship_kwargs={"primaryjoin": "Category.user_id == User.id and deleted_at is None"})
    household: Optional["Household"] = Relationship(back_populates="categories", sa_relationship_kwargs={"primaryjoin": "Category.household_id == Household.id and deleted_at is None"})
    transactions: list["Transaction"] = Relationship(back_populates="category")
    budget_goals: list["BudgetGoal"] = Relationship(back_populates="category")
