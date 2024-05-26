import json
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
        travel_recommendation = await TravelRecommendation.get_things_by_id(uid)
    except ItemNotFound as e:
        return custom_response(status_code=status.HTTP_404_NOT_FOUND, data=e.dict())

    task_status = travel_recommendation['status']
    data = {
        'uid': uid,
        'status': task_status,
    }
    if task_status == Status.PENDING.value:
        data['message'] = "The recommendations are not yet available. Please try again later."

    else:
        data['country'] = travel_recommendation['country']
        data['season'] = travel_recommendation['season']
        data['recommendations'] = travel_recommendation['recommendations']

    return custom_response(data)


@router.post('/')
async def generate_travel_recommendations(
    data_in: TravelRecommendationCreate
):
    try:
        new_collection = await TravelRecommendation.create_update(data_in)
        new_collection = new_collection.dump()
    except Exception as e:
        return custom_response(status_code=status.HTTP_400_BAD_REQUEST, data={'message': str(e)})

    uid = new_collection.get('id')
    data = {
        'uid': uid,
        'country': new_collection.get('country'),
        'season': new_collection.get('season')
    }
    await producer.send_and_wait("jobs", await compress(json.dumps(data)))
    return custom_response({
        "uid": uid
    })
