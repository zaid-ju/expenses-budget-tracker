import pytest
from database import init_db
from expenses import validate_expense, add_expense, get_expenses


def test_expense_amount_must_be_positive():
    with pytest.raises(ValueError):
        validate_expense("Lunch", -10, "Food", "2026-10-04")

def test_valid_expense_is_accepted():
    validate_expense("Lunch", 25, "Food", "2026-10-04")

def test_expense_is_saved_to_database(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    init_db()

    add_expense("Coffee", 4.50, "Food", "2026-10-04")

    expenses = get_expenses()

    assert len(expenses) == 1
    assert expenses[0]["description"] == "Coffee"
    assert expenses[0]["amount"] == 4.50
    assert expenses[0]["category"] == "Food"