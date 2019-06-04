import logging
import sys
import json

from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

from app.storage import get_minio_client
from app.core import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
policy_read_only = {
    "Version":
    "2012-10-17",
    "Statement": [{
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
            "AWS": "*"
        },
        "Action": "s3:GetBucketLocation",
        "Resource": f"arn:aws:s3:::{config.MINIO_BUCKET}"
    }, {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
            "AWS": "*"
        },
        "Action": "s3:ListBucket",
        "Resource": f"arn:aws:s3:::{config.MINIO_BUCKET}"
    }, {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
            "AWS": "*"
        },
        "Action": "s3:GetObject",
        "Resource": f"arn:aws:s3:::{config.MINIO_BUCKET}/*"
    }]
}


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
    else:
        try:
            minio.set_bucket_policy(config.MINIO_BUCKET, json.dumps(policy_read_only))
        except ResponseError as err:
            logger.error(err)
            sys.exit(1)


if __name__ == "__main__":
    main()
