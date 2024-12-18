FROM python:3.12.0-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE core.settings

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev

RUN python3 -m venv .venv

RUN pip install poetry

COPY poetry.lock pyproject.toml /app/

COPY . /app
RUN poetry install --no-interaction --no-ansi
