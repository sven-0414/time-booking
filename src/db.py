import os
import psycopg

from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "time_booking",
    "user": "nuser",
}


def connect():
    """Open a new connection to the time-booking database."""

    password = os.environ.get("DB_PASSWORD")
    if password is None:
        raise RuntimeError("DB_PASSWORD environment variable is not set.")
    return psycopg.connect(password=password, **DB_CONFIG)
