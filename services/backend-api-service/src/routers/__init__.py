from .recommendations import router as recommendation_router
from .file_processing import router as file_router

routers = (
    recommendation_router,
    file_router,
)
