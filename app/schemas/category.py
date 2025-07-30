from app.models.category import CategoryBase
from pydantic import BaseModel
from uuid import UUID

class CategoryCreate(CategoryBase):
    id: UUID

class CategoryRead(CategoryBase):
    id: UUID

    
