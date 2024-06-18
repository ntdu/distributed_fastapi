from typing import Union
from bson.objectid import ObjectId


def convert_str_to_object_id(id: Union[str, ObjectId]):
    """
    Convert str or ObjectID to ObjectId

    Args:
        id (Union[str, ObjectId]): bson id as str or ObjectId

    Raises:
        ErrorResponseException:
            4220101: Invalid object id format

    Returns:
        _type_: id as ObjectId
    """
    if isinstance(id, str):
        return ObjectId(id)

    if isinstance(id, ObjectId):
        return id

