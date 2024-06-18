import json
import logging
from aiokafka import AIOKafkaConsumer
from src.connectors import OpenAIApiConnector
from src.settings import get_settings
from src.models import Recommendation
from src.utils import decompress
from src.routers import get_recommendations

logger = logging.getLogger("uvicorn")
openai_connector = OpenAIApiConnector()

settings = get_settings()

def create_consumer() -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        settings.kafka_topics,
        bootstrap_servers=settings.kafka_instance,
    )

consumer = create_consumer()

async def consume():
    while True:
        async for msg in consumer:
            value = await decompress(msg.value, settings.file_encoding)
            logger.info(
                f"""consumed:
                    topic: {msg.topic},
                    partition: {msg.partition},
                    offset: {msg.offset},
                    key: {msg.key},
                    value: {value},
                    timestamp: {msg.timestamp}""",
            )

            try:
                await get_recommendations(json.loads(value))
            except Exception as e:
                logger.exception(f"Conmmer exception: {str(e)}")