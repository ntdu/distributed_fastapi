from core.models.base import BaseDateTimeModel
from src.databases import mongo_instance

mongo_instance.register(BaseDateTimeModel)
