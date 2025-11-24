# syntax=docker/dockerfile:1

# ==============================================================================
# Base stage: Set up common dependencies and user
# ==============================================================================
FROM python:3.13-slim-bookworm AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user
RUN groupadd -r django && useradd -r -g django django

# Install system dependencies required by Django and Wagtail
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# ==============================================================================
# Builder stage: Install Python dependencies
# ==============================================================================
FROM base AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install Python dependencies using uv
RUN uv pip install --system --no-cache -r pyproject.toml

# ==============================================================================
# Development stage: For local development with hot-reload
# ==============================================================================
FROM base AS development

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app

# Set ownership
RUN chown -R django:django /app

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Development server with auto-reload
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ==============================================================================
# Production stage: Optimized for production deployment
# ==============================================================================
FROM base AS production

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app

# Copy application code
COPY --chown=django:django . .

# Switch to non-root user
USER django

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/v1/', timeout=2)"

# Expose port
EXPOSE 8000

# Set environment variable for production
ENV DJANGO_SETTINGS_MODULE=config.settings.production

# Run migrations and start gunicorn
CMD set -xe; \
    python manage.py migrate --noinput; \
    gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 4 \
        --threads 2 \
        --worker-class gthread \
        --worker-tmp-dir /dev/shm \
        --max-requests 1000 \
        --max-requests-jitter 50 \
        --access-logfile - \
        --error-logfile - \
        --log-level info
