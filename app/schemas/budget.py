from pydantic import BaseModel


class BudgetCreate(BaseModel):
    name: str
    amount: float
