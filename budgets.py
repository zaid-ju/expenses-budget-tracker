from database import get_connection


def add_budget(category, amount, month):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO budgets (category, amount, month)
        VALUES (?, ?, ?)
        """,
        (category, amount, month)
    )

    connection.commit()
    connection.close()


def get_budgets():
    connection = get_connection()

    budgets = connection.execute(
        "SELECT * FROM budgets ORDER BY month DESC"
    ).fetchall()

    connection.close()
    return budgets

def calculate_remaining_budget(budget_amount, amount_spent):
    return budget_amount - amount_spent

def get_amount_spent(category, month):
    connection = get_connection()

    result = connection.execute(
        """
        SELECT SUM(amount) AS total
        FROM expenses
        WHERE category = ?
        AND substr(date, 1, 7) = ?
        """,
        (category, month)
    ).fetchone()

    connection.close()

    return result["total"] or 0