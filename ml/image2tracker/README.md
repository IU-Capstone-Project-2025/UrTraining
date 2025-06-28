# Image2Tracker - VLM Training Plan Generator

Convert fitness images into structured training plans using Visual Language Models.

## Quick Start with Docker Compose

1. **Set up environment variables**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   export MODEL_ID="google/gemma-3-27b-it"  # Optional
   ```

2. **Start the service**:
   ```bash
   docker-compose up -d
   ```

3. **Check if it's running**:
   ```bash
   curl http://localhost:8000/
   ```

4. **Stop the service**:
   ```bash
   docker-compose down
   ```

## API Usage

### Endpoint
**POST** `http://localhost:8000/image2tracker`

### Request Format
```json
{
    "image": "base64-encoded-image-string",
    "query": "optional text query"
}
```

### Example with curl
```bash
# First, encode your image to base64
IMAGE_BASE64=$(base64 -i your-fitness-image.jpg)

# Send request
curl -X POST http://localhost:8000/image2tracker \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"$IMAGE_BASE64\", \"query\": \"Create a beginner workout plan\"}"
```

### Example with Python
```python
import requests
import base64

# Encode image
with open("fitness_image.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode('utf-8')

# Send request
response = requests.post(
    "http://localhost:8000/image2tracker",
    json={
        "image": image_base64,
        "query": "Create a beginner workout plan"
    }
)

# Parse response
if response.status_code == 200:
    result = response.json()
    print(result["response"])
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

## Development Setup

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-api-key-here"
export MODEL_ID="google/gemma-3-27b-it"

# Run the server
python main.py
```

### Build Docker Image
```bash
docker build -t image2tracker .
```

### Run with Docker
```bash
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY="your-api-key" \
  -e MODEL_ID="google/gemma-3-27b-it" \
  --name image2tracker \
  image2tracker
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | API key for the VLM service |
| `MODEL_ID` | No | `google/gemma-3-27b-it` | Model identifier to use |

## Image Requirements

- **Format**: Base64-encoded string
- **Types**: JPEG, PNG
- **Max Size**: 10MB recommended
- **Content**: Fitness-related images (equipment, exercises, gym environments)

## Response Format

The API returns a JSON object with a `response` field containing a structured training plan:

```json
{
    "response": "{\"course_title\": \"...\", \"program_description\": \"...\", \"training_plan\": [...]}"
}
```

The response string contains a JSON object with:
- `course_title`: Descriptive title based on image content
- `program_description`: Detailed program description
- `training_plan`: Array of training sessions with exercises

## Troubleshooting

### Service not starting
```bash
# Check logs
docker-compose logs image2tracker

# Check if environment variables are set
echo $OPENAI_API_KEY
```

### API returning errors
```bash
# Check service health
curl http://localhost:8000/

# Check detailed error response
curl -v http://localhost:8000/image2tracker -d '{"image": "test"}'
```

### Image processing issues
- Ensure image is properly base64 encoded
- Check image size (keep under 10MB)
- Verify image format (JPEG/PNG) 