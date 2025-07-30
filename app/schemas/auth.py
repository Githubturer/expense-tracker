from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.constants import UserRole, TokenType
from .base import BaseResponse
from uuid import UUID


class EmailResendRequest(BaseModel):
    email: EmailStr

class PasswordResetRequest(BaseModel):
    new_password: str
    token: str

class ChangePasswordRequest(BaseModel):
    user_id: UUID | None = None
    old_password: str
    new_password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str

class VerificationToken(BaseModel):
    email: EmailStr
    scope: str
    exp: datetime

class TokenPayload(BaseModel): #za jednostavnost jedan model za access i refresh token
    user_id: str
    household_id: str
    role: UserRole
    type: TokenType
    exp: datetime