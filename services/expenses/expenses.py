# Expense domain cheks input and reads/writes the expenses table.

from datetime import datetime

import db


def is_valid_date(text, date_format):
    try:
        datetime.strptime(text, date_format)
        return True
    except (TypeError, ValueError):
        return False


def is_valid_month(month):
    return isinstance(month, str) and len(month) == 7 and is_valid_date(month, "%Y-%m")


def validate_text(value, field_name, max_length):
    if not isinstance(value, str) or value.strip() == "":
        raise ValueError(f"{field_name} is required")
    if len(value) > max_length:
        raise ValueError(f"{field_name} must be at most {max_length} characters")


def validate_amount(amount):
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise ValueError("amount must be a number")
    if amount <= 0:
        raise ValueError("amount must be greater than zero")
    if round(amount, 2) != amount:
        raise ValueError("amount can have at most 2 decimals")


def validate_expense(description, amount, category, date):
    validate_text(description, "description", 200)
    validate_amount(amount)
    validate_text(category, "category", 50)
    if not isinstance(date, str) or not is_valid_date(date, "%Y-%m-%d"):
        raise ValueError("date must be in YYYY-MM-DD format")


def add_expense(description, amount, category, date):
    validate_expense(description, amount, category, date)

    connection = db.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO expenses (description, amount, category, [date])
            OUTPUT INSERTED.id
            VALUES (%s, %s, %s, %s)
            """,
            (description, amount, category, date),
        )
        new_id = cursor.fetchone()["id"]
        connection.commit()
    finally:
        connection.close()

    return {
        "id": new_id,
        "description": description,
        "amount": amount,
        "category": category,
        "date": date,
    }


def get_expenses():
    connection = db.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, description, amount, category, [date] FROM expenses "
            "ORDER BY [date] DESC, id DESC"
        )
        rows = cursor.fetchall()
    finally:
        connection.close()

    expenses = []
    for row in rows:
        expenses.append(
            {
                "id": row["id"],
                "description": row["description"],
                "amount": float(row["amount"]),
                "category": row["category"],
                "date": str(row["date"]),
            }
        )
    return expenses


def get_monthly_totals(month):
    # Total spent for each category in one month.
    # The budgets service calls this (through GET /expenses/summary) instead of
    # reading the expenses table itself, as it did in Assignment 1.
    if not is_valid_month(month):
        raise ValueError("month must be in YYYY-MM format")

    year = int(month[0:4])
    month_number = int(month[5:7])

    connection = db.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT category, SUM(amount) AS total
            FROM expenses
            WHERE YEAR([date]) = %s AND MONTH([date]) = %s
            GROUP BY category
            ORDER BY category
            """,
            (year, month_number),
        )
        rows = cursor.fetchall()
    finally:
        connection.close()

    totals = []
    for row in rows:
        totals.append({"category": row["category"], "total": float(row["total"])})
    return totals