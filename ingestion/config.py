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

REQUIRED_S3_VARIABLES = [
    "AWS_REGION",
    "S3_BUCKET_NAME",
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

def get_s3_config() -> dict[str, str]:
    """Load and validate Amazon S3 configuration."""

    missing_variables = [
        variable
        for variable in REQUIRED_S3_VARIABLES
        if not os.getenv(variable)
    ]

    if missing_variables:
        missing = ", ".join(missing_variables)
        raise ValueError(
            f"Missing required S3 environment variables: {missing}"
        )

    return {
        "region": os.environ["AWS_REGION"],
        "bucket_name": os.environ["S3_BUCKET_NAME"],
    }
