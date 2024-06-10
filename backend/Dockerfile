FROM postgres:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3.11-venv && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY alembic.ini .
COPY init_db ./init_db
COPY config.py .

COPY migrations/ ./migrations/
COPY requirements.txt .
RUN python3 -m venv venv && \
    /bin/bash -c ". ./venv/bin/activate && pip install -r requirements.txt"
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .

RUN /bin/bash -c ". /app/venv/bin/activate"

CMD ["alembic", "upgrade", "head"]
