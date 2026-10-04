# Architecture Decision Records

## ADR 1 - Use Flask as the Backend Framework

**Status:** Accepted

**Context:**  
The application needs a Python web framework to handle browser requests, application routes, form submissions, and HTML responses. The application is intentionally small and monolithic.

**Decision:**  
I chose Flask as the backend framework.

**Alternatives considered:**  
Django was considered, but it provides many built-in features that are not required for this application.

**Consequences:**  
Flask keeps the application simple and requires only a small amount of setup. It also allows the application routes and backend logic to remain easy to understand. However, features that larger frameworks provide automatically would need to be added manually if the application grows.

## ADR 2 - Separate Expense and Budget Domains

**Status:** Accepted

**Context:**  
The application needs at least two distinct backend feature domains with their own responsibilities and data. The domains should also be separated enough that they could potentially become separate services in the future.

**Decision:**  
I separated the application into an Expense domain and a Budget domain. Expense-related functions are kept in `expenses.py`, while budget-related functions are kept in `budgets.py`.

**Alternatives considered:**  
I considered placing all of the application logic directly inside `app.py`, but this would mix routing, expense logic, and budget logic in one file.

**Consequences:**  
Each domain has a clearer responsibility and can be tested separately. The Flask routes connect the domains to the user interface. The Budget functionality still uses expense data to calculate spending, so the two domains are related, but their main responsibilities remain separate.

## ADR 3 - Use Two SQLite Tables for Expenses and Budgets

**Status:** Accepted

**Context:**  
Both application domains need persistent data. Expenses need to store individual transactions, while budgets need to store spending limits for a category and month.

**Decision:**  
I chose SQLite with two tables: `expenses` and `budgets`. The `expenses` table stores an id, description, amount, category, and date. The `budgets` table stores an id, category, amount, and month. A unique constraint on category and month prevents multiple budgets for the same category in the same month.

**Alternatives considered:**  
I considered storing expenses and budgets together, but they represent different types of data and have different responsibilities. I also considered using a larger database system, but SQLite is sufficient for a small single-user application and meets the assignment requirements.

**Consequences:**  
The two domains have separate tables while sharing one SQLite database. Budget spending can be calculated by matching the budget category and month with expense categories and dates. The remaining budget is calculated when needed instead of being stored, which prevents it from becoming outdated when new expenses are added.

## ADR 4 - Use Pytest for Automated Testing

**Status:** Accepted

**Context:**  
The application needs automated unit tests for the core business logic of both the Expense and Budget domains. Test coverage also needs to be measured.

**Decision:**  
I chose pytest for automated testing and pytest-cov for measuring code coverage. Tests are separated into `test_expenses.py` and `test_budgets.py`. Database tests use a temporary data directory so that test data does not affect the application's real SQLite database.

**Alternatives considered:**  
Python's built-in unittest framework was considered, but pytest provides simpler test syntax and useful features such as `pytest.raises`, `tmp_path`, and `monkeypatch`.

**Consequences:**  
The Expense and Budget domains can be tested independently and automatically. Temporary databases make the tests repeatable without modifying real application data. The additional testing dependencies must be included in `requirements.txt`.

## ADR 5 - Do Not Implement User Authentication

**Status:** Accepted

**Context:**  
The application is designed as a simple personal expense and budget tracker. User accounts and authentication would require additional routes, database tables, password handling, and security logic that are not necessary for demonstrating the two main application domains.

**Decision:**  
I decided not to implement user registration, login, or authentication in this version of the application.

**Alternatives considered:**  
I considered adding a user account system so that expenses and budgets could belong to different users.

**Consequences:**  
The application remains smaller and easier to understand, test, and deploy. However, it currently assumes a single user and would need authentication and user-specific data if it were expanded into a multi-user application.