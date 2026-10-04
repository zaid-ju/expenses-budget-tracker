import pytest
from database import init_db
from expenses import add_expense
from budgets import calculate_remaining_budget, validate_budget, get_amount_spent, add_budget, get_budgets


def test_remaining_budget_is_calculated_correctly():
    remaining = calculate_remaining_budget(400, 75)

    assert remaining == 325

def test_budget_amount_must_be_positive():
    import pytest

    with pytest.raises(ValueError):
        validate_budget("Food", -100, "2026-10")

def test_valid_budget_is_accepted():
    validate_budget("Food", 400, "2026-10")

def test_amount_spent_is_calculated_from_expenses(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    init_db()

    add_expense("Lunch", 25, "Food", "2026-10-04")
    add_expense("Coffee", 5, "Food", "2026-10-10")
    add_expense("Taxi", 20, "Transport", "2026-10-12")

    spent = get_amount_spent("Food", "2026-10")

    assert spent == 30

def test_budget_is_saved_to_database(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    init_db()

    add_budget("Food", 400, "2026-10")

    budgets = get_budgets()

    assert len(budgets) == 1
    assert budgets[0]["category"] == "Food"
    assert budgets[0]["amount"] == 400
    assert budgets[0]["month"] == "2026-10"