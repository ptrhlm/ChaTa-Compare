import logging
import sys

from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

from app.storage import get_minio_client
from app.core import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    try:
        minio = get_minio_client()
        minio.make_bucket(config.MINIO_BUCKET)
        logger.info(f'Create bucket {config.MINIO_BUCKET}')
    except (BucketAlreadyExists, BucketAlreadyOwnedByYou):
        logger.info(f'Bucket already exists. Skipping')
    except ResponseError as err:
        logger.error(err)
        sys.exit(1)


if __name__ == "__main__":
    main()
