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
class Recommendation(BaseDateTimeModel):
    uid = fields.StringField()
    places = fields.ListField(fields.StringField())

    class Meta:
        collection_name = 'Recommendation'

    @classmethod
    async def create_update(cls, data: dict):
        try:
            new_collection = cls(
                uid=data.get('uid'),
                places=data.get('places'),
            )
            await new_collection.commit()
        except Exception as e:
            raise e
        else:
            return new_collection

    @classmethod
    async def get_things_by_id(cls, id: str):
        thing = await cls.find_one({'_id': convert_str_to_object_id(id)})
        if not thing:
            raise ItemNotFound("Item with ID {} not found".format(id)) 
        return dict(thing.dump())
