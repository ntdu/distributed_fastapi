
import boto3
import logging

from botocore.exceptions import NoCredentialsError

logger = logging.getLogger("uvicorn")

from src.settings import get_settings

settings = get_settings()

s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)


def upload_to_s3(local_file, s3_bucket, s3_key):
  try:
    if isinstance(local_file, str):
      s3.upload_file(local_file, s3_bucket, s3_key)
    else:
      s3.upload_fileobj(local_file, s3_bucket, s3_key)
    return True
  except NoCredentialsError:
      logger.info('NoCredentialsError')
      return False


def generate_presigned_url(bucket_name, original_url):
  return s3.generate_presigned_url(
    ClientMethod='get_object',
    Params={'Bucket': bucket_name, 'Key': original_url},
    ExpiresIn=3600,
  )
