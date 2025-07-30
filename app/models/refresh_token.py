from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from .user import User

class RefreshTokenBase(SQLModel):
    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    expires_at: datetime


class RefreshToken(RefreshTokenBase, table=True):
    __tablename__ = "refresh_token"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    token_hash: str = Field(index=True)
    ip_address: str
    user_agent: str
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime
    revoked: bool = Field(default=False)


    user: User = Relationship(back_populates="refresh_tokens")
