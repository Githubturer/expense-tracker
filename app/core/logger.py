import logging
from .config import settings


def configure_logging() -> None:
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s - %(funcName)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
