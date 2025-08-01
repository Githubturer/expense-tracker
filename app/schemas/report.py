from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.constants import ReportPeriod


# Response Models
class CategorySpending(BaseModel):
    category_id: UUID
    category_name: str
    total_amount: float
    transaction_count: int
    percentage_of_total: float


class DaySpending(BaseModel):
    date: date
    total_amount: float
    transaction_count: int


class TransactionSummary(BaseModel):
    transaction_id: UUID
    amount: float
    description: str
    date: datetime
    category_name: str


class TransactionReport(BaseModel):
    # Period info
    period: ReportPeriod
    date_from: date
    date_to: date

    # Summary statistics
    total_income: float
    total_expenses: float
    net_amount: float
    income_transaction_count: int
    expense_transaction_count: int
    total_transaction_count: int

    # Top transactions
    biggest_income: Optional[TransactionSummary]
    biggest_expense: Optional[TransactionSummary]

    # Day analysis
    highest_spending_day: Optional[DaySpending]
    most_transactions_day: Optional[DaySpending]

    # Category breakdown
    spending_per_category: list[CategorySpending]

    # Daily/weekly/monthly trends (optional)
    daily_trends: Optional[list[DaySpending]] = None


# Query Parameters
class ReportQueryParams(BaseModel):
    period: ReportPeriod = Field(ReportPeriod.MONTHLY, description="Report period")
    date_from: Optional[date] = Field(
        None, description="Custom start date (required if period=custom)"
    )
    date_to: Optional[date] = Field(
        None, description="Custom end date (required if period=custom)"
    )
    include_trends: bool = Field(False, description="Include daily spending trends")
    category_limit: int = Field(
        10, ge=1, le=50, description="Max categories to include"
    )
