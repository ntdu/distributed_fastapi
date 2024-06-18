import json
import logging
from src.models import Recommendation
from src.connectors import OpenAIApiConnector
from src.utils import remove_number_prefix
from src.kafka.producer import producer, compress


logger = logging.getLogger("uvicorn")
openai_connector = OpenAIApiConnector()


async def get_recommendations(value_json: dict):

    country = value_json.get('country')
    season = value_json.get('season')

    try:
        response = await openai_connector.get_places(country, season)
        message_response = response['choices'][0]['message']['content']
        recommendations = [remove_number_prefix(item) for item in message_response.split('\n')]

    except Exception as e:
        logger.exception(f"get_recommendations: {e}")

    else:
        await Recommendation.create_update(data={
            'uid': value_json.get('uid'),
            'places': recommendations
        })

        data = {
            'uid': value_json.get('uid'),
            'recommendations': recommendations
        }
        await producer.send_and_wait("jobs-status", await compress(json.dumps(data)))
