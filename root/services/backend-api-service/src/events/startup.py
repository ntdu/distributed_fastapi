import logging
import asyncio
from src.kafka import producer
from src.kafka.consumer import consume
from src.sentry import init_sentry
logger = logging.getLogger("uvicorn")


async def event_01_connect_kafka():
    await producer.start()
    logger.info('startup-event: event_01_connect_kafka done')

async def event_02_consume_data_from_kafka():
    asyncio.create_task(consume())
    logger.info('startup-event: event_02_consume_data_from_kafka ...')

async def event_03_init_sentry():
    await init_sentry()
    logger.info('startup-event: event_03_init_sentry done')

events = [v for k, v in locals().items() if k.startswith("event_")]
