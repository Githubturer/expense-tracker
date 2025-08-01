from fastapi import APIRouter, Depends
from app.repositories import UserRepository
from app.dependencies import get_db_session, get_current_user
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas import UserRead, UserUpdate, UserBalance
from app.models import User
from app.services.user_service import UserService
from app.services import TransactionService
from app.endpoints.transaction import router as transaction_router

router = APIRouter()
router.include_router(transaction_router)

@router.get("/", response_model=UserRead, status_code=200)
async def get_user(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
):
    user = await UserRepository(session).get_user_by_id(current_user.user_id)
    return user

@router.put("/", response_model=UserRead, status_code=200)
async def update_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
):
    user_data.id = current_user.user_id
    return await UserService(session).update_user(user_data)


@router.delete("/", response_model=None, status_code=204)
async def delete_user(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
):
    await UserService(session).delete_user(current_user.user_id)

@router.get("/balance", response_model=UserBalance, status_code=200)
async def get_user_balance(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
):
    """
    ukljucit potrosnju po TOP 3 kategorije za ovaj mjesec.
    Ukljuciti prekoracenje budzeta za ovaj mjesec.
    ukljuciti informaciju o budzetu za ovaj mjesec.
    """
    return await TransactionService(session).get_user_balance(current_user.user_id)



