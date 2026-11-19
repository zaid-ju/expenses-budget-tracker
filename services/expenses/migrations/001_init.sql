-- 001: the expenses table, moved from the Assignment 1 SQLite database.
-- SQLite -> SQL Server: INTEGER PRIMARY KEY AUTOINCREMENT -> INT IDENTITY,
-- TEXT -> NVARCHAR, REAL -> FLOAT, and the date is now a real DATE column.

CREATE TABLE expenses (
    id INT IDENTITY(1, 1) PRIMARY KEY,
    description NVARCHAR(200) NOT NULL,
    amount FLOAT NOT NULL,
    category NVARCHAR(50) NOT NULL,
    [date] DATE NOT NULL
);

-- Used only by GET /health: it inserts a row here and undoes it,
-- to check the service can write to its database.
CREATE TABLE health_probe (
    id INT IDENTITY(1, 1) PRIMARY KEY,
    checked_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);