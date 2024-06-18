from fastapi import FastAPI, APIRouter, Query, BackgroundTasks
from src.events import shutdown_events, startup_events

def create_application() -> FastAPI:
    """Create FastAPI application and set routes.

    Returns:
        FastAPI: The created FastAPI instance.
    """

    application = FastAPI(
        on_startup=startup_events,
        on_shutdown=shutdown_events,
    )
    return application


app = create_application()
