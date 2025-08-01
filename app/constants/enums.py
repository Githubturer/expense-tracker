from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


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


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    VERIFICATION = "verification"
    PASSWORD_RESET = "password_reset"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SortBy(str, Enum):
    AMOUNT = "amount"
    DATE = "date"
    CATEGORY = "category"


class ReportPeriod(str, Enum):
    CUSTOM = "custom"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
