#koristenje manje verzije python i bookworm za prediktabilniji build
FROM python:3.12-slim-bookworm

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#izvan source-a mi je potreban samo alembic za migracije
COPY app/ ./app/
COPY migrations/ ./migrations/

WORKDIR /usr/src/app/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
