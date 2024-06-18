import json
# from prefect import task
from src.kafka import producer, compress

async def producer_send_data(data: dict):
    await producer.send_and_wait("jobs", await compress(json.dumps(data)))
