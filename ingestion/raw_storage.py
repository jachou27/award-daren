import json
from datetime import datetime, timezone
from pathlib import Path


RAW_DATA_DIR = Path("data/raw")


def save_raw_response(
    payload: dict,
    hotel_id: str,
) -> Path:
    """Save a raw source response and return its file path."""

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")

    filename = f"hyatt_{hotel_id}_{timestamp}.json"
    file_path = RAW_DATA_DIR / filename

    with file_path.open("x", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    return file_path