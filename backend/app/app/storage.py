from minio import Minio

from app.core import config


def get_minio_client() -> Minio:
    return Minio(config.MINIO_SERVER,
                 access_key=config.MINIO_ACCESS_KEY,
                 secret_key=config.MINIO_SECRET_KEY,
                 secure=False)


def get_url(file_name: str) -> str:
    return '//' + config.SERVER_NAME + '/storage/' + config.MINIO_BUCKET + '/' + file_name
