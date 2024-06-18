import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Class for storing settings."""

    APP_ENV: Optional[str] = os.getenv("APP_ENV", 'dev')

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

    SENTRY_SDK_DSN: Optional[str] = os.getenv("SENTRY_SDK_DSN")

    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION")

    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME")
    S3_DEFAULT_SESION_ID: str = os.getenv("S3_DEFAULT_SESION_ID")
    S3_STREAM_PREFIX: str = os.getenv("S3_STREAM_PREFIX")

    CLOUD_FRONT_PRIVATE_KEY: str = os.getenv("CLOUD_FRONT_PRIVATE_KEY")
    CLOUD_FRONT_PUBLIC_KEY_ID: str = os.getenv("CLOUD_FRONT_PUBLIC_KEY_ID")
    CLOUD_FRONT_URL: str = os.getenv("CLOUD_FRONT_URL")

