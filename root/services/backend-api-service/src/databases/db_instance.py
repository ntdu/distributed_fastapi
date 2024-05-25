# -*- coding: utf-8 -*-
from core.databases.mongo import get_umongo_instance
from src.settings import get_settings


settings = get_settings()

mongo_uri = f"""mongodb://{settings.DB_MONGO_USERNAME}:{settings.DB_MONGO_PASSWORD}@{settings.DB_MONGO_HOST}:{settings.DB_MONGO_PORT}/"""

mongo_instance = get_umongo_instance(mongo_uri, settings.DB_MONGO_DB_NAME)
