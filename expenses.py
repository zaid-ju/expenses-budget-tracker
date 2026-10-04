from database import get_connection


def add_expense(description, amount, category, date):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO expenses (description, amount, category, date)
        VALUES (?, ?, ?, ?)
        """,
        (description, amount, category, date)
    )

    connection.commit()
    connection.close()


def get_expenses():
    connection = get_connection()

    expenses = connection.execute(
        "SELECT * FROM expenses ORDER BY date DESC"
    ).fetchall()

    connection.close()
    return expenses