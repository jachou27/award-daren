import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

import ingestion.raw_storage as raw_storage


def test_save_raw_response(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    monkeypatch.setattr(raw_storage, "RAW_DATA_DIR", raw_dir)

    fixture_path = Path(
        "tests/fixtures/hyatt_award_availability_sample.json"
    )

    with fixture_path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    saved_path = raw_storage.save_raw_response(
        payload=payload,
        hotel_id="HNLRW",
        source_type="award",
        pipeline_run_id=1,
    )

    assert isinstance(saved_path, Path)
    assert saved_path.exists()
    assert saved_path.parent == raw_dir
    assert saved_path.name.startswith("hyatt_HNLRW_award_run1_")
    assert saved_path.suffix == ".json"

    with saved_path.open("r", encoding="utf-8") as file:
        saved_payload = json.load(file)

    assert saved_payload == payload


def test_save_raw_response_does_not_overwrite(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    monkeypatch.setattr(raw_storage, "RAW_DATA_DIR", raw_dir)

    payload = {"hotelId": "HNLRW"}

    fixed_time = datetime(
        2026,
        8,
        13,
        18,
        30,
        0,
        tzinfo=timezone.utc,
    )

    with patch("ingestion.raw_storage.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_time

        raw_storage.save_raw_response(
            payload=payload,
            hotel_id="HNLRW",
            source_type="award",
            pipeline_run_id=1,
        )

        with pytest.raises(FileExistsError):
            raw_storage.save_raw_response(
                payload=payload,
                hotel_id="HNLRW",
                source_type="award",
                pipeline_run_id=1,
            )
