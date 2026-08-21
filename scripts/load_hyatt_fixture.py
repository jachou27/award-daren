import json
from ingestion.transform import transform_hyatt_data
from ingestion.database import get_database_connection
from ingestion.load import load

with open("tests/fixtures/hyatt_award_availability_sample.json") as file:
    award_data = json.load(file)

with open("tests/fixtures/hyatt_cash_availability_sample.json") as file:
    cash_data = json.load(file)

with open("tests/fixtures/hyatt_hotel_sample.json") as file:
    hotel_data = json.load(file)


transformed_data = transform_hyatt_data(award_data, cash_data, hotel_data, "2026-09-22")

connection = get_database_connection()

pipeline_run_id =  1

load_counts = load(connection, transformed_data, pipeline_run_id)

print(load_counts)