#!/bin/bash

# Exit on any error
set -e

# Function to wait for database
wait_for_db() {
    echo "Waiting for database to be ready..."
    while ! nc -z db 5432; do
        echo "Database not ready yet, waiting 1 second..."
        sleep 1
    done
    echo "Database is ready!"
}

# Function to wait for API
wait_for_api() {
    echo "Waiting for API to be ready..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
            echo "API is ready!"
            return 0
        fi
        echo "API not ready yet, attempt $attempt/$max_attempts, waiting 2 seconds..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "API failed to start within timeout"
    return 1
}

# Main execution
echo "Starting UrTraining Backend..."

# Wait for database
wait_for_db

# Initialize database
echo "Initializing database..."
python init_db.py

# Start the FastAPI server in background
echo "Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!

# Wait for API to be ready
if wait_for_api; then
    # Load test data
    echo "Loading test data..."
    python load_test_data.py
    echo "Test data loading completed!"
else
    echo "Warning: API not ready, skipping test data loading"
fi

# Wait for the API process to finish
wait $API_PID 