from fastapi import Response
from app.core import settings


def set_refresh_token_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
    )
