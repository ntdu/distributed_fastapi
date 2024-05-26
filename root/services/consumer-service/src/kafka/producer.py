import brotli
from aiokafka import AIOKafkaProducer

from src.settings import get_settings

def create_producer() -> AIOKafkaProducer:
    return AIOKafkaProducer(bootstrap_servers=get_settings().kafka_instance)

producer = create_producer()

async def compress(message: str) -> bytes:

    return brotli.compress(
        bytes(message, get_settings().file_encoding),
        quality=get_settings().file_compression_quality,
    )
