import logging
from src.kafka import producer

logger = logging.getLogger("uvicorn")


async def event_01_disconnect_kafka():
    await producer.stop()
    logger.info('startup-event: event_01_disconnect_kafka done')


events = [v for k, v in locals().items() if k.startswith("event_")]
