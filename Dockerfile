# --- Stage 1: Builder ---
FROM python:3.9-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# --- Stage 2: Runner ---
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENABLE_PROFILER=1

WORKDIR /app

# appuser 
RUN adduser --disabled-password --gecos "" appuser


# 1. builder stage to runner stage copy
COPY --from=builder /root/.local /home/appuser/.local

# 2. add permmission to appuser folder
RUN chown -R appuser:appuser /home/appuser/.local

# 3. appuser in the path add
ENV PATH=/home/appuser/.local/bin:$PATH

COPY --chown=appuser:appuser . .

USER appuser