from flask import Flask, request, redirect, render_template
from database import init_db
from expenses import add_expense, get_expenses

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


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)