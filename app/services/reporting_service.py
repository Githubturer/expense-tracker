from datetime import date, timedelta
from app.constants import ReportPeriod, TransactionCategory
from app.schemas import (
    TransactionReport,
    ReportQueryParams,
    CategorySpending,
    DaySpending,
    TransactionSummary,
)
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from app.models import Transaction
from app.repositories import TransactionRepository
from uuid import UUID

class ReportingService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.transaction_repo = TransactionRepository(session)

    def _get_date_range(
        self, period: ReportPeriod, date_from: Optional[date], date_to: Optional[date]
    ) -> tuple[date, date]:
        today = date.today()

        if period == ReportPeriod.CUSTOM:
            if not date_from or not date_to:
                raise ValueError("date_from and date_to are required for custom period")
            return date_from, date_to
        elif period == ReportPeriod.WEEKLY:
            start_date = today - timedelta(days=6)
            return start_date, today
        elif period == ReportPeriod.MONTHLY:
            start_date = today.replace(day=1)
            return start_date, today
        elif period == ReportPeriod.QUARTERLY:
            quarter = ((today.month - 1) // 3) + 1
            start_month = (quarter - 1) * 3 + 1
            start_date = today.replace(month=start_month, day=1)
            return start_date, today
        elif period == ReportPeriod.YEARLY:
            start_date = today.replace(month=1, day=1)
            return start_date, today

    def _calculate_summary_stats(self, transactions: list[Transaction]) -> dict:
        income_transactions = [
            t
            for t in transactions
            if t.transaction_category == TransactionCategory.INCOME
        ]
        expense_transactions = [
            t
            for t in transactions
            if t.transaction_category == TransactionCategory.EXPENSE
        ]

        return {
            "income_transactions": income_transactions,
            "expense_transactions": expense_transactions,
            "total_income": sum(t.amount for t in income_transactions),
            "total_expenses": sum(t.amount for t in expense_transactions),
            "income_count": len(income_transactions),
            "expense_count": len(expense_transactions),
            "total_count": len(transactions),
        }

    def _find_biggest_transactions(
        self,
        income_transactions: list[Transaction],
        expense_transactions: list[Transaction],
    ) -> dict:
        return {
            "biggest_income": max(income_transactions, key=lambda x: x.amount)
            if income_transactions
            else None,
            "biggest_expense": max(expense_transactions, key=lambda x: x.amount)
            if expense_transactions
            else None,
        }

    def _analyze_daily_patterns(self, expense_transactions: list[Transaction]) -> dict:
        daily_spending = {}
        daily_counts = {}

        for transaction in expense_transactions:
            day = transaction.date.date()
            daily_spending[day] = daily_spending.get(day, 0) + transaction.amount
            daily_counts[day] = daily_counts.get(day, 0) + 1

        highest_spending_day = None
        most_transactions_day = None

        if daily_spending:
            max_spending_day = max(daily_spending.items(), key=lambda x: x[1])
            highest_spending_day = DaySpending(
                date=max_spending_day[0],
                total_amount=max_spending_day[1],
                transaction_count=daily_counts[max_spending_day[0]],
            )
            max_transactions_day = max(daily_counts.items(), key=lambda x: x[1])
            most_transactions_day = DaySpending(
                date=max_transactions_day[0],
                total_amount=daily_spending[max_transactions_day[0]],
                transaction_count=max_transactions_day[1],
            )

        return {
            "highest_spending_day": highest_spending_day,
            "most_transactions_day": most_transactions_day,
            "daily_spending": daily_spending,
            "daily_counts": daily_counts,
        }

    def _analyze_category_spending(
        self, expense_transactions: list[Transaction], total_expenses: float, limit: int
    ) -> list[CategorySpending]:
        """Analyze spending by category"""
        category_spending = {}

        for transaction in expense_transactions:
            cat_id = transaction.category_id
            cat_name = transaction.category.name

            if cat_id not in category_spending:
                category_spending[cat_id] = {"name": cat_name, "amount": 0, "count": 0}

            category_spending[cat_id]["amount"] += transaction.amount
            category_spending[cat_id]["count"] += 1

        # Convert to CategorySpending objects
        spending_per_category = []
        for cat_id, data in category_spending.items():
            percentage = (
                (data["amount"] / total_expenses * 100) if total_expenses > 0 else 0
            )
            spending_per_category.append(
                CategorySpending(
                    category_id=cat_id,
                    category_name=data["name"],
                    total_amount=data["amount"],
                    transaction_count=data["count"],
                    percentage_of_total=percentage,
                )
            )

        spending_per_category.sort(key=lambda x: x.total_amount, reverse=True)
        return spending_per_category[:limit]

    def _generate_daily_trends(
        self, start_date: date, end_date: date, daily_spending: dict, daily_counts: dict
    ) -> list[DaySpending]:
        """Generate daily trends data"""
        daily_trends = []
        current_date = start_date

        while current_date <= end_date:
            day_amount = daily_spending.get(current_date, 0)
            day_count = daily_counts.get(current_date, 0)
            daily_trends.append(
                DaySpending(
                    date=current_date,
                    total_amount=day_amount,
                    transaction_count=day_count,
                )
            )
            current_date += timedelta(days=1)

        return daily_trends

    async def create_report(self, params: ReportQueryParams, user_id: UUID) -> TransactionReport:
        """Kreiramo izveštaj o transakcijama za određeni period
        U njemu se nalazi:
        - statistika transakcija
        - najveće prihode i rashode
        - najviše potrošnje po danu
        - potrošnja po kategorijama
        - trendovi potrošnje po danima

        ##TODO - Dodati subcategories za kategorije
        """
        start_date, end_date = self._get_date_range(
            params.period, params.date_from, params.date_to
        )

        transactions = await self.transaction_repo.get_transactions_for_period(
            start_date=start_date,
            end_date=end_date,
            include_category_data=True,  # Trebamo category podatke za report
            user_id=user_id
        )

        summary = self._calculate_summary_stats(transactions)

        biggest = self._find_biggest_transactions(
            summary["income_transactions"], summary["expense_transactions"]
        )

        daily_analysis = self._analyze_daily_patterns(summary["expense_transactions"])

        spending_per_category = self._analyze_category_spending(
            summary["expense_transactions"],
            summary["total_expenses"],
            params.category_limit,
        )

        daily_trends = None
        if params.include_trends:
            daily_trends = self._generate_daily_trends(
                start_date,
                end_date,
                daily_analysis["daily_spending"],
                daily_analysis["daily_counts"],
            )

        return TransactionReport(
            period=params.period,
            date_from=start_date,
            date_to=end_date,
            total_income=summary["total_income"],
            total_expenses=summary["total_expenses"],
            net_amount=summary["total_income"] - summary["total_expenses"],
            income_transaction_count=summary["income_count"],
            expense_transaction_count=summary["expense_count"],
            total_transaction_count=summary["total_count"],
            biggest_income=self._create_transaction_summary(biggest["biggest_income"])
            if biggest["biggest_income"]
            else None,
            biggest_expense=self._create_transaction_summary(biggest["biggest_expense"])
            if biggest["biggest_expense"]
            else None,
            highest_spending_day=daily_analysis["highest_spending_day"],
            most_transactions_day=daily_analysis["most_transactions_day"],
            spending_per_category=spending_per_category,
            daily_trends=daily_trends,
        )

    def _create_transaction_summary(
        self, transaction: Transaction
    ) -> TransactionSummary:
        """Helper to create TransactionSummary from Transaction"""
        return TransactionSummary(
            transaction_id=transaction.id,
            amount=transaction.amount,
            description=transaction.description,
            date=transaction.date,
            category_name=transaction.category.name,
        )
