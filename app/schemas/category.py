from app.models.category import CategoryBase
from app.constants import TransactionCategory
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class CategoryCreate(BaseModel):
    parent_id: Optional[UUID] = (
        None  # ako je None, onda je kategorija root, ako postoji, onda je podkategorija
    )
    name: str
    description: str
    category_type: TransactionCategory

class InternalCategoryCreate(CategoryBase):
    user_id: UUID
    household_id: UUID

class CategoryRead(CategoryBase):
    id: UUID


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryReadWithSubcategories(CategoryRead):
    subcategories: Optional[list["CategoryRead"]] = Field(default_factory=list)
