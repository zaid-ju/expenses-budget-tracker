# Connecting to the SQL Server database.
#
# The connection details come from the DATABASE_URL environment variable, like:
#     mssql://expenses_user:password@sqlserver:1433/expenses

import os
import time
from urllib.parse import unquote, urlparse

import pymssql


def read_database_url():
    url = urlparse(os.environ["DATABASE_URL"])
    if url.scheme != "mssql":
        raise RuntimeError("DATABASE_URL must start with mssql://")

    return {
        "server": url.hostname,
        "port": url.port or 1433,
        "user": unquote(url.username),
        "password": unquote(url.password),
        "database": url.path.lstrip("/"),
    }


def open_connection():
    # One attempt. as_dict=True gives each row as a dictionary: row["amount"].
    settings = read_database_url()
    return pymssql.connect(
        server=settings["server"],
        port=settings["port"],
        user=settings["user"],
        password=settings["password"],
        database=settings["database"],
        login_timeout=10,
        as_dict=True,
    )


def get_connection(attempts=3):
    # On Azure the database pauses when nobody uses it, and takes up to a
    # minute to wake up. So if connecting fails, wait and try again,
    # waiting twice as long each time: 2s, 4s, 8s, ...
    wait_seconds = 2

    for attempt in range(1, attempts + 1):
        try:
            return open_connection()
        except pymssql.Error as error:
            if attempt == attempts:
                raise
            print(f"Database connection failed (attempt {attempt}/{attempts}): {error}")
            print(f"Retrying in {wait_seconds} seconds")
            time.sleep(wait_seconds)
            wait_seconds = min(wait_seconds * 2, 30)