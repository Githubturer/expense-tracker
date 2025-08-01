"""Populating tables

Revision ID: 616412e9ad67
Revises: c4cf728b2c5d
Create Date: 2025-07-31 15:58:01.422914

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid
from datetime import datetime, timedelta
import random
from app.core.security import hash_password
from app.constants.enums import (
    TransactionType,
    TransactionCategory,
    UserRole,
    BudgetPeriod,
)

# revision identifiers, used by Alembic.
revision: str = "616412e9ad67"
down_revision: Union[str, Sequence[str], None] = "c4cf728b2c5d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    now = datetime.now()

    households = []
    users = []
    user_household_pairs = []

    for i in range(1, 11):
        household_id = uuid.uuid4()
        user_id = uuid.uuid4()

        households.append(
            {
                "id": household_id,
                "name": f"Household {i}",
                "country": "Country",
                "city": "City",
                "address": "Address",
                "zip_code": "12345",
                "created_at": now,
                "updated_at": now,
            }
        )

        users.append(
            {
                "id": user_id,
                "email": f"admin{i}@email.com",
                "first_name": f"Admin{i}",
                "last_name": "User",
                "password": hash_password(f"admin{i}"),
                "age": 30,
                "role": "ADMIN",
                "household_id": household_id,
                "is_verified": True,
                "created_at": now,
                "updated_at": now,
            }
        )

        user_household_pairs.append((user_id, household_id))

    op.bulk_insert(
        sa.table(
            "household",
            sa.column("id", sa.Uuid()),
            sa.column("name", sa.String),
            sa.column("country", sa.String),
            sa.column("city", sa.String),
            sa.column("address", sa.String),
            sa.column("zip_code", sa.String),
            sa.column("created_at", sa.DateTime),
            sa.column("updated_at", sa.DateTime),
        ),
        households,
    )

    op.bulk_insert(
        sa.table(
            "user",
            sa.column("id", sa.Uuid()),
            sa.column("email", sa.String),
            sa.column("first_name", sa.String),
            sa.column("last_name", sa.String),
            sa.column("password", sa.String),
            sa.column("age", sa.Integer),
            sa.column("role", sa.Enum(UserRole)),
            sa.column("household_id", sa.Uuid()),
            sa.column("is_verified", sa.Boolean),
            sa.column("created_at", sa.DateTime),
            sa.column("updated_at", sa.DateTime),
        ),
        users,
    )

    currency_ids = [
        uuid.UUID("11111111-1111-1111-1111-111111111111"),
        uuid.UUID("22222222-2222-2222-2222-222222222222"),
        uuid.UUID("33333333-3333-3333-3333-333333333333"),
        uuid.UUID("44444444-4444-4444-4444-444444444444"),
        uuid.UUID("55555555-5555-5555-5555-555555555555"),
    ]

    income_category_ids = [
        uuid.UUID("66666666-1111-1111-1111-111111111111"),
    ]

    groceries_category_id = uuid.UUID("77777777-3333-1111-1111-111111111111")
    groceries_subcategory_ids = [
        uuid.UUID("77777777-3333-2222-1111-111111111111"),
        uuid.UUID("77777777-3333-3333-1111-111111111111"),
        uuid.UUID("77777777-3333-4444-1111-111111111111"),
        uuid.UUID("77777777-3333-5555-1111-111111111111"),
    ]

    expense_category_ids = [
        uuid.UUID("77777777-1111-1111-1111-111111111111"),
        uuid.UUID("77777777-2222-1111-1111-111111111111"),
        uuid.UUID("77777777-4444-1111-1111-111111111111"),
        uuid.UUID("77777777-5555-1111-1111-111111111111"),
    ]

    transactions = []
    date1 = datetime.now()
    date2 = datetime(2024, 6, 1)

    start_date = min(date1, date2)
    end_date = max(date1, date2)

    for user_id, household_id in user_household_pairs:
        transactions.append(
            {
                "id": uuid.uuid4(),
                "amount": 20000,
                "description": "Initial State",
                "date": start_date,
                "transaction_type": TransactionType.FIXED.value,
                "transaction_category": TransactionCategory.INCOME.value,
                "household_id": household_id,
                "user_id": user_id,
                "category_id": random.choice(income_category_ids),
                "currency_id": random.choice(currency_ids),
                "created_at": now,
                "updated_at": now,
            }
        )

    time_difference_seconds = int((end_date - start_date).total_seconds())
    housing_category_id = uuid.UUID("77777777-1111-1111-1111-111111111111")

    for _ in range(10000):
        date = start_date + timedelta(
            seconds=random.randint(0, time_difference_seconds)
        )

        user_id, household_id = random.choice(user_household_pairs)

        if random.random() < 0.15:
            transaction_category = TransactionCategory.INCOME
            category_id = random.choice(income_category_ids)
            description = "Random Income"
            transaction_type = TransactionType.FIXED.value
        else:
            transaction_category = TransactionCategory.EXPENSE
            description = "Random Expense"

            is_grocery = random.random() < 0.7
            if is_grocery:
                category_id = (
                    random.choice(groceries_subcategory_ids)
                    if random.random() < 0.5
                    else groceries_category_id
                )
            else:
                category_id = random.choice(expense_category_ids)

        if transaction_category == TransactionCategory.INCOME:
            amount = random.randint(1000, 5000)
        else:
            amount = round(random.uniform(5, 250), 2)


        transactions.append(
            {
                "id": uuid.uuid4(),
                "amount": amount,
                "description": description,
                "date": date,
                "transaction_type": "FIXED",
                "transaction_category": transaction_category.value,
                "household_id": household_id,
                "user_id": user_id,
                "category_id": category_id,
                "currency_id": random.choice(currency_ids),
                "created_at": now,
                "updated_at": now,
            }
        )

    op.bulk_insert(
        sa.table(
            "transaction",
            sa.column("id", sa.Uuid()),
            sa.column("amount", sa.Float),
            sa.column("description", sa.String),
            sa.column("date", sa.DateTime),
            sa.column("transaction_type", sa.Enum(TransactionType)),
            sa.column("transaction_category", sa.Enum(TransactionCategory)),
            sa.column("household_id", sa.Uuid()),
            sa.column("user_id", sa.Uuid()),
            sa.column("category_id", sa.Uuid()),
            sa.column("currency_id", sa.Uuid()),
            sa.column("created_at", sa.DateTime),
            sa.column("updated_at", sa.DateTime),
        ),
        transactions,
    )


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
