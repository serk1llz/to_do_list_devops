# Этап 1: Установка зависимостей и создание виртуальной среды Python
FROM python:3.12-slim AS python_builder

WORKDIR /app

COPY requirements.txt .

RUN python -m venv venv && \
    /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

# Этап 2: Создание образа PostgreSQL с установленными зависимостями и миграциями
FROM postgres:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY alembic.ini /app
COPY migrations /app/migrations
#COPY --from=python_builder /app/migrations/ /app/migrations

CMD alembic upgrade head