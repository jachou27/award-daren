import argparse
import json
import sys
from pathlib import Path

from ingestion.database import get_database_connection
from ingestion.load import load
from ingestion.pipeline_runs import (
    start_pipeline_run,
    complete_pipeline_run,
    fail_pipeline_run,
)
from ingestion.raw_storage import save_raw_response
from ingestion.transform import transform_hyatt_data


def main() -> int:
    """Run the end-to-end Hyatt pipeline and return a process exit code."""
    parser = argparse.ArgumentParser()

    parser.add_argument("--award-input", required=True)
    parser.add_argument("--cash-input", required=True)
    parser.add_argument("--hotel-input", required=True)
    parser.add_argument("--stay-date", required=True)

    args = parser.parse_args()

    connection = get_database_connection()

    try:
        with connection.cursor() as cursor:
            pipeline_run_id = start_pipeline_run(cursor, "hyatt")
            connection.commit()

            try:
                award_path = Path(args.award_input)
                cash_path = Path(args.cash_input)
                hotel_path = Path(args.hotel_input)
                stay_date = args.stay_date

                if not award_path.exists():
                    raise FileNotFoundError(
                        f"Input file not found: {award_path}"
                    )

                if not cash_path.exists():
                    raise FileNotFoundError(
                        f"Input file not found: {cash_path}"
                    )

                if not hotel_path.exists():
                    raise FileNotFoundError(
                        f"Input file not found: {hotel_path}"
                    )

                with open(award_path) as file:
                    award_data = json.load(file)

                with open(cash_path) as file:
                    cash_data = json.load(file)

                with open(hotel_path) as file:
                    hotel_data = json.load(file)

                save_raw_response(
                    award_data,
                    hotel_data["hotel_id"],
                    "award",
                    pipeline_run_id
                )

                save_raw_response(
                    cash_data,
                    hotel_data["hotel_id"],
                    "cash",
                    pipeline_run_id
                )

                save_raw_response(
                    hotel_data,
                    hotel_data["hotel_id"],
                    "hotel",
                    pipeline_run_id
                )

                transformed_data = transform_hyatt_data(
                    award_data,
                    cash_data,
                    hotel_data,
                    stay_date
                )

                records_extracted = (
                    1
                    + len(transformed_data["room_types"])
                    + len(transformed_data["availability"])
                )

                load_counts = load(
                    cursor,
                    transformed_data,
                    pipeline_run_id
                )

                records_loaded = sum(load_counts.values())

                complete_pipeline_run(
                    cursor,
                    pipeline_run_id,
                    records_extracted,
                    records_loaded
                )

                connection.commit()

                success_message = (
                    "Pipeline completed successfully\n\n"
                    f"Pipeline run ID: {pipeline_run_id}\n"
                    f"Records extracted: {records_extracted}\n"
                    f"Records loaded: {records_loaded}"
                )

                print(success_message)
                return 0

            except Exception as e:
                error_message = (
                    "Pipeline failed\n\n"
                    f"Pipeline run ID: {pipeline_run_id}\n"
                    f"Error: {e}"
                )

                connection.rollback()

                fail_pipeline_run(
                    cursor,
                    pipeline_run_id,
                    str(e)
                )

                connection.commit()

                print(error_message)
                return 1

    finally:
        connection.close()


if __name__ == "__main__":
    sys.exit(main())
