import sentry_sdk
from src.settings import get_settings

async def init_sentry():
    setting = get_settings()
    SENTRY_SDK_DSN = setting.SENTRY_SDK_DSN
    if SENTRY_SDK_DSN:
        sentry_sdk.init(
            dsn=SENTRY_SDK_DSN,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
            environment=setting.APP_ENV
        )

    return None
