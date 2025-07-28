from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from . import Household


class CurrencyBase(SQLModel):
    name: str = Field(max_length=30)
    symbol: str = Field(max_length=3)
    code: str = Field(max_length=3)
    rate: float = Field(ge=0)


class Currency(CurrencyBase, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    household: "Household" = Relationship(back_populates="currencies")
