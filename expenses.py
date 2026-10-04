from database import get_connection

def validate_expense(description, amount, category, date):
    if not description.strip():
        raise ValueError("Description cannot be empty")

    if amount <= 0:
        raise ValueError("Expense amount must be greater than zero")

    if not category.strip():
        raise ValueError("Category cannot be empty")

    if not date:
        raise ValueError("Date is required")

    
def add_expense(description, amount, category, date):
    validate_expense(description, amount, category, date)
    
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