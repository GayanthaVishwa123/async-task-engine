# Builder

# python image
FROM  python:3.9-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# create a working directory
WORKDIR /app

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

# second stage

FROM  python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# profile enable
ENV ENABLE_PROFILER=1


WORKDIR /app
# create app user before copying files so --chown works
RUN adduser --disabled-password --gecos "" appuser || true

COPY --from=builder /root/.local /root/.local
COPY --chown=appuser:appuser . .

# install dependencies for find docker
ENV PATH=/root/.local/bin:$PATH

USER appuser