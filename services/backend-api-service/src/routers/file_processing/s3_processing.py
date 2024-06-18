from fastapi import APIRouter, status, BackgroundTasks
import os
import uuid
from datetime import datetime
from src.models import TravelRecommendation
from src.schemas.recommendations import TravelRecommendationCreate
from core.exceptions.database import ItemNotFound
from core.response.http_response import custom_response
from core.enumerations.recommendations import Status
from src.utils import producer_send_data
from fastapi import APIRouter, UploadFile, Form
from typing import List, Optional

from src.settings import get_settings
from src.aws import upload_to_s3, generate_presigned_url, generate_presigned_url_with_signer

settings = get_settings()

router = APIRouter(prefix="/api/v1/file-processing", tags=["Files"])


@router.post("/stream")
async def stream_file(
                    file: UploadFile,
                    session_id: Optional[str] = Form(None)):
    try:

        user_id = 123  # get user_id from request

        hash_name = uuid.uuid4().hex
        now = datetime.now()
        if not session_id:
            session_id = settings.S3_DEFAULT_SESION_ID
        # format to string
        datetime_prefix = now.strftime("%Y%m%d%H%M%S")

        _, file_extension = os.path.splitext(file.filename)
        s3_image_key = f"{settings.S3_STREAM_PREFIX}/{user_id}/{session_id}/{datetime_prefix}_{hash_name}{file_extension}"

        if not file.content_type.startswith('image/') :
            return custom_response(
                status_code=400,
                data={
                    'message': f'Invalid file type: {file.content_type}',
                }
            )

        upload_to_s3(file.file, settings.S3_BUCKET_NAME, s3_image_key)
        return custom_response(
            status_code=status.HTTP_201_CREATED,
            data={ 
                "session_file_path": f'{settings.S3_STREAM_PREFIX}/{user_id}/{session_id}/{datetime_prefix}_{hash_name}',
                # "check": generate_presigned_url(settings.S3_BUCKET_NAME, s3_image_key)
                # "url": f'{settings.CLOUD_FRONT_URL}/{s3_image_key}',
                "url": generate_presigned_url_with_signer(f'{settings.CLOUD_FRONT_URL}/{s3_image_key}')
                },
            )
    except Exception as e:
        print(e)
        return custom_response(status_code=500,data={
            'message': 'error',
            'traceback': str(e),
        })