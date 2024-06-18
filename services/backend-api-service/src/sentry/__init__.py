import logging
import sentry_sdk
from src.settings import get_settings


logger = logging.getLogger("uvicorn")


async def init_sentry():
    setting = get_settings()
    SENTRY_SDK_DSN = setting.SENTRY_SDK_DSN
    if SENTRY_SDK_DSN:
        try:
            sentry_sdk.init(
                dsn=SENTRY_SDK_DSN,
                traces_sample_rate=1.0,
                profiles_sample_rate=1.0,
                environment=setting.APP_ENV
            )
        except Exception as e:
            logger.exception(f"Init sentry get exception: {e}")

    return None
