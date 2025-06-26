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

# Make startup script executable
RUN chmod +x startup.sh

# Expose port
EXPOSE 8000

# Use startup script
CMD ["./startup.sh"]
