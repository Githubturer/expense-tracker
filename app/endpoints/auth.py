from fastapi import APIRouter, Depends, BackgroundTasks, Response, Request
from app.services import (
    HouseholdService,
    UserService,
    AuthService,
    mail_service
)
from app.schemas import (
    HouseholdCreate,
    UserCreate,
    HouseholdRead, 
    UserRead, 
    Token,
    EmailResendRequest, 
    PasswordResetRequest, 
    ChangePasswordRequest
)
from app.dependencies import get_db_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.utils import set_refresh_token_cookie
from app.core import get_current_user
from app.models import User
import logging

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/household", response_model=HouseholdRead, status_code=201)
async def register_household(
    household_data: HouseholdCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db_session),
):
    household_service = HouseholdService(session)
    household_and_admin = await household_service.create_household_and_admin(household_data)
    background_tasks.add_task(
        mail_service.send_verification_email,
        household_and_admin.users[0],
    )
    return household_and_admin

@router.post("/email-confirmation", response_model=None, status_code=204)
## može biti i PUT metoda.
async def confirm_email(
    token: str,
    session: AsyncSession = Depends(get_db_session)
):
    auth_service = AuthService(session)
    await auth_service.verify_email(token)

@router.post("/user", response_model=UserRead, status_code=201)
async def register_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    user_service = UserService(session)
    user_data.household_id = current_user.household_id
    new_user = await user_service.create_user(user_data)
    background_tasks.add_task(
        mail_service.send_verification_email,
        new_user,
    )
    return new_user

@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_db_session),
    response: Response = Response,
    request: Request = Request,
):
    auth_service = AuthService(session)
    tokens: Token = await auth_service.authenticate_user(form_data.username, form_data.password, request.headers.get("user-agent"), request.client.host)
    set_refresh_token_cookie(response, tokens.refresh_token)
    return tokens

@router.post("/logout", response_model=None, status_code=204)
async def logout(
    request: Request = Request,
    response: Response = Response,
    session: AsyncSession = Depends(get_db_session),
):
    auth_service = AuthService(session)
    await auth_service.logout(request.cookies.get("refresh_token"))
    response.delete_cookie("refresh_token")

@router.post("/refresh", response_model=Token)
async def refresh(
    request: Request = Request,
    response: Response = Response,
    session: AsyncSession = Depends(get_db_session),
):
    auth_service = AuthService(session)
    tokens: Token = await auth_service.refresh_access_token(request.cookies.get("refresh_token"))
    set_refresh_token_cookie(response, tokens.refresh_token)
    return tokens

@router.post("/resend-email-confirmation", response_model=None, status_code=204)
async def resend_email_confirmation(
    request_data: EmailResendRequest,
    session: AsyncSession = Depends(get_db_session),
    background_tasks: BackgroundTasks = BackgroundTasks,
):
    auth_service = AuthService(session)
    user = await auth_service.resend_email_confirmation(request_data.email)
    background_tasks.add_task(
        mail_service.send_verification_email,
        user,
    )

@router.post("/forgot-password", response_model=None, status_code=204)
async def forgot_password(
    request_data: EmailResendRequest,
    session: AsyncSession = Depends(get_db_session),
    background_tasks: BackgroundTasks = BackgroundTasks,
):
    auth_service = AuthService(session)
    user = await auth_service.forgot_password(request_data.email)
    background_tasks.add_task(
        mail_service.send_password_reset_email,
        user,
    )

@router.post("/reset-password", response_model=None, status_code=204)
async def reset_password(
    request_data: PasswordResetRequest,
    session: AsyncSession = Depends(get_db_session),
):
    auth_service = AuthService(session)
    await auth_service.reset_password(request_data)


@router.post("/change-password", response_model=None, status_code=204)
async def change_password(
    request_data: ChangePasswordRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    auth_service = AuthService(session)
    request_data.user_id = current_user.user_id
    await auth_service.change_password(request_data)
