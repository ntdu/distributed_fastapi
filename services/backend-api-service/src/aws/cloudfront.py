import logging

from datetime import datetime, timedelta

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner


from src.settings import get_settings
logger = logging.getLogger("uvicorn")

settings = get_settings()


def rsa_signer(message):
    private_key = serialization.load_pem_private_key(
        settings.CLOUD_FRONT_PRIVATE_KEY.strip('\n').encode(),
        password=None,  # Provide a password if the key is encrypted
        backend=default_backend() 
    )

    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


def generate_presigned_url_with_signer(url,
                                        expire_date=datetime.now() + timedelta(days=2)):
    cloudfront_signer = CloudFrontSigner(settings.CLOUD_FRONT_PUBLIC_KEY_ID, rsa_signer)
    return cloudfront_signer.generate_presigned_url(url, date_less_than=expire_date)
