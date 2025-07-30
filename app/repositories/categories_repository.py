from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import or_
from typing import Optional, List
from uuid import UUID
from app.models.category import Category, CategoryBase


class CategoriesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, category: CategoryBase) -> Category:
        db_category = Category.model_validate(category)
        self.session.add(db_category)
        await self.session.commit()
        await self.session.refresh(db_category)
        return db_category

    async def get_category_by_id(self, category_id: UUID) -> Optional[Category]:
        statement = select(Category).where(Category.id == category_id)
        result = await self.session.exec(statement)
        return result.first()

    async def get_system_and_household_categories(
        self, household_id: Optional[UUID] = None
    ) -> List[Category]:
        conditions = [Category.household_id.is_(None)]
        if household_id:
            conditions.append(Category.household_id == household_id)
        
        statement = select(Category).where(or_(*conditions))
        result = await self.session.exec(statement)
        return result.all()

    async def update_category(self, category_id: UUID, category: CategoryBase) -> Optional[Category]:
        db_category = await self.get_category_by_id(category_id)
        if not db_category:
            return None
        
        category_data = category.model_dump(exclude_unset=True)
        for key, value in category_data.items():
            setattr(db_category, key, value)
            
        self.session.add(db_category)
        await self.session.commit()
        await self.session.refresh(db_category)
        return db_category
    
    async def delete_category(self, category_id: UUID) -> bool:
        db_category = await self.get_category_by_id(category_id)
        if not db_category:
            return False
        
        await self.session.delete(db_category)
        await self.session.commit()
        return True
