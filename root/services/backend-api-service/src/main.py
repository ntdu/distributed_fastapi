from fastapi import FastAPI, APIRouter, Query, BackgroundTasks
from src.routers import routers
from src.events import shutdown_events, startup_events

def create_application() -> FastAPI:
    """Create FastAPI application and set routes.

    Returns:
        FastAPI: The created FastAPI instance.
    """

    application = FastAPI(
        docs_url="/docs",
        on_startup=startup_events,
        on_shutdown=shutdown_events,
    )
    for x_router in routers:
        if x_router and isinstance(x_router, APIRouter):
            application.include_router(x_router)
            continue
        print(f'routers expected an instance of APIRouter but get {type(x_router)}')

    return application


app = create_application()
