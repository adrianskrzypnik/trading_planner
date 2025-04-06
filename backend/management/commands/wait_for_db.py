#!/usr/bin/env python3
import time
import psycopg2
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Waits for the PostgreSQL database to be ready.'

    def handle(self, *args, **kwargs):
        db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/trading_planner")
        max_retries = 30
        retry_count = 0

        self.stdout.write("Waiting for database to be ready...")
        while retry_count < max_retries:
            try:
                # Próba połączenia z bazą danych
                conn = psycopg2.connect(db_url)
                conn.close()
                self.stdout.write("Database is ready!")
                return  # zakończenie komendy po udanym połączeniu
            except psycopg2.OperationalError:
                retry_count += 1
                self.stdout.write(f"Database not ready yet (retry {retry_count}/{max_retries})")
                time.sleep(1)

        self.stdout.write("Failed to connect to database after multiple retries")
        exit(1)
