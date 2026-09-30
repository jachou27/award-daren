from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError, NoCredentialsError

from ingestion.s3_storage import (
    build_raw_hyatt_key,
    read_json,
    upload_json,
)


def test_upload_json(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-west-1")
    monkeypatch.setenv("S3_BUCKET_NAME", "award-daren-data")

    mock_s3_client = MagicMock()

    with patch(
        "ingestion.s3_storage.get_s3_client",
        return_value=mock_s3_client,
    ):
        object_key = upload_json(
            {"test": "data"},
            "raw/hyatt/test.json",
        )

    mock_s3_client.put_object.assert_called_once_with(
        Bucket="award-daren-data",
        Key="raw/hyatt/test.json",
        Body=b'{\n  "test": "data"\n}',
        ContentType="application/json",
    )

    assert object_key == "raw/hyatt/test.json"


def test_read_json(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-west-1")
    monkeypatch.setenv("S3_BUCKET_NAME", "award-daren-data")

    mock_s3_client = MagicMock()

    mock_s3_client.get_object.return_value = {
        "Body": BytesIO(b'{\n  "test": "data"\n}')
    }

    with patch(
        "ingestion.s3_storage.get_s3_client",
        return_value=mock_s3_client,
    ):
        payload = read_json("raw/hyatt/test.json")

    mock_s3_client.get_object.assert_called_once_with(
        Bucket="award-daren-data",
        Key="raw/hyatt/test.json",
    )

    assert payload == {"test": "data"}


def test_upload_json_client_error(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-west-1")
    monkeypatch.setenv("S3_BUCKET_NAME", "award-daren-data")

    mock_s3_client = MagicMock()

    mock_s3_client.put_object.side_effect = ClientError(
        {
            "Error": {
                "Code": "AccessDenied",
                "Message": "Access Denied",
            }
        },
        "PutObject",
    )

    with patch(
        "ingestion.s3_storage.get_s3_client",
        return_value=mock_s3_client,
    ):
        with pytest.raises(
            RuntimeError,
            match="Failed to upload S3 object",
        ):
            upload_json(
                {"test": "data"},
                "raw/hyatt/test.json",
            )


def test_read_json_client_error(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-west-1")
    monkeypatch.setenv("S3_BUCKET_NAME", "award-daren-data")

    mock_s3_client = MagicMock()

    mock_s3_client.get_object.side_effect = ClientError(
        {
            "Error": {
                "Code": "NoSuchKey",
                "Message": "The specified key does not exist.",
            }
        },
        "GetObject",
    )

    with patch(
        "ingestion.s3_storage.get_s3_client",
        return_value=mock_s3_client,
    ):
        with pytest.raises(
            RuntimeError,
            match="Failed to read S3 object",
        ):
            read_json("raw/hyatt/missing.json")


def test_upload_json_no_credentials(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-west-1")
    monkeypatch.setenv("S3_BUCKET_NAME", "award-daren-data")

    mock_s3_client = MagicMock()

    mock_s3_client.put_object.side_effect = NoCredentialsError()

    with patch(
        "ingestion.s3_storage.get_s3_client",
        return_value=mock_s3_client,
    ):
        with pytest.raises(
            RuntimeError,
            match="AWS credentials are unavailable",
        ):
            upload_json(
                {"test": "data"},
                "raw/hyatt/test.json",
            )


def test_build_raw_hyatt_key():
    object_key = build_raw_hyatt_key(
        hotel_id="CHIHC",
        source_type="award",
        pipeline_run_id=12,
    )

    assert object_key.startswith(
        "raw/hyatt/CHIHC/12/award_"
    )
    assert object_key.endswith(".json")
