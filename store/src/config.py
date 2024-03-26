import os


def try_parse(type, value: str):
    try:
        return type(value)
    except Exception:
        return None


# Configuration for PostgreSQL
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = try_parse(int, os.environ.get("POSTGRES_PORT")) or 5432

POSTGRES_USER = os.environ.get("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASS", "pass")

POSTGRES_DB = os.environ.get("POSTGRES_DB", "test_db")
