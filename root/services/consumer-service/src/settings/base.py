import os
from pydantic_settings import BaseSettings
from core.design_patterns import ThreadSafeSingleton

class Settings(BaseSettings, ThreadSafeSingleton):
    """Class for storing settings."""

    kafka_host: str = os.getenv("KAFKA_HOST")
    kafka_port: str = os.getenv("KAFKA_PORT")
    kafka_topics: str = os.getenv("KAFKA_TOPICS")
    kafka_instance: str = f"{kafka_host}:{kafka_port}"
    file_encoding: str = "utf-8"
    file_compression_quality: int = 1

    DB_MONGO_HOST: str = os.getenv("DB_MONGO_HOST")
    DB_MONGO_PORT: str = os.getenv("DB_MONGO_PORT")
    DB_MONGO_USERNAME: str = os.getenv("DB_MONGO_USERNAME")
    DB_MONGO_PASSWORD: str = os.getenv("DB_MONGO_PASSWORD")
    DB_MONGO_DB_NAME: str = os.getenv("DB_MONGO_DB_NAME")

    OPENAI_BASE_URL: str = 'https://api.openai.com/v1'
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
