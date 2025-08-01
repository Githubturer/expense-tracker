from pydantic import BaseModel, Field, field_validator, ValidationInfo
from app.constants import TransactionCategory, TransactionType, SortOrder, SortBy
from datetime import datetime, date
from uuid import UUID
from typing import Optional

class TransactionBase(BaseModel):
    amount: float
    description: str
    date: datetime
    transaction_type: TransactionType
    transaction_category: TransactionCategory
    category_id: UUID

class TransactionInternal(TransactionBase):
    user_id: UUID
    household_id: UUID

class TransactionCreate(TransactionBase):
    currency_id: Optional[UUID] = Field(default=UUID("22222222-2222-2222-2222-222222222222"))

class TransactionRead(TransactionBase):
    id: UUID

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None

class TransactionDelete(BaseModel):
    id: UUID

class TransactionList(BaseModel):
    transactions: list[TransactionRead]

class TransactionQueryParams(BaseModel):
    # Sortiranje
    sort_by: SortBy = Field(default=SortBy.DATE, description="Field to sort by")
    sort_order: SortOrder = Field(default=SortOrder.DESC, description="Sort order")
    
    # Filtriranje
    transaction_type: Optional[TransactionType] = Field(None, description="Filter by income or expense")
    transaction_category: Optional[TransactionCategory] = Field(None, description="Filter by category")
    category_id: Optional[UUID] = Field(None, description="Filter by category")
    date_from: Optional[date] = Field(None, description="Start date for filtering (YYYY-MM-DD)")
    date_to: Optional[date] = Field(None, description="End date for filtering (YYYY-MM-DD)")
    
    # Paginacija
    limit: int = Field(100, ge=1, le=1000, description="Maximum number of results")
    offset: int = Field(0, ge=0, description="Number of results to skip")
    
    @field_validator('date_to')
    def validate_date_range(cls, v: Optional[date], info: ValidationInfo) -> Optional[date]:
        date_from = info.data.get('date_from')
        if v and date_from and v < date_from:
            raise ValueError('date_to must be after date_from')
        return v
