from fastapi import FastAPI
from contextlib import asynccontextmanager
from config import configure_logging
from database import init_db
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
    await init_db()
    yield
    logger.info("""
                --------------------------------
                Shutting down...
                --------------------------------
                """)

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "My app is working"}