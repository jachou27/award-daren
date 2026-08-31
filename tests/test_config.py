import pytest

from ingestion.config import REQUIRED_DATABASE_VARIABLES, get_database_config

def test_missing_database_environment_variables(monkeypatch):
    for variable in REQUIRED_DATABASE_VARIABLES:
        monkeypatch.delenv(variable, raising=False)

    with pytest.raises(ValueError):
        get_database_config()
