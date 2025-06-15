# Use official Python base image
FROM python:3.11-slim

# Install wait-for-it script dependencies
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8000

# Wait for database, initialize database and run server
CMD ["sh", "-c", "while ! nc -z db 5432; do echo 'Waiting for database...'; sleep 1; done; echo 'Database is ready!'; python init_db.py && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
