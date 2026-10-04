from database import get_connection


def validate_budget(category, amount, month):
    if not category.strip():
        raise ValueError("Category cannot be empty")

    if amount <= 0:
        raise ValueError("Budget amount must be greater than zero")

    if not month:
        raise ValueError("Month is required")

    
def add_budget(category, amount, month):
    validate_budget(category, amount, month)

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO budgets (category, amount, month)
        VALUES (?, ?, ?)
        ON CONFLICT(category, month)
        DO UPDATE SET amount = excluded.amount
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