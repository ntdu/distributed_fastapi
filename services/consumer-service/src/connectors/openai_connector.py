import logging
from core.connectors import BaseApiConnector
from src.settings import get_settings
from pydantic_settings import BaseSettings
from core.design_patterns import ThreadSafeSingleton
settings = get_settings()
logger = logging.getLogger("uvicorn")

class OpenAIApiConnector(BaseApiConnector, ThreadSafeSingleton):
    def __init__(self, setting=settings, logger=logger):
        super().__init__(logger)
        self.openai_base_url = setting.OPENAI_BASE_URL
        self.openai_api_key = setting.OPENAI_API_KEY

        self.completions_url = f'{self.openai_base_url}/chat/completions'

    async def get_places(self, country: float, season: float):
        return await self._fetch(
            method='post',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.openai_api_key}'
            },
            url=self.completions_url,
            return_json=True,
            payload={
                "messages": [{
                    "role": "user",
                    "content": f"Suggest three things to do in {country} during {season}. Don't need to explain in detail. Return result in a line without dot ending"
                }],
                "temperature": 0.7,
                "max_tokens": 2000,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "model": "gpt-3.5-turbo",
                "stream": False
            }
        )
