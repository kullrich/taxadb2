import pytest
import configparser
import os

def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="taxadb.ini", help="Path to config file")

@pytest.fixture(scope="session")
def config(request):
    """Load configuration from an .ini file."""
    config_path = request.config.getoption("--config")
    parser = configparser.ConfigParser()
    parser.read(config_path)

    return {
        "sql": {
            "dbtype": parser.get("sql", "dbtype", fallback="sqlite"),
            "username": parser.get("sql", "username", fallback=None),
            "password": parser.get("sql", "password", fallback=None),
            "hostname": parser.get("sql", "hostname", fallback=None),
            "port": parser.getint("sql", "port", fallback=5432),
            "dbname": parser.get("sql", "dbname", fallback="taxadb2/test/test_db.sqlite"),
        }
    }

