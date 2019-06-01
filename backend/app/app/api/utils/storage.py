from minio import Minio

from app.storage import get_minio_client


def get_storage() -> Minio:
    return get_minio_client()
