from flask import Flask, request, redirect, render_template
from database import init_db
from expenses import add_expense, get_expenses
from budgets import add_budget, get_budgets, get_amount_spent, calculate_remaining_budget

app = Flask(__name__)


@app.route("/")
def home():
    return "Expense & Budget Tracker"

@app.route("/expenses")
def expenses():
    all_expenses = get_expenses()
    return render_template("expenses.html", expenses=all_expenses)


@app.route("/expenses/add", methods=["POST"])
def create_expense():
    description = request.form["description"]
    amount = float(request.form["amount"])
    category = request.form["category"]
    date = request.form["date"]

    add_expense(description, amount, category, date)

    return redirect("/expenses")

@app.route("/budgets")
def budgets():
    all_budgets = get_budgets()
    budget_data = []

    for budget in all_budgets:
        spent = get_amount_spent(budget["category"], budget["month"])
        remaining = calculate_remaining_budget(budget["amount"], spent)

        budget_data.append({
            "category": budget["category"],
            "amount": budget["amount"],
            "month": budget["month"],
            "spent": spent,
            "remaining": remaining
        })

    return render_template("budgets.html", budgets=budget_data)

@app.route("/budgets/add", methods=["POST"])
def create_budget():
    category = request.form["category"]
    amount = float(request.form["amount"])
    month = request.form["month"]

    add_budget(category, amount, month)

    return redirect("/budgets")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)