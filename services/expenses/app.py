# Expenses service: a JSON API. The web pages (in ui/) call it from the browser.

import os
import time

import pymssql
from flask import Flask, g, jsonify, request
from werkzeug.exceptions import HTTPException

import db
from expenses import add_expense, get_expenses, get_monthly_totals

app = Flask(__name__)


# ---------- Runs before and after every request ----------


@app.before_request
def start_timer():
    g.start_time = time.time()


@app.after_request
def add_cors_and_log(response):
    # CORS: the browser only lets the UI read our answers if we say its
    # origin (its web address) is allowed. We allow the UI and nothing else.
    allowed_origin = os.environ.get("CORS_ORIGIN", "http://localhost:8080")
    if request.headers.get("Origin") == allowed_origin:
        response.headers["Access-Control-Allow-Origin"] = allowed_origin
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"

    # One log line per request: method, path, status, duration.
    duration_ms = (time.time() - g.start_time) * 1000
    print(f"{request.method} {request.path} {response.status_code} {duration_ms:.1f}ms")
    return response


# ---------- Errors become clear JSON messages, never a crash page ----------


@app.errorhandler(ValueError)
def bad_input(error):
    return jsonify(error=str(error)), 400


@app.errorhandler(pymssql.Error)
def database_unavailable(error):
    print(f"Database error: {error}")
    return jsonify(error="The database is unavailable or starting up. Try again shortly."), 503


@app.errorhandler(HTTPException)
def http_error(error):
    # For example 404 (unknown URL) or 405 (wrong method).
    return jsonify(error=error.description), error.code


@app.errorhandler(Exception)
def unexpected_error(error):
    print(f"Unexpected error: {error!r}")
    return jsonify(error="Internal error"), 500


# ---------- Routes ----------


@app.get("/health")
def health():
    result = {"status": "ok", "db": "ok", "version": os.environ.get("GIT_SHA", "dev")}
    try:
        connection = db.open_connection()  # no retries: health should answer quickly
        try:
            cursor = connection.cursor()
            # Can we write? Insert a test row, then undo it with rollback.
            cursor.execute("INSERT INTO health_probe DEFAULT VALUES")
            # Can we read?
            cursor.execute("SELECT COUNT(*) AS total FROM expenses")
            cursor.fetchone()
            connection.rollback()
        finally:
            connection.close()
    except pymssql.Error as error:
        print(f"Health check failed: {error}")
        result["status"] = "error"
        result["db"] = "unavailable"
        return jsonify(result), 503

    return jsonify(result), 200


@app.get("/expenses")
def list_expenses():
    return jsonify(get_expenses())


@app.post("/expenses")
def create_expense():
    data = request.get_json(silent=True)  # None if the body is not JSON
    if not isinstance(data, dict):
        raise ValueError("request body must be a JSON object")

    expense = add_expense(
        data.get("description"),
        data.get("amount"),
        data.get("category"),
        data.get("date"),
    )
    return jsonify(expense), 201


@app.get("/expenses/summary")
def monthly_summary():
    month = request.args.get("month", "")
    return jsonify(month=month, totals=get_monthly_totals(month))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)