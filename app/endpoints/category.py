from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.repositories.categories_repository import CategoriesRepository
from app.schemas.category import CategoryRead
from app.dependencies import get_db_session

router = APIRouter()

@router.get("/", response_model=list[CategoryRead])
async def read_categories(
    *,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Retrieve all available categories for the current user's household,
    including system-wide default categories.
    """
    categories_repo = CategoriesRepository(session)
    return await categories_repo.get_system_and_household_categories()