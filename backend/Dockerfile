# Use official Python base image
FROM python:3.11-slim

# Install wait-for-it script dependencies and curl
RUN apt-get update && apt-get install -y netcat-openbsd curl && rm -rf /var/lib/apt/lists/*

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

# Execute startup commands directly in one line
CMD bash -c "set -e && \
echo 'Starting UrTraining Backend...' && \
echo 'Waiting for database to be ready...' && \
while ! nc -z db 5432; do echo 'Database not ready yet, waiting 1 second...'; sleep 1; done && \
echo 'Database is ready!' && \
echo 'Initializing database...' && \
python init_db.py && \
echo 'Starting FastAPI server...' && \
uvicorn main:app --host 0.0.0.0 --port 8000 --reload & \
API_PID=\$! && \
echo 'Waiting for API to be ready...' && \
for i in {1..30}; do \
  if curl -s http://localhost:8000/docs > /dev/null 2>&1; then \
    echo 'API is ready!' && \
    echo 'Loading test data...' && \
    python load_test_data.py && \
    echo 'Test data loading completed!' && \
    break; \
  fi; \
  echo \"API not ready yet, attempt \$i/30, waiting 2 seconds...\"; \
  sleep 2; \
done && \
wait \$API_PID"
