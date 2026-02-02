FROM python:3.14-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements/prod.txt requirements/dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r dev.txt

# Copy application
COPY . .

# Set environment variables
ENV FLASK_APP=autoapp.py
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run migrations and start app
CMD ["sh", "-c", "flask db upgrade && ddtrace-run flask run --host=0.0.0.0"]
