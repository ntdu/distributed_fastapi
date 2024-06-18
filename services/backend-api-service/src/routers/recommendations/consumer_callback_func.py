import logging
from src.models import TravelRecommendation

logger = logging.getLogger("uvicorn")

async def update_recommendations(
    data_in: dict
):
    try:
        await TravelRecommendation.update(data_in)
    except Exception as e:
        logger.exception(e)
