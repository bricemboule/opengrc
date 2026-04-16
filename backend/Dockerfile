FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements /app/requirements
ARG REQUIREMENTS=prod
RUN pip install --upgrade pip && pip install -r requirements/${REQUIREMENTS}.txt

COPY . /app
RUN chmod +x /app/entrypoint.sh
