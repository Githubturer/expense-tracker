from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core import settings
from passlib.context import CryptContext
from app.constants import TokenType
from app.exceptions import InvalidCredentialsError
from app.models.user import User
from app.schemas import TokenPayload, VerificationToken
import hashlib
from fastapi import Header
from typing import Annotated

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def determine_token_type(token_type: TokenType) -> tuple[str, timedelta]:
    """Helper function to determine the secret key and expiration time for the given token type"""
    if token_type == TokenType.ACCESS:
        return settings.access_secret_key, timedelta(minutes=settings.access_token_expire_minutes)
    elif token_type == TokenType.REFRESH:
        return settings.refresh_secret_key, timedelta(days=settings.refresh_token_expire_days)
    elif token_type == TokenType.VERIFICATION:
        return settings.verification_secret_key, timedelta(minutes=settings.verification_token_expire_minutes)
    elif token_type == TokenType.PASSWORD_RESET:
        return settings.password_reset_secret_key, timedelta(minutes=settings.password_reset_token_expire_minutes)

def to_encode(user_data: User, token_type: TokenType, expire: datetime) -> TokenPayload | VerificationToken:
    """Helper function to encode the user data and token type"""

    # za jednostavnost isti token za verifikaciju i resetiranje 
    if token_type in (TokenType.VERIFICATION, TokenType.PASSWORD_RESET):
        return VerificationToken(
            email=user_data.email,
            scope=token_type.value,
            exp=expire
        )
    else:
        return TokenPayload(
            user_id=str(user_data.id),
            household_id=str(user_data.household_id),
            role=user_data.role,
            type=token_type,
            exp=expire
        )

def create_token(user_data: User, token_type: TokenType) -> str:
    """Used for access, refresh, and verification 
    Determines the secret key and expiration time for the given token type
    Args:
        user_data: User
        token_type: TokenType
    Returns:
        str: encoded token
    """

    secret_key, expire_delta = determine_token_type(token_type)
    expire = datetime.now() + expire_delta

    encoded_jwt = jwt.encode(to_encode(user_data, token_type, expire).model_dump(), secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str, token_type: TokenType) -> TokenPayload | VerificationToken:
    try:
        secret_key, _ = determine_token_type(token_type)
        payload = jwt.decode(token, secret_key, algorithms=[settings.algorithm])
        if token_type in (TokenType.VERIFICATION, TokenType.PASSWORD_RESET):
            return VerificationToken(**payload)
        else:
            return TokenPayload(**payload)
    except JWTError:
        raise InvalidCredentialsError
        
async def get_current_user(authorization: Annotated[str | None, Header()]) -> User:
    if not authorization:
        raise InvalidCredentialsError
    token = authorization.split(" ")[1]
    payload = verify_token(token, TokenType.ACCESS)
    return payload

def verify_password(plain_password: str, hashed_password: str) -> bool:
    "Match plain password with hashed password"

    return pwd_context.verify(plain_password, hashed_password)

def hash_password(value: str) -> str:
    """Hash a password"""
    return pwd_context.hash(value)

def hash_refresh_token(value: str) -> str:
    """Hash a refresh token"""
    return hashlib.sha256(value.encode()).hexdigest()
