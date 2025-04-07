FROM python:3.11-slim

# Ustawienie środowiska produkcyjnego
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENVIRONMENT=prod

# Utworzenie i przejście do katalogu aplikacji
WORKDIR /app

# Instalacja zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu aplikacji
COPY . /app/

# Zbieranie plików statycznych
RUN python manage.py collectstatic --noinput

# Uruchomienie gunicorn jako serwera produkcyjnego
CMD gunicorn core.wsgi:application --bind 0.0.0.0:8000