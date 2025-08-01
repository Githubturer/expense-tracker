from app.models.transaction import Transaction
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, func
from sqlalchemy import case, and_, desc, asc
from sqlalchemy.orm import selectinload
from app.models import Category
from app.constants import TransactionCategory, SortOrder
from app.schemas import TransactionQueryParams
from datetime import date
from uuid import UUID
from typing import Optional


class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_transaction(self, transaction: Transaction) -> Transaction:
        transaction = Transaction.model_validate(transaction)
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)
        return transaction

    async def get_transaction(self, transaction_id: UUID) -> Transaction | None:
        statement = (
            select(Transaction)
            .where(
                and_(
                    Transaction.id == transaction_id,
                    Transaction.user_id.is_not(None),
                )
            )
        )
        result = await self.session.exec(statement)
        return result.one_or_none()

    async def get_transactions(
        self, params: TransactionQueryParams, user_id: UUID
    ) -> list[Transaction]:
        statement = select(Transaction)
        conditions = []
        # filtriranje
        if params.transaction_type:
            conditions.append(Transaction.transaction_type == params.transaction_type)
        if params.transaction_category:
            conditions.append(
                Transaction.transaction_category == params.transaction_category
            )
        if params.category_id:
            conditions.append(Transaction.category_id == params.category_id)
        if params.date_from:
            conditions.append(Transaction.date >= params.date_from)
        if params.date_to:
            conditions.append(Transaction.date <= params.date_to)

        if conditions:
            statement = statement.where(and_(*conditions))

        # sortiranje
        sort_column = getattr(Transaction, params.sort_by, Transaction.date)
        if params.sort_order == SortOrder.DESC:
            statement = statement.order_by(desc(sort_column))
        else:
            statement = statement.order_by(asc(sort_column))
        # paginacija
        statement = statement.offset(params.offset).limit(params.limit)

        if user_id:
            statement = statement.where(
                and_(
                    Transaction.user_id == user_id,
                )
            )

        result = await self.session.exec(statement)
        return result.all()

    async def get_transactions_for_period(
        self,
        start_date: date,
        end_date: date,
        user_id: Optional[UUID] = None,
        transaction_category: Optional[TransactionCategory] = None,
        include_category_data: bool = True,
    ) -> list[Transaction]:
        """
        Dohvaća transakcije za određeni period - glavni query za sve analize
        Može filtrirati po korisniku i kategoriji transakcije
        """
        if include_category_data:
            # Za reportove trebamo podatke o kategoriji
            statement = select(Transaction).options(selectinload(Transaction.category))
        else:
            # Za jednostavne kalkulacije ne trebamo join
            statement = select(Transaction)

        conditions = [Transaction.date >= start_date, Transaction.date <= end_date]

        if user_id:
            conditions.append(Transaction.user_id == user_id)

        if transaction_category:
            conditions.append(Transaction.transaction_category == transaction_category)

        statement = statement.where(and_(*conditions))
        result = await self.session.exec(statement)
        return result.all()

    async def get_total_amount_for_period(
        self,
        start_date: date,
        end_date: date,
        user_id: Optional[UUID] = None,
        transaction_category: Optional[TransactionCategory] = None,
    ) -> float:
        """
        Vraća samo ukupnu sumu za period - puno brže od dohvaćanja svih transakcija
        """
        statement = select(func.sum(Transaction.amount)).where(
            and_(Transaction.date >= start_date, Transaction.date <= end_date)
        )

        if user_id:
            statement = statement.where(Transaction.user_id == user_id)

        if transaction_category:
            statement = statement.where(
                Transaction.transaction_category == transaction_category
            )

        total = (await self.session.exec(statement)).one_or_none()
        return total or 0.0

    async def get_user_balance(self, user_id: UUID) -> float:
        statement = select(
            func.sum(
                case(
                    (
                        Transaction.transaction_category == TransactionCategory.INCOME,
                        Transaction.amount,
                    ),
                    (
                        Transaction.transaction_category == TransactionCategory.EXPENSE,
                        -Transaction.amount,
                    ),
                    (
                        Transaction.transaction_category
                        == TransactionCategory.TRANSFER,
                        -Transaction.amount,
                    ),
                    else_=0,
                )
            )
        ).where(Transaction.user_id == user_id)
        balance = (await self.session.exec(statement)).one_or_none()
        return balance or 0.0

    async def get_user_current_year_spending(self, user_id: UUID) -> float:
        today = date.today()
        start_of_year = today.replace(month=1, day=1)

        return await self.get_total_amount_for_period(
            start_date=start_of_year,
            end_date=today,
            user_id=user_id,
            transaction_category=TransactionCategory.EXPENSE,
        )

    async def get_user_spending_by_category(self, user_id: UUID) -> dict[str, float]:
        statement = (
            select(Category.name, func.sum(Transaction.amount))
            .join(Category)
            .where(
                and_(
                    Transaction.user_id == user_id,
                    Transaction.transaction_category == TransactionCategory.EXPENSE,
                )
            )
            .group_by(Category.name)
        )
        result = await self.session.exec(statement)
        return dict(result.all())

    async def update_transaction(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)
        return transaction

    async def delete_transaction(self, transaction_id: UUID) -> bool:
        transaction = await self.get_transaction(transaction_id)
        if not transaction:
            return False
        transaction.user_id = None
        await self.update_transaction(transaction)
        return True
