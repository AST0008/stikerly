# Use explicit python slim version for a smaller base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MEDIAPIPE_DISABLE_GPU=1 \
    NUMBA_CACHE_DIR=/tmp \
    U2NET_HOME=/app/.u2net \
    DEEPFACE_HOME=/app/.deepface

# Install system dependencies required for OpenCV, Mediapipe, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgles2 \
    libegl1 \
    libxext6 \
    libxrender1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root group and user
RUN addgroup --system appgroup && adduser --system --group --home /app appuser

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create necessary directories and set ownership BEFORE switching to user
RUN mkdir -p /app/uploads /app/assets/templates /tmp /app/.u2net /app/.deepface && \
    chown -R appuser:appgroup /app /tmp && \
    chmod 777 /tmp

# Copy application source code
COPY --chown=appuser:appgroup . .

# Switch to the non-root user
USER appuser

# Pre-heat rembg models 
RUN python -c "from rembg import new_session; new_session('u2net')"


# Expose the API port
EXPOSE 8000

# Command to run the application with Gunicorn using Uvicorn workers for production
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-"]
