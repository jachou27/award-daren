from datetime import date, datetime, timezone
from decimal import Decimal

def validate_required_fields(data, required_fields, record_name):
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required {record_name} field: {field}")

def transform_room_types(award_data, hotel_id):
    if not hotel_id:
        raise ValueError("Missing required room type field: hotel_id")

    room_types = []

    for room in award_data["roomRates"].values():
        validate_required_fields(room, ["roomTypeCode", "roomType"], "room type")
        validate_required_fields(room["roomType"], ["title"], "room type")
        room_type_record = {
                "hotel_id": hotel_id,
                "source_room_type_id": room["roomTypeCode"],
                "name": room["roomType"]["title"],
                "award_type": room.get("roomCategory")
            }

        room_types.append(room_type_record)

    return room_types

#print(transform_room_types(data, 'HNLRW'))


def transform_availability(award_data, cash_data, stay_date):
    if not stay_date:
        raise ValueError("Missing required availability field: stay_date")
    availability_records = []
    stay_date = date.fromisoformat(stay_date)
    observed_at = datetime.now(timezone.utc)
    for room in award_data["roomRates"].values():
        validate_required_fields(room, ["roomTypeCode", "ratePlans"], "availability")
        award_available = False
        points_price = None
        source_room_type_id = room['roomTypeCode']
        for plan in room['ratePlans']:
            validate_required_fields(plan, ["ratePlanCategory"],"award rate plan")
            if plan['ratePlanCategory'] == "POINTS":
                validate_required_fields(plan, ["points"], "award rate plan")
                award_available = True
                points_price = int(plan['points'])

    
        cash_room = cash_data["roomRates"][source_room_type_id]
        validate_required_fields(cash_room, ["ratePlans"], "cash room")
        cash_price = None
        currency = None
        for cash_plan in cash_room['ratePlans']:
            validate_required_fields(cash_plan, ["id"], "cash rate plan")
            if cash_plan['id'] == "MYHI":
                validate_required_fields(cash_plan, ["totalAfterTax", "currencyCode"], "cash rate plan")
                cash_price = Decimal(str(cash_plan["totalAfterTax"]))
                currency = cash_plan["currencyCode"].upper()

        availability_record = {
            "source_room_type_id": source_room_type_id,
            "award_available": award_available,
            "points_price": points_price,
            "stay_date": stay_date,
            "observed_at": observed_at,
            "cash_price": cash_price,
            "currency": currency
        }

        availability_records.append(availability_record)

    return availability_records


#print(transform_availability(award_data, cash_data, "2026-09-22"))

def transform_hotel(hotel_data):
    validate_required_fields(hotel_data, ["hotel_id", "name", "brand"], "hotel")

    hotel_record = {
        "hotel_id": hotel_data["hotel_id"],
        "name": hotel_data["name"],
        "brand": hotel_data["brand"],
        "category": hotel_data.get("category"),
        "address": hotel_data.get("address"),
        "city": hotel_data.get("city"),
        "country": hotel_data.get("country")
    }

    return hotel_record

#print(transform_hotel(hotel_data))

def transform_hyatt_data(award_data, cash_data, hotel_data, stay_date):
    hotel = transform_hotel(hotel_data)
    room_types = transform_room_types(award_data, hotel["hotel_id"])
    availability = transform_availability(award_data, cash_data, stay_date)

    transformed_data = {
        "hotel": hotel,
        "room_types": room_types,
        "availability": availability
    }

    return transformed_data
