import logging
from src.kafka import consumer, consume
from src.kafka.producer import producer

logger = logging.getLogger("uvicorn")


async def event_01_connect_kafka():
    await producer.start()
    await consumer.start()

    logger.info('startup-event: event_01_connect_kafka done')


async def event_02_consume_data_from_kafka():
    await consume()
    logger.info('startup-event: event_02_consume_data_from_kafka ...')

events = [v for k, v in locals().items() if k.startswith("event_")]
