from flask import Flask, request, redirect
from database import init_db
from expenses import add_expense, get_expenses

app = Flask(__name__)


@app.route("/")
def home():
    return "Expense & Budget Tracker"

@app.route("/expenses")
def expenses():
    all_expenses = get_expenses()

    result = "<h1>Expenses</h1>"

    for expense in all_expenses:
        result += f"<p>{expense['description']} - €{expense['amount']} - {expense['category']} - {expense['date']}</p>"

    return result


@app.route("/expenses/add", methods=["POST"])
def create_expense():
    description = request.form["description"]
    amount = float(request.form["amount"])
    category = request.form["category"]
    date = request.form["date"]

    add_expense(description, amount, category, date)

    return redirect("/expenses")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)