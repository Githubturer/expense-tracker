from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app.constants import TransactionType, TransactionCategory
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from . import Household, User, Currency, Category


class TransactionBase(SQLModel):
    amount: float
    description: str
    date: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True)))
    transaction_type: TransactionType
    transaction_category: TransactionCategory
    split_group_id: UUID | None = Field(
        default=None
    )  # Sluzi za razdjeljene transakcije unutar iste transakcije. [Više cimera plaća jednu stanarinu]
    transfer_group_id: UUID | None = Field(
        default=None
    )  # Sluzi za unutarnje transfer transakcije između korisnika u istoj kućanstvu. [Roditelj daje djetetu dnevni/tjedni/mjesecni dzeparac]
    reccuring_group_id: UUID | None = Field(
        default=None
    )  # Sluzi za rekurzivne transakcije. [Mjesecna stanarina]

    household_id: UUID = Field(
        default=None, foreign_key="household.id", ondelete="CASCADE", nullable=False
    )
    # iako se korisnik moze izbrisati, transakcija ce biti spremljena u bazi. Omogucuje auditiranje transakcija.
    user_id: UUID | None = Field(
        default=None, foreign_key="user.id", ondelete="SET NULL", nullable=True
    )
    category_id: UUID = Field(default=None, foreign_key="category.id", nullable=False)
    currency_id: UUID = Field(default=None, foreign_key="currency.id", nullable=True)


class Transaction(TransactionBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(TIMESTAMP(timezone=True)))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(TIMESTAMP(timezone=True)))

    household: "Household" = Relationship(back_populates="transactions")
    user: Optional["User"] = Relationship(back_populates="transactions")
    currency: "Currency" = Relationship(back_populates="transactions")
    category: "Category" = Relationship(back_populates="transactions")
