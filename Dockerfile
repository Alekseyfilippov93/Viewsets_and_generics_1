# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# копируем зависимости
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# копируем проект
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]