import json
from datetime import datetime, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

from ingestion.config import get_s3_config


def get_s3_client():
    """Create and return an Amazon S3 client."""

    config = get_s3_config()

    return boto3.client(
        "s3",
        region_name=config["region"],
    )


def upload_json(payload: dict, object_key: str) -> str:
    """Upload a JSON payload to Amazon S3 and return its object key."""

    config = get_s3_config()
    s3_client = get_s3_client()

    json_body = json.dumps(
        payload,
        indent=2,
        ensure_ascii=False,
    )

    try:
        s3_client.put_object(
            Bucket=config["bucket_name"],
            Key=object_key,
            Body=json_body.encode("utf-8"),
            ContentType="application/json",
        )
    except NoCredentialsError as exc:
        raise RuntimeError(
            "AWS credentials are unavailable."
        ) from exc
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(
            f"Failed to upload S3 object: "
            f"s3://{config['bucket_name']}/{object_key}"
        ) from exc

    return object_key


def read_json(object_key: str) -> dict:
    """Read a JSON object from Amazon S3 and return its payload."""

    config = get_s3_config()
    s3_client = get_s3_client()

    try:
        response = s3_client.get_object(
            Bucket=config["bucket_name"],
            Key=object_key,
        )

        json_body = response["Body"].read().decode("utf-8")

        return json.loads(json_body)

    except NoCredentialsError as exc:
        raise RuntimeError(
            "AWS credentials are unavailable."
        ) from exc
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(
            f"Failed to read S3 object: "
            f"s3://{config['bucket_name']}/{object_key}"
        ) from exc


def build_raw_hyatt_key(
    hotel_id: str,
    source_type: str,
    pipeline_run_id: int,
) -> str:
    """Build an S3 object key for a raw Hyatt artifact."""

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")

    return (
        f"raw/hyatt/"
        f"{hotel_id}/"
        f"{pipeline_run_id}/"
        f"{source_type}_{timestamp}.json"
    )
