from app.repositories.transaction_repository import TransactionRepository
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas import UserBalance, TransactionUpdate
from app.constants import TransactionCategory
from app.models import Transaction
from uuid import UUID
from datetime import date, timedelta


class TransactionService:
    def __init__(self, session: AsyncSession):
        self.transaction_repo = TransactionRepository(session)

    async def get_user_balance(self, user_id: UUID) -> UserBalance:
        balance = await self.transaction_repo.get_user_balance(user_id)
        spending_current_month = await self.get_user_transactions_by_month(
            user_id, TransactionCategory.EXPENSE
        )
        income_current_month = await self.get_user_transactions_by_month(
            user_id, TransactionCategory.INCOME
        )
        return UserBalance(
            balance=balance,
            spending_current_month=spending_current_month,
            income_current_month=income_current_month,
        )
    async def update_transaction(self, transaction_id: UUID, transaction: TransactionUpdate) -> Transaction:
        get_transaction = await self.transaction_repo.get_transaction(transaction_id)
        for key, value in transaction.model_dump(exclude_unset=True).items():
                setattr(get_transaction, key, value)
        return await self.transaction_repo.update_transaction(get_transaction)

    async def get_user_transactions_by_month(
        self,
        user_id: UUID,
        transaction_category: TransactionCategory,
        months_ago: int = 0,
    ) -> float:
        start_date, end_date = self._get_month_range(months_ago)

        return await self.transaction_repo.get_total_amount_for_period(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            transaction_category=transaction_category,
        )

    def _get_month_range(self, months_ago: int = 0) -> tuple[date, date]:
        today = date.today()
        month = today.month - months_ago
        year = today.year

        while month <= 0:
            month += 12
            year -= 1

        start_date = date(year, month, 1)

        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)

        return start_date, end_date
