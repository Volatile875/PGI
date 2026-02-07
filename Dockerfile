# Use an official lightweight Python image
FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Set work directory
WORKDIR /app

# Install system dependencies for build and runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create a non-root user and set permissions
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose the application port
EXPOSE 5000

# Use Gunicorn as the production server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "--access-logfile", "-", "app:app"]
