import re
import json
import logging
import brotli
from aiokafka import AIOKafkaConsumer
from src.settings import get_settings
import asyncio
from src.routers.recommendations.consumer_callback_func import update_recommendations

logger = logging.getLogger("uvicorn")

settings = get_settings()
loop = asyncio.get_event_loop()

def create_consumer() -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        settings.kafka_topics,
        loop=loop,
        bootstrap_servers=settings.kafka_instance,
        auto_offset_reset='latest'
    )

consumer = create_consumer()

async def decompress(file_bytes: bytes) -> str:
    return str(
        brotli.decompress(file_bytes),
        settings.file_encoding,
    )


async def consume():
    await consumer.start()
    try:
        async for msg in consumer:
            value = await decompress(msg.value)
            logger.info(
                f"""consumed:
                    topic: {msg.topic},
                    partition: {msg.partition},
                    offset: {msg.offset},
                    key: {msg.key},
                    value: {value},
                    timestamp: {msg.timestamp}""",
            )
            value_json = json.loads(value)
            await update_recommendations(value_json)
    except Exception as e:
        logger.exception(e)
    finally:
        await consumer.stop()
