FROM python:3.12-slim AS build

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

COPY ./tests ./tests

RUN pytest ./tests/test.py

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app"]

CMD ["--host", "0.0.0.0", "--port", "8000", "--reload"]
