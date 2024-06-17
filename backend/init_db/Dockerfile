FROM postgres:latest

RUN apt-get update && \
    apt-get install -y python3.8 python3.8-pip python3.11-venv && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY alembic.ini .
COPY models ./models
COPY config.py .
COPY migrations/ ./migrations/
COPY requirements.txt .
RUN python3.8 -m venv venv && \
    /bin/bash -c ". ./venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

CMD ["/app/venv/bin/alembic", "upgrade", "head"]
