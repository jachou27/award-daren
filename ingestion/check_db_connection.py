from .database import get_database_connection

def main() -> None:
    try:
        with get_database_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()

                print("Database connection successful.")
                print(f"PostgreSQL version: {version[0]}")

    except (ValueError, ConnectionError) as exc:
        print(f"Database connection failed: {exc}")

if __name__ == "__main__":
    main()