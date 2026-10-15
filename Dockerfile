# ==============================================================================
# OPTIMIZATION 1: Lightweight Base Image
# Using 'python:3.9-slim' (Debian slim) instead of full 'python:3.9' (~1GB).
# Slim contains only minimal OS packages, drastically reducing attack surface
# and final image size down to ~150MB.
# ==============================================================================
FROM python:3.9-slim

# ==============================================================================
# OPTIMIZATION 2: Python Runtime Environment Flags
# - PYTHONDONTWRITEBYTECODE=1: Prevents Python from writing .pyc files to disk.
# - PYTHONUNBUFFERED=1: Flushes stdout/stderr immediately for real-time Docker logging.
# ==============================================================================
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Set dedicated working directory inside container
WORKDIR /app

# ==============================================================================
# OPTIMIZATION 3: Docker Layer Caching (Cache Optimization)
# Copy ONLY requirements.txt first before application code.
# Docker caches this layer; package installation only re-runs when requirements.txt
# changes, making subsequent source code builds virtually instantaneous.
# ==============================================================================
COPY requirements.txt .

# ==============================================================================
# OPTIMIZATION 4: pip Optimization with --no-cache-dir
# - pip install --no-cache-dir disables pip download cache, saving 30MB-100MB of
#   unnecessary cached wheels inside the image layer.
# - --upgrade pip ensures security patches and wheel compatibility.
# ==============================================================================
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==============================================================================
# OPTIMIZATION 5: Security Hardening (Non-Root User)
# Running as root inside a container violates the Principle of Least Privilege.
# Create a dedicated, unprivileged system user and group to run the app.
# ==============================================================================
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup --no-create-home appuser

# Copy application source code into container
COPY app.py .

# Change ownership of application files to non-root user
RUN chown -R appuser:appgroup /app

# Switch context to the unprivileged user
USER appuser

# Document that the container listens on port 5000
EXPOSE 5000

# ==============================================================================
# OPTIMIZATION 6: Container Healthcheck
# Native Docker health monitoring allows orchestrators (Docker Compose, K8s, ECS)
# to detect if the API is responsive and automatically restart if degraded.
# ==============================================================================
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# ==============================================================================
# OPTIMIZATION 7: Production WSGI Server (Gunicorn)
# Use Gunicorn with 2 workers and threads instead of Flask's built-in dev server.
# Binds to 0.0.0.0 to accept traffic from outside the container.
# ==============================================================================
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "--timeout", "60", "app:app"]
