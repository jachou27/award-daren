import json
from datetime import date, datetime, timezone
from decimal import Decimal

with open("tests/fixtures/hyatt_award_availability_sample.json") as file:
    award_data = json.load(file)

with open("tests/fixtures/hyatt_cash_availability_sample.json") as file:
    cash_data = json.load(file)

with open("tests/fixtures/hyatt_hotel_sample.json") as file:
    hotel_data = json.load(file)

def transform_room_types(award_data, hotel_id):
    # Return a list of dictionary that contains hotel_id, source_room_type_id, name, and award_type
    room_types = []

    for room in award_data["roomRates"].values():
        room_type_record = {
                "hotel_id": hotel_id,
                "source_room_type_id": room["roomTypeCode"],
                "name": room["roomType"]["title"],
                "award_type": room["roomCategory"]
            }

        room_types.append(room_type_record)

    return room_types

#print(transform_room_types(data, 'HNLRW'))


def transform_availability(award_data, cash_data, stay_date):
    availability_records = []
    stay_date = date.fromisoformat(stay_date)
    observed_at = datetime.now(timezone.utc)
    for room in award_data["roomRates"].values():
        award_available = False
        points_price = None
        source_room_type_id = room['roomTypeCode']
        for plan in room['ratePlans']:
            if plan['ratePlanCategory'] == "POINTS":
                award_available = True
                points_price = int(plan['points'])

    
        cash_room = cash_data["roomRates"][source_room_type_id]
        cash_price = None
        currency = None
        for cash_plan in cash_room['ratePlans']:
            if cash_plan['id'] == "MYHI":
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
    hotel_record = {
        "hotel_id": hotel_data["hotel_id"],
        "name": hotel_data["name"],
        "brand": hotel_data["brand"],
        "category": hotel_data["category"],
        "address": hotel_data["address"],
        "city": hotel_data["city"],
        "country": hotel_data["country"]
    }

    return hotel_record

#print(transform_hotel(hotel_data))

