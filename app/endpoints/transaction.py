from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas import (
    TransactionCreate,
    TransactionRead,
    TransactionUpdate,
    TransactionQueryParams,
    TransactionReport,
    ReportQueryParams,
    TransactionInternal,
)
from app.repositories import TransactionRepository
from app.services import TransactionService
from app.services import ReportingService
from app.dependencies import get_db_session, get_current_user
from uuid import UUID
from app.models.user import User
from fastapi import HTTPException

router = APIRouter(dependencies=[Depends(get_current_user)], prefix="/transactions")


@router.post("/", response_model=TransactionRead, status_code=201)
async def create_transaction(
    transaction: TransactionCreate, session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """
    moze se iskoristit za inicijalizaciju stanja racuna.
    za prijenos sredstava između korisnika u istom kucanstvu, etc.
    """
    transaction_internal = TransactionInternal(
        **transaction.model_dump(),
        user_id=current_user.user_id,
        household_id=current_user.household_id,
    )
    transaction_repo = TransactionRepository(session)
    return await transaction_repo.create_transaction(transaction_internal)


@router.get("/", response_model=list[TransactionRead], status_code=200)
async def get_transactions(
    params: TransactionQueryParams = Depends(),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    transaction_repo = TransactionRepository(session)
    return await transaction_repo.get_transactions(params, current_user.user_id)


@router.get("/report", response_model=TransactionReport, status_code=200)
async def get_transaction_report(
    params: ReportQueryParams = Depends(),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    reporting_service = ReportingService(session)
    return await reporting_service.create_report(params, current_user.user_id)


@router.get("/{transaction_id}", response_model=TransactionRead, status_code=200)
async def get_transaction(
    transaction_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    transaction_repo = TransactionRepository(session)
    transaction = await transaction_repo.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=TransactionRead, status_code=200)
async def update_transaction(
    transaction_id: UUID,
    transaction: TransactionUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    transaction_service = TransactionService(session)
    transaction = await transaction_service.update_transaction(transaction_id, transaction)
    return transaction


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(
    transaction_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    transaction_repo = TransactionRepository(session)
    return await transaction_repo.delete_transaction(transaction_id)
