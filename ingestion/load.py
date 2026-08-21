def load(connection, transformed_data, pipeline_run_id):
    hotel = transformed_data["hotel"]
    room_types = transformed_data["room_types"]
    availability_records = transformed_data["availability"]

    hotel_count = 0
    room_type_count = 0
    availability_count = 0
    room_type_mapping = {}

    try:
        with connection.cursor() as cursor:
            load_hotel(cursor, hotel)
            hotel_count += 1

            for room_type in room_types:
                source_room_type_id = room_type["source_room_type_id"]
                room_type_id = load_room_type(cursor, room_type)
                room_type_mapping[source_room_type_id] = room_type_id
                room_type_count += 1

            for availability in availability_records:
                load_availability(cursor, availability, room_type_mapping, pipeline_run_id)
                availability_count += 1

        connection.commit()
    except Exception:
        connection.rollback()
        raise 

    counts = {
        "hotels": hotel_count,
        "room_types": room_type_count,
        "availability": availability_count
    }

    return counts



def load_hotel(cursor, hotel: dict) -> None:
    sql = """
    INSERT INTO hotels (
    hotel_id,
    name,
    brand,
    category,
    address,
    city,
    country
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (hotel_id)
    DO UPDATE SET
        name = EXCLUDED.name,
        brand = EXCLUDED.brand,
        category = EXCLUDED.category,
        address = EXCLUDED.address,
        city = EXCLUDED.city,
        country = EXCLUDED.country;
    """

    cursor.execute(
        sql,
        (
            hotel["hotel_id"],
            hotel["name"],
            hotel["brand"],
            hotel["category"],
            hotel["address"],
            hotel["city"],
            hotel["country"]
        )
    )

def load_room_type(cursor, room_type: dict) -> int:
    sql = """
    INSERT INTO room_types (
    hotel_id,
    source_room_type_id,
    name,
    award_type
    )
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (hotel_id, source_room_type_id)
    DO UPDATE SET
        name = EXCLUDED.name,
        award_type = EXCLUDED.award_type
    RETURNING room_type_id
    """

    cursor.execute(
        sql,
        (
            room_type["hotel_id"],
            room_type["source_room_type_id"],
            room_type["name"],
            room_type["award_type"]
        )
    )

    row = cursor.fetchone()

    return row[0]


def load_availability(cursor, availability: dict, room_type_mapping: dict, pipeline_run_id: int) -> None:
    source_room_type_id = availability["source_room_type_id"]
    if source_room_type_id in room_type_mapping:
        room_type_id = room_type_mapping[source_room_type_id]
    else:
        raise KeyError(f"Room type {source_room_type_id} not found in room_type_mapping")
    
    sql = """
    INSERT INTO daily_availability (
    room_type_id,
    stay_date,
    award_available,
    points_price,
    cash_price,
    currency,
    observed_at,
    pipeline_run_id
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            room_type_id,
            availability["stay_date"],
            availability["award_available"],
            availability["points_price"],
            availability["cash_price"],
            availability["currency"],
            availability["observed_at"],
            pipeline_run_id
        )
    )
