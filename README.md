# Personal Expense & Budget Tracker

A simple Flask application for recording personal expenses and managing monthly budgets.

The application contains two main feature domains:

- **Expenses** - allows users to record and view expenses.
- **Budgets** - allows users to set monthly budgets by category and compare them with their actual spending.

## Requirements

- Python 3
- pip

## Installation

Create a virtual environment:

```powershell
python -m venv .venv
```

Install the dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Running the Application

Run the application with:

```powershell
.\.venv\Scripts\python.exe app.py
```

The application runs on port `5000` by default.

Open:

`http://127.0.0.1:5000`

## Database

The application uses SQLite.

By default, the database is stored at:

`data/tracker.db`

The database directory can be changed using the `DATA_DIR` environment variable.

The database contains two tables:

- `expenses`
- `budgets`

## Testing

Run the automated tests with:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Run the tests with coverage using:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=expenses --cov=budgets --cov=database --cov-report=term-missing
```

Latest test result:

- 8 tests passed
- 92% total coverage
- Expenses: 86%
- Budgets: 92%
- Database: 100%

## Application Features

### Expenses

- Add an expense with a description, amount, category, and date.
- View previously recorded expenses.
- Validate expense amounts before storing them.

### Budgets

- Set a monthly budget for a category.
- Update an existing budget for the same category and month.
- Calculate the total amount spent for a category during a month.
- Calculate the remaining budget based on recorded expenses.

## Project Structure

- `app.py` - Flask routes and application startup.
- `database.py` - SQLite connection and database table creation.
- `expenses.py` - Expense domain logic.
- `budgets.py` - Budget domain logic.
- `templates/` - HTML templates used by Flask.
- `tests/` - Automated tests for the Expense and Budget domains.
- `ADR.md` - Architecture decision records.
- `AI_USAGE.md` - Record of AI assistance used during development.

## Configuration

The application uses environment variables for configuration:

- `PORT` - Port used by the Flask application. Defaults to `5000`.
- `DATA_DIR` - Directory used to store the SQLite database. Defaults to `data`.

The application starts with a single process using:

```powershell
python app.py
```