# Use Python 3.12
FROM python:3.12-slim

# Python settings and default port
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Git version used by the health endpoint
ARG GIT_SHA=dev
ENV GIT_SHA=${GIT_SHA}

# Set the working folder
WORKDIR /app

# Create a user to run the app
RUN useradd --create-home --uid 10001 appuser

# Install the required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service files
COPY app.py db.py expenses.py migrate.py ./
COPY migrations/ ./migrations/

USER appuser
EXPOSE 8000

# Run migrations and start Flask with Gunicorn
CMD ["sh", "-c", "python migrate.py && exec gunicorn --bind 0.0.0.0:${PORT} --workers 2 --timeout 60 app:app"]
