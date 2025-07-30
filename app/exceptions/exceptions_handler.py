from fastapi import Request, status
from fastapi.responses import JSONResponse
from .exceptions import DuplicateEmailError, InvalidCredentialsError, UserNotFoundError, NewPasswordError

async def duplicate_email_exception_handler(request: Request, exc: DuplicateEmailError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": str(exc)},
    )

async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": str(exc)},
    )

async def user_not_found_exception_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)},
    )

async def new_password_exception_handler(request: Request, exc: NewPasswordError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)},
    )