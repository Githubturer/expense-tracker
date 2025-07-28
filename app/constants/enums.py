from enum import Enum


class TransactionType(str, Enum):
    FIXED = "fixed"
    VARIABLE = "variable"


class TransactionCategory(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class BudgetPeriod(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
