"""
Upload the latest Silver Parquet dataset to Amazon S3.
"""

from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from config.config import (
    AWS_REGION,
    S3_BUCKET_NAME,
    S3_PREFIX,
    PROCESSED_DATA_DIR,
)

from scripts.logger import logger
from scripts.utils import get_latest_file


def create_s3_client():
    """
    Create an S3 client using the AWS credential provider chain.
    """

    return boto3.client(
        "s3",
        region_name=AWS_REGION,
    )

def build_s3_key(file_path: Path) -> str:
    """
    Preserve Hive partitioning inside S3.

    Example:

    silver/year=2026/month=07/day=11/file.parquet
    """

    relative = file_path.relative_to(PROCESSED_DATA_DIR)

    return f"{S3_PREFIX}/{relative.as_posix()}"


def upload_latest_parquet():

    logger.info("Searching for latest Parquet file...")

    latest_file = get_latest_file(
        PROCESSED_DATA_DIR,
        "parquet",
    )

    logger.info(f"Latest file: {latest_file}")

    s3_key = build_s3_key(latest_file)

    client = create_s3_client()
    
    try:
        logger.info(f"Uploading {latest_file.name} to S3...")

        client.upload_file(
            Filename=str(latest_file),
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
        )

        logger.info("Upload completed successfully.")

    except ClientError as error:
            logger.exception("Failed to upload file to S3.")
            raise

    logger.info("Upload completed successfully.")

    logger.info(f"S3 Bucket : {S3_BUCKET_NAME}")

    logger.info(f"S3 Object : {s3_key}")

    file_size_mb = latest_file.stat().st_size / (1024 * 1024)

    logger.info(f"File Size : {file_size_mb:.2f} MB")
    
    return {
        "bucket": S3_BUCKET_NAME,
        "object": s3_key,
        "file": latest_file.name,
        "size_mb": round(file_size_mb, 2),
    }

def test_connection():
    """
    Test AWS authentication by listing S3 buckets.
    """

    client = create_s3_client()

    response = client.list_buckets()

    logger.info("Successfully connected to AWS.")
    logger.info("Available buckets:")

    for bucket in response["Buckets"]:
        logger.info(f" - {bucket['Name']}")

if __name__ == "__main__":
    upload_latest_parquet()