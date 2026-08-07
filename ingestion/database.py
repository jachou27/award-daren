import psycopg

from .config import get_database_config


def get_database_connection() -> psycopg.Connection:
    """Create and return a PostgreSQL connection."""

    config = get_database_config()

    try:
        return psycopg.connect(**config)
    except psycopg.Error as exc:
        raise ConnectionError(
            f"Failed to connect to PostgreSQL: {exc}"
        ) from exc