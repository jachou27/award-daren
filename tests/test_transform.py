import json
from decimal import Decimal
from pathlib import Path

import pytest

from ingestion.transform import (
    transform_availability,
    transform_hotel,
    transform_hyatt_data,
    transform_room_types,
)


def test_transform_hotel():
    hotel_data ={
        "hotel_id": "HNLRW",
        "name": "Hyatt Regency Waikiki Beach Resort and Spa",
        "brand": "Hyatt Regency",
        "category": 5,
        "address": "2424 Kalakaua Avenue, Honolulu, Hawaii 96815-3289, United States",
        "city": "Honolulu",
        "country": "United States"
    }

    result = transform_hotel(hotel_data)

    assert result["hotel_id"] == "HNLRW"
    assert result["category"] == 5

    hotel_data_minimal ={
        "hotel_id": "HNLRW",
        "name": "Hyatt Regency Waikiki Beach Resort and Spa",
        "brand": "Hyatt Regency",
    }

    result_minimal = transform_hotel(hotel_data_minimal)

    assert result_minimal["category"] is None
    assert result_minimal["address"] is None
    assert result_minimal["city"] is None
    assert result_minimal["country"] is None

    hotel_data_missing_id ={
        "name": "Hyatt Regency Waikiki Beach Resort and Spa",
        "brand": "Hyatt Regency",
    }

    with pytest.raises(ValueError):
        transform_hotel(hotel_data_missing_id)

    hotel_data_missing_name = {
        "hotel_id": "HNLRW",
        "brand": "Hyatt Regency",        
    }

    with pytest.raises(ValueError):
        transform_hotel(hotel_data_missing_name)    

def test_transform_room_types():
    award_data ={
        "roomRates": {
            "VW04": {
            "roomTypeCode": "VW04",
            "roomCategory": "STANDARD",
            "roomType": {
                "title": "1 King Bed, Waikiki City View"
                }
            }
        }
    }

    result = transform_room_types(award_data, "HNLRW")
    assert len(result) == 1
    assert result[0]["source_room_type_id"] == "VW04"
    assert result[0]["name"] == "1 King Bed, Waikiki City View"

    with pytest.raises(ValueError):
        transform_room_types(award_data, "")

    award_data_missing_code = {
        "roomRates": {
            "VW04": {
                "roomType": {
                    "title": "1 King Bed, Waikiki City View"
                }
            }
        }
    }

    with pytest.raises(ValueError):
        transform_room_types(award_data_missing_code, "HNLRW")

    award_data_missing_room_type = {
        "roomRates": {
            "VW04": {
                "roomTypeCode": "VW04"
            }
        }
    }

    with pytest.raises(ValueError):
        transform_room_types(award_data_missing_room_type, "HNLRW")

    award_data_missing_title = {
        "roomRates": {
            "VW04": {
                "roomTypeCode": "VW04",
                "roomType": {}
            }
        }
    }

    with pytest.raises(ValueError):
        transform_room_types(award_data_missing_title, "HNLRW")

    award_data_no_category = {
        "roomRates": {
            "VW04": {
                "roomTypeCode": "VW04",
                "roomType": {
                    "title": "1 King Bed, Waikiki City View"
                }
            }
        }
    }

    result_no_category = transform_room_types(award_data_no_category, "HNLRW")

    assert result_no_category[0]["award_type"] is None

def test_transform_availability():
    award_data = {
        "roomRates": {
            "VW04": {
                "roomTypeCode": "VW04",
                "ratePlans": [
                    {
                        "ratePlanCategory": "POINTS",
                        "points": 20000
                    }
                ]
            }
        }
    }

    cash_data = {
        "roomRates": {
            "VW04": {
                "ratePlans": [
                    {
                        "id": "MYHI",
                        "totalAfterTax": 390.56,
                        "currencyCode": "USD"
                    }
                ]
            }
        }
    }

    result = transform_availability(award_data, cash_data, "2026-09-22")
    assert len(result) == 1
    assert result[0]["award_available"] is True
    assert result[0]["points_price"] == 20000
    assert result[0]["cash_price"]== Decimal("390.56")

    with pytest.raises(ValueError):
        transform_availability(award_data, cash_data, "")

    award_data_missing_room_code = {
        "roomRates": {
            "VW04": {
                "ratePlans": [
                    {
                        "ratePlanCategory": "POINTS",
                        "points": 20000
                    }
                ]
            }
        }
    }

    with pytest.raises(ValueError):
        transform_availability(
            award_data_missing_room_code,
            cash_data,
            "2026-09-22"
        )        

    award_data_missing_rate_plans = {
        "roomRates": {
            "VW04": {
                "roomTypeCode": "VW04"
            }
        }
    }

    with pytest.raises(ValueError):
        transform_availability(
            award_data_missing_rate_plans,
            cash_data,
            "2026-09-22"
        )

    award_data_missing_points = {
        "roomRates": {
            "VW04": {
                "roomTypeCode": "VW04",
                "ratePlans": [
                    {
                        "ratePlanCategory": "POINTS"
                    }
                ]
            }
        }
    }

    with pytest.raises(ValueError):
        transform_availability(
            award_data_missing_points,
            cash_data,
            "2026-09-22"
        )

    cash_data_missing_price = {
        "roomRates": {
            "VW04": {
                "ratePlans": [
                    {
                        "id": "MYHI",
                        "currencyCode": "USD"
                    }
                ]
            }
        }
    }

    with pytest.raises(ValueError):
        transform_availability(
            award_data,
            cash_data_missing_price,
            "2026-09-22"
        )

    cash_data_missing_currency = {
        "roomRates": {
            "VW04": {
                "ratePlans": [
                    {
                        "id": "MYHI",
                        "totalAfterTax": 390.56
                    }
                ]
            }
        }
    }

    with pytest.raises(ValueError):
        transform_availability(
            award_data,
            cash_data_missing_currency,
            "2026-09-22"
        )

def test_transform_sanitized_hyatt_fixture():
    fixture_dir = Path("tests/fixtures")

    award_path = fixture_dir / "hyatt_award_availability_sample.json"
    cash_path = fixture_dir / "hyatt_cash_availability_sample.json"
    hotel_path = fixture_dir / "hyatt_hotel_sample.json"

    with award_path.open("r", encoding="utf-8") as file:
        award_data = json.load(file)

    with cash_path.open("r", encoding="utf-8") as file:
        cash_data = json.load(file)

    with hotel_path.open("r", encoding="utf-8") as file:
        hotel_data = json.load(file)

    stay_date = "2026-09-22"

    transformed_data = transform_hyatt_data(
        award_data,
        cash_data,
        hotel_data,
        stay_date,
    )

    assert transformed_data["hotel"]["hotel_id"] == "HNLRW"
    assert len(transformed_data["room_types"]) > 0
    assert len(transformed_data["availability"]) > 0

    availability = transformed_data["availability"][0]

    assert isinstance(availability["points_price"], int)
    assert isinstance(availability["cash_price"], Decimal)
    assert availability["currency"] == availability["currency"].upper()
