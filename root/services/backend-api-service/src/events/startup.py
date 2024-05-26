import logging
import asyncio
from src.kafka import producer
from src.kafka.consumer import consumer, consume

logger = logging.getLogger("uvicorn")


async def event_01_connect_kafka():
    await producer.start()
    # await consumer.start()
    logger.info('startup-event: event_01_connect_kafka done')

async def event_02_consume_data_from_kafka():
    asyncio.create_task(consume())
    # await consume()
    logger.info('startup-event: event_02_consume_data_from_kafka ...')

events = [v for k, v in locals().items() if k.startswith("event_")]
