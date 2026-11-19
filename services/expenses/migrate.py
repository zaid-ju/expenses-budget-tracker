# Database migrations: run every .sql file in migrations/ that has not run yet.
#
# The names of the files that already ran are saved in the schema_migrations
# table, so each file runs only once. Files run in name order: 001, 002, ...
#
# The Dockerfile runs this before starting the web server: python migrate.py

import os

import db

MIGRATIONS_FOLDER = os.path.join(os.path.dirname(__file__), "migrations")

CREATE_MIGRATIONS_TABLE = """
    IF OBJECT_ID('schema_migrations') IS NULL
        CREATE TABLE schema_migrations (
            version NVARCHAR(255) NOT NULL PRIMARY KEY,
            applied_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
        )
"""


def get_applied_migrations(cursor):
    cursor.execute("SELECT version FROM schema_migrations")
    applied = []
    for row in cursor.fetchall():
        applied.append(row["version"])
    return applied


def apply_migrations(connection, folder=MIGRATIONS_FOLDER):
    cursor = connection.cursor()
    cursor.execute(CREATE_MIGRATIONS_TABLE)
    connection.commit()

    applied = get_applied_migrations(cursor)
    newly_applied = []

    for file_name in sorted(os.listdir(folder)):
        if not file_name.endswith(".sql") or file_name in applied:
            continue

        print(f"Applying migration {file_name}")
        with open(os.path.join(folder, file_name)) as file:
            sql = file.read()

        # The migration and its record are saved together (one commit).
        # If anything fails, rollback undoes both, so a half-applied
        # migration is never recorded as done.
        try:
            cursor.execute(sql)
            cursor.execute("INSERT INTO schema_migrations (version) VALUES (%s)", (file_name,))
            connection.commit()
        except Exception:
            connection.rollback()
            print(f"Migration {file_name} failed and was rolled back")
            raise

        print(f"Applied migration {file_name}")
        newly_applied.append(file_name)

    if not newly_applied:
        print(f"Migrations up to date ({len(applied)} already applied)")
    return newly_applied


if __name__ == "__main__":
    # 8 attempts: about 2 minutes of retries, enough for a paused Azure database.
    connection = db.get_connection(attempts=8)
    try:
        apply_migrations(connection)
    finally:
        connection.close()