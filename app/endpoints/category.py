from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.repositories.categories_repository import CategoriesRepository
from app.schemas.category import (
    CategoryRead,
    CategoryReadWithSubcategories,
    CategoryCreate,
    CategoryUpdate,
    InternalCategoryCreate,
)
from app.dependencies import get_db_session, get_current_user
from app.models.user import User
from uuid import UUID
import logging

logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=CategoryRead, status_code=201)
async def create_category(
    category: CategoryCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """parent_id je ID roditeljske kategorije. Ako je None, onda je kategorija root. Ako postoji, onda je podkategorija.."""
    # Trenutna mana kreiranja podkategorija je što podkategorija ima tip kategorije [trebala bi nasljedit od kategorije **REDUNDANT**]
    category = InternalCategoryCreate(
        user_id=current_user.user_id,
        household_id=current_user.household_id,
        **category.model_dump(),
    )
    categories_repo = CategoriesRepository(session)
    return await categories_repo.create_category(category)


@router.get("/", response_model=list[CategoryRead], status_code=200)
async def read_categories(
    *,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Ucitava sve kategorije za kućanstvo,
    ukljucujuci i sistemsku kategoriju.
    Ne ukljucuje subkategorije. Sluzi za glavni izbornik kategorija npr.
    """
    categories_repo = CategoriesRepository(session)
    categories = await categories_repo.get_system_and_household_categories()
    return categories


@router.get("/{category_id}", response_model=CategoryReadWithSubcategories)
async def read_category(
    category_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Ucitava kategoriju po id-u.
    Ukljucuje subkategorije.
    Groceries ima npr subkategorije:
    id - 77777777-3333-1111-1111-111111111111
    """
    categories_repo = CategoriesRepository(session)
    category = await categories_repo.get_category_by_id(category_id, subcategories=True)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryReadWithSubcategories.model_validate(category, from_attributes=True)


@router.put("/{category_id}", response_model=CategoryRead, status_code=200)
async def update_category(
    category_id: UUID,
    category: CategoryUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    categories_repo = CategoriesRepository(session)
    return await categories_repo.update_category(category_id, category)


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: UUID, session: AsyncSession = Depends(get_db_session)
):
    categories_repo = CategoriesRepository(session)
    category_deleted = await categories_repo.delete_category(category_id)
    if not category_deleted:
        raise HTTPException(status_code=404, detail="Category not found")
