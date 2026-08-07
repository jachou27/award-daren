import os
import sys
from pathlib import Path

import psycopg
from dotenv import load_dotenv


# Locate the project root:
# award-daren/ingestion/check_db_connection.py
#              └──────── parents[1] ────────┘
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load environment variables from award-daren/.env
load_dotenv(PROJECT_ROOT / ".env")


REQUIRED_ENV_VARS = [
    "POSTGRES_DB",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
]


def validate_environment() -> None:
    """Confirm that all required database variables are configured."""
    missing_variables = [
        variable
        for variable in REQUIRED_ENV_VARS
        if not os.getenv(variable)
    ]

    if missing_variables:
        missing_list = ", ".join(missing_variables)
        raise RuntimeError(
            f"Missing required environment variables: {missing_list}"
        )


def check_database_connection() -> None:
    """Connect to PostgreSQL and run a simple verification query."""
    validate_environment()

    try:
        with psycopg.connect(
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ["POSTGRES_HOST"],
            port=int(os.environ["POSTGRES_PORT"]),
            connect_timeout=5,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        current_database(),
                        current_user,
                        version();
                    """
                )

                database_name, database_user, postgres_version = (
                    cursor.fetchone()
                )

        print("Database connection successful.")
        print(f"Database: {database_name}")
        print(f"User: {database_user}")
        print(f"PostgreSQL: {postgres_version}")

    except psycopg.Error as error:
        print("Database connection failed.")
        print(f"Reason: {error}")
        sys.exit(1)


if __name__ == "__main__":
    check_database_connection()