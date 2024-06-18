import logging
from functools import lru_cache

from .base import *

logger = logging.getLogger("uvicorn")

@lru_cache()
def get_settings() -> BaseSettings:
    """Get application settings usually stored as environment variables.

    Returns:
        Settings: Application settings.
    """

    logger.info("Loading config settings from the environment...")
    return Settings()
