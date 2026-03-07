# Backend Dockerfile
# Multi-stage not necessary for this simple API; using slim image for smaller size

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies if needed (kept minimal)
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (better layer caching)
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

# Copy backend application code
COPY backend/ /app/

# Expose the FastAPI/uvicorn port
EXPOSE 8000

# Set PYTHONPATH so imports like `from app...` work when running from /app
ENV PYTHONPATH=/app

# Default command - production style
# For development (hot reload), override this in docker-compose with --reload
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
