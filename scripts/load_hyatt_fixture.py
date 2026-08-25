import json
from ingestion.transform import transform_hyatt_data
from ingestion.database import get_database_connection
from ingestion.load import load
from ingestion.pipeline_runs import start_pipeline_run, complete_pipeline_run, fail_pipeline_run

with open("tests/fixtures/hyatt_award_availability_sample.json") as file:
    award_data = json.load(file)

with open("tests/fixtures/hyatt_cash_availability_sample.json") as file:
    cash_data = json.load(file)

with open("tests/fixtures/hyatt_hotel_sample.json") as file:
    hotel_data = json.load(file)


transformed_data = transform_hyatt_data(award_data, cash_data, hotel_data, "2026-09-22")
records_extracted = 1 + len(transformed_data["room_types"]) + len(transformed_data["availability"])

connection = get_database_connection()

with connection.cursor() as cursor:
    pipeline_run_id = start_pipeline_run(cursor, "hyatt")
    connection.commit()
    try:
        load_counts = load(cursor, transformed_data, pipeline_run_id)
        records_loaded = sum(load_counts.values())
        complete_pipeline_run(cursor, pipeline_run_id, records_extracted, records_loaded)
        connection.commit()
    except Exception:
        error_message = "Hyatt pipeline failed"
        connection.rollback()
        fail_pipeline_run(cursor, pipeline_run_id, error_message)
        connection.commit()
        raise
