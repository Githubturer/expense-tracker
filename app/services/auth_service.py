from app.repositories import UserRepository, RefreshTokenRepository
from app.core import create_token
from app.schemas import Token, ChangePasswordRequest
from app.models import User, RefreshToken
from app.core.security import verify_password, verify_token, hash_refresh_token, hash_password
from app.constants import TokenType
from app.exceptions import InvalidCredentialsError, UserNotFoundError, NewPasswordError
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timedelta
from app.core import settings
from pydantic import EmailStr
from app.schemas import PasswordResetRequest

class AuthService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)
        self.refresh_token_repo = RefreshTokenRepository(session)

    async def authenticate_user(self, email: str, password: str, user_agent: str, ip_address: str) -> User:
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise UserNotFoundError
        if not user.is_verified:
            raise InvalidCredentialsError("User not verified, please verify your email") #malo ambigious, ali radi jednostavnosti
        if not verify_password(password, user.password):
            raise InvalidCredentialsError
        access_token = create_token(user, TokenType.ACCESS)
        refresh_token = create_token(user, TokenType.REFRESH)
        refresh_token_obj = RefreshToken(
            token_hash=hash_refresh_token(refresh_token),
            user_id=user.id,
            expires_at=datetime.now() + timedelta(days=settings.refresh_token_expire_days),
            user_agent=user_agent,
            ip_address=ip_address
        )
        await self.refresh_token_repo.create_refresh_token(refresh_token_obj)

        return Token(access_token=access_token, refresh_token=refresh_token)
    
    async def refresh_access_token(self, refresh_token: str) -> Token:
        refresh_token_obj = await self.refresh_token_repo.get_refresh_token_by_token(hash_refresh_token(refresh_token))
        if not refresh_token_obj or refresh_token_obj.revoked:
            raise InvalidCredentialsError
        if refresh_token_obj.expires_at < datetime.now():
            raise InvalidCredentialsError
        user = await self.user_repo.get_user_by_id(refresh_token_obj.user_id)
        if not user:
            raise UserNotFoundError
        await self.refresh_token_repo.revoke_refresh_token(refresh_token_obj)
        new_refresh_token = create_token(user, TokenType.REFRESH)
        new_refresh_token_obj = RefreshToken(
            token_hash=hash_refresh_token(new_refresh_token),
            user_id=user.id,
            expires_at=datetime.now() + timedelta(days=settings.refresh_token_expire_days),
            user_agent=refresh_token_obj.user_agent,
            ip_address=refresh_token_obj.ip_address
        )
        await self.refresh_token_repo.create_refresh_token(new_refresh_token_obj)
        access_token = create_token(user, TokenType.ACCESS)
        return Token(access_token=access_token, refresh_token=new_refresh_token)
    
    async def verify_email(self, token: str) -> bool:
        payload = verify_token(token, TokenType.VERIFICATION)
        user = await self.user_repo.get_user_by_email(payload.email)
        if not user:
            raise UserNotFoundError
        user.is_verified = True
        await self.user_repo.update_user(user)
        return True
    
    async def resend_email_confirmation(self, email: EmailStr) -> None:
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise UserNotFoundError
        if user.is_verified:
            raise InvalidCredentialsError('User already verified')
        return user
 
    async def logout(self, refresh_token: str) -> None:
        refresh_token_obj = await self.refresh_token_repo.get_refresh_token_by_token(hash_refresh_token(refresh_token))
        if not refresh_token_obj:
            raise InvalidCredentialsError
        await self.refresh_token_repo.revoke_refresh_token(refresh_token_obj)

    async def forgot_password(self, email: EmailStr) -> None:
        user = await self.user_repo.get_user_by_email(email)
        return user

    async def reset_password(self, data: PasswordResetRequest) -> None:
        payload = verify_token(data.token, TokenType.PASSWORD_RESET)
        user = await self.user_repo.get_user_by_email(payload.email)
        if not user:
            raise UserNotFoundError
        user.password = hash_password(data.new_password)
        await self.user_repo.update_user(user)

    async def change_password(self, data: ChangePasswordRequest) -> None:
        user = await self.user_repo.get_user_by_id(data.user_id)
        if not user:
            raise UserNotFoundError
        if not verify_password(data.old_password, user.password):
            raise NewPasswordError("Invalid old password")
        if data.new_password == data.old_password:
            raise NewPasswordError
        user.password = hash_password(data.new_password)
        await self.user_repo.update_user(user)
        return user
    
