import re
import json
import logging
import brotli
from aiokafka import AIOKafkaConsumer
from src.connectors import OpenAIApiConnector
from src.settings import get_settings
from src.models import Recommendation

logger = logging.getLogger("uvicorn")
openai_connector = OpenAIApiConnector()

settings = get_settings()

def create_consumer() -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        settings.kafka_topics,
        bootstrap_servers=settings.kafka_instance,
    )

consumer = create_consumer()

async def decompress(file_bytes: bytes) -> str:
    return str(
        brotli.decompress(file_bytes),
        settings.file_encoding,
    )

def remove_number_prefix(text):
  """Removes number prefixes (e.g., "1.", "2.", "3.") from strings."""
  return re.sub(r"^\d+\. ", "", text)


from src.kafka.producer import producer, compress

async def consume():
    while True:
        async for msg in consumer:
            value = await decompress(msg.value)
            print(
                "consumed: ",
                f"topic: {msg.topic},",
                f"partition: {msg.partition},",
                f"offset: {msg.offset},",
                f"key: {msg.key},",
                f"value: value,",
                f"timestamp: {msg.timestamp}",
            )
            try:
                value_json = json.loads(value)
                country = value_json.get('country')
                season = value_json.get('season')
                data = {
                    'uid': value_json.get('uid'),
                    'country': country,
                    'season': season,
                }
                try:
                    response = await openai_connector.get_places(country, season)
                    message_response = response['choices'][0]['message']['content']
                    recommendations = [remove_number_prefix(item) for item in message_response.split('\n')]

                    # recommendations = [
                    #     "Visit Ha Long Bay",
                    #     "Explore Hoi An",
                    #     "Relax on Phu Quoc Island"
                    # ]
                except Exception as e:
                    logger.exception(e)

                else:
                    new_collection = await Recommendation.create_update(data={
                        'uid': data.get('uid'),
                        'places': recommendations
                    })
                    new_collection = new_collection.dump()
                    data = {
                        'uid': data.get('uid'),
                        'recommendations': recommendations
                    }
                    print(data)
                    print("*" * 100)
                    await producer.send_and_wait("jobs-status", await compress(json.dumps(data)))

                # response = await openai_connector.get_places(country='VietNam', season='fall')
                # print(f"response: {response}")
                # if response:
                #     message_response = response['choices'][0]['message']['content']
                #     recommendations = [remove_number_prefix(item) for item in message_response.split('\n')]
                #     print(recommendations)

                # # Update the document in MongoDB
                # await TravelRecommendation.find_one(TravelRecommendation.uid == uid).update(
                #     {"status": "completed", "recommendations": recommendations}
                # )
            except Exception as e:
                print(f"Error processing recommendations for UID : {e}")