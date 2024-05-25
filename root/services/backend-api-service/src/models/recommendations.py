from typing import List
from umongo import fields, ValidationError
from core.enumerations.recommendations import Status, Season
# from umongo.document import ValidationError

from core.models.base import BaseDateTimeModel
from core.utils.database import convert_str_to_object_id
from core.exceptions.database import ItemNotFound

from .base import mongo_instance

def validate_choices(choices: List[str]):
    """Custom validator to ensure value is within provided choices."""
    def validator(field_value):
        if field_value not in choices:
            raise ValidationError(
                f"Invalid value '{field_value}'. Must be one of: {', '.join(choices)}"
            )
    return validator

@mongo_instance.register
class ThingsHistory(BaseDateTimeModel):
    status = fields.StringField(default=Status.PENDING.value,
                                validate=validate_choices([Status.PENDING.value, Status.COMPLETED.value]))
    country = fields.StringField(required=True)
    season = fields.StringField(required=True,
                                validate=validate_choices([
                                    Season.SPRING.value,
                                    Season.SUMMER.value,
                                    Season.FALL.value,
                                    Season.WINTER.value]))

    class Meta:
        collection_name = 'ThingsHistory'

    @classmethod
    async def create_update(cls, data: dict):
        try:
            new_things_history = cls(
                season=data.season,
                country=data.country,
            )
            await new_things_history.commit()
        except Exception as e:
            raise e
        else:
            return new_things_history

        return await cls.collection.update_one(
            {'uuid': uuid},
            {
                '$set': {
                    'country': data.country,
                    'season': data.season
                }
            },
            upsert=True
        )
    
        # try:
        #     if data.uuid:
        #         uuid = convert_str_to_object_id(data.uuid)
        #     else:
        #         uuid = ObjectId()

        #     await cls.collection.update_one(
        #         {'uuid': uuid},
        #         {
        #             '$set': {
        #                 'country': data.country,
        #                 'season': data.season
        #             }
        #         },
        #         upsert=True
        #     )
        # except Exception as e:
        #     print(f'exception {e}')

    @classmethod
    async def get_things_by_id(cls, id: str):
        thing = await cls.find_one({'_id': convert_str_to_object_id(id)})
        if not thing:
            raise ItemNotFound("Item with ID {} not found".format(id)) 
        return dict(thing.dump())
