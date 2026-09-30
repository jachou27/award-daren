import pytest

from ingestion.config import (
    REQUIRED_DATABASE_VARIABLES,
    get_database_config,
    get_s3_config,
)

def test_missing_database_environment_variables(monkeypatch):
    for variable in REQUIRED_DATABASE_VARIABLES:
        monkeypatch.delenv(variable, raising=False)

    with pytest.raises(ValueError):
        get_database_config()

def test_get_s3_config(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-west-1")
    monkeypatch.setenv("S3_BUCKET_NAME", "award-daren-data")

    config = get_s3_config()

    assert config == {
        "region": "us-west-1",
        "bucket_name": "award-daren-data",
    }

def test_get_s3_config_missing_variables(monkeypatch):
    monkeypatch.delenv("AWS_REGION", raising=False)
    monkeypatch.delenv("S3_BUCKET_NAME", raising=False)

    with pytest.raises(
        ValueError,
        match="Missing required S3 environment variables"
    ):
        get_s3_config()
