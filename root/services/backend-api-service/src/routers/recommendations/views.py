from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from bson.objectid import ObjectId
from src.models import TravelRecommendation
from src.schemas.recommendations import TravelRecommendationCreate
from core.exceptions.database import ItemNotFound
from core.response.http_response import custom_response
from core.enumerations.recommendations import Status
from src.kafka import producer, compress


router = APIRouter(prefix="/api/v1/travel-recommendations", tags=["Recommendations"])


@router.get('/{uid}')
async def get_travel_recommendations(
    uid: str,
):
    try:
        thing = await TravelRecommendation.get_things_by_id(uid)
    except ItemNotFound as e:
        return custom_response(status_code=status.HTTP_404_NOT_FOUND, data=e.dict())

    status = thing['status']
    data = {
        'uid': uid,
        'status': status,
    }
    if status == Status.PENDING.value:
        data['message'] = "The recommendations are not yet available. Please try again later."

    else:
        data['country'] = thing['country']
        data['season'] = thing['season']

    return custom_response(data)


@router.post('/')
async def generate_travel_recommendations(
    data_in: TravelRecommendationCreate
):
    try:
        new_collection = await TravelRecommendation.create_update(data_in)
        new_collection_id = new_collection.dump()['id']
    except Exception as e:
        return custom_response(status_code=status.HTTP_400_BAD_REQUEST, data={'message': str(e)})

    await producer.send_and_wait("jobs", await compress(new_collection_id))
    return custom_response({
        "uid": new_collection_id
    })
