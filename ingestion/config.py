import os

from dotenv import load_dotenv

load_dotenv()

REQUIRED_DATABASE_VARIABLES = [
    "POSTGRES_HOST", 
    "POSTGRES_PORT",
    "POSTGRES_DB",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
]

def get_database_config() -> dict[str, str]:
    """Load and validate PostgreSQL configuration.""" 

    missing_variables = [
        variable
        for variable in REQUIRED_DATABASE_VARIABLES
        if not os.getenv(variable)
    ]

    if missing_variables:
        missing = ", ".join(missing_variables)
        raise ValueError(
            f"Missing required database environment variables: {missing}"
        )

    return {
        "host": os.environ["POSTGRES_HOST"],
        "port": os.environ["POSTGRES_PORT"],
        "dbname": os.environ["POSTGRES_DB"],
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
    }