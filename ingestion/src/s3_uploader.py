
import boto3
from pathlib import Path
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()


def get_s3_client():
    return boto3.client("s3")


def check_bucket_connection(bucket_name: str) -> bool:

    s3_client = get_s3_client()

    try:
        s3_client.head_bucket(Bucket=bucket_name)

        print(f"Successfully connected to S3 bucket: {bucket_name}")
        return True

    except ClientError as error:
        print("S3 bucket connection failed:")
        print(error.response["Error"]["Message"])
        return False


def upload_csv_to_s3(
    file_path: Path,
    bucket_name: str,
    batch_id: str,
    load_type: str,
    raw_prefix: str = "raw/"
) -> str:

    if load_type not in ("initial_load", "incremental_load"):
        raise ValueError(f"Invalid load type: {load_type}")

    s3_client = get_s3_client()

    dataset_name = file_path.stem.split("_")[0] if False else file_path.stem

    file_name = f"{dataset_name}_{batch_id}{file_path.suffix}"

    s3_key = (
        f"{raw_prefix.rstrip('/')}/"
        f"{dataset_name}/{file_name}"
    )

    # Check whether the destination object already exists
    try:
        response = s3_client.head_object(
            Bucket=bucket_name,
            Key=s3_key
        )

        # Verify that the existing object has the expected size
        if response["ContentLength"] != file_path.stat().st_size:
            raise ValueError(
                f"Existing S3 object has a different size: {s3_key}"
            )

        print(f"Already uploaded to S3: {s3_key}")
        return s3_key

    except ClientError as error:
        error_code = error.response["Error"]["Code"]

        if error_code not in ("404", "NoSuchKey", "NotFound"):
            raise

    # Upload CSV when the object does not exist
    s3_client.upload_file(
        str(file_path),
        bucket_name,
        s3_key
    )

    print(f"Successfully uploaded: {s3_key}")

    return s3_key
