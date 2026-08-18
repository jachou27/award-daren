from ingestion.transform import transform_hotel, transform_room_types, transform_availability
from decimal import Decimal

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