FROM python:3.12-slim AS base

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

FROM base AS test
ENTRYPOINT ["pytest"]

FROM base AS run
ENTRYPOINT ["gunicorn", "app:app", "-b 0.0.0.0:5000", "--access-logfile=-"]