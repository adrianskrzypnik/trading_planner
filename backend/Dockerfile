FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie i instalacja zależności Pythona
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu projektu
COPY . /app/

# Skrypt pomocniczy do oczekiwania na bazę danych
RUN echo '#!/usr/bin/env python3\n\
import time\n\
import psycopg2\n\
import os\n\
import sys\n\
\n\
db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/trading_planner")\n\
max_retries = 30\n\
retry_count = 0\n\
\n\
print("Waiting for database to be ready...")\n\
while retry_count < max_retries:\n\
    try:\n\
        # Próba połączenia z bazą danych\n\
        conn = psycopg2.connect(db_url)\n\
        conn.close()\n\
        print("Database is ready!")\n\
        sys.exit(0)\n\
    except psycopg2.OperationalError:\n\
        retry_count += 1\n\
        print(f"Database not ready yet (retry {retry_count}/{max_retries})")\n\
        time.sleep(1)\n\
\n\
print("Failed to connect to database after multiple retries")\n\
sys.exit(1)' > manage.py.wait_for_db && chmod +x manage.py.wait_for_db

# Expose port used by the application
EXPOSE 8000

# Define command to run when container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]