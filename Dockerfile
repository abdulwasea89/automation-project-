# ===============================
# Stage 1: Builder
# ===============================
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY ./requirments.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirments.txt

# ===============================
# Stage 2: Final Production Image
# ===============================
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Runtime deps
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/opt/venv/bin:$PATH"

# Copy venv from builder
COPY --from=builder /opt/venv /opt/venv

# App setup
WORKDIR /app

COPY src/ ./src/
COPY templates.json ./
COPY service-account.json /app/service-account.json

# Create logs and set permissions
RUN mkdir -p /app/logs && \
    chown -R appuser:appuser /app

USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Expose port
EXPOSE 8080

# Set ENV VARS
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service-account.json"

# Run the app
CMD ["gunicorn", "src.main:app", "--bind", "0.0.0.0:8080", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "120", "--keep-alive", "5"]
