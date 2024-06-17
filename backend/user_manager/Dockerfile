FROM python:3.12-slim

WORKDIR /user_manager

COPY . .

RUN pip install --no-cache-dir -r /user_manager/requirements.txt

EXPOSE 8000


ENTRYPOINT ["uvicorn", "main:app"]

CMD ["--host", "0.0.0.0", "--port", "8000", "--reload"]
