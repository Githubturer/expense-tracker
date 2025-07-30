from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core import configure_logging
from app.endpoints import category_router, auth_router
from app.exceptions.exceptions_handler import (
    duplicate_email_exception_handler,
    invalid_credentials_exception_handler,
    user_not_found_exception_handler,
    new_password_exception_handler
)
from app.exceptions import (
    DuplicateEmailError,
    InvalidCredentialsError,
    UserNotFoundError,
    NewPasswordError
)
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("""
                --------------------------------
                Starting up...
                --------------------------------
                """)
    yield
    logger.info("""
                --------------------------------
                Shutting down...
                --------------------------------
                """)

app = FastAPI(lifespan=lifespan)

#rute
app.include_router(category_router, prefix="/categories", tags=["categories"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])


#iznimke
app.add_exception_handler(DuplicateEmailError, duplicate_email_exception_handler)
app.add_exception_handler(InvalidCredentialsError, invalid_credentials_exception_handler)
app.add_exception_handler(UserNotFoundError, user_not_found_exception_handler)
app.add_exception_handler(NewPasswordError, new_password_exception_handler)

@app.get("/")
async def root():
    return {"message": "My app is working"}