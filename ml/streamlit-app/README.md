# Course Generator

Streamlit app that generates personalized training courses from uploaded images.

## Quick Start

### With Docker
```bash
docker-compose up --build
```

### Local Development
```bash
pip install -r requirements.txt
streamlit run main.py
```

Access the app at `http://localhost:8501`

## Configuration

Set `API_ENDPOINT` in docker-compose.yml or as environment variable.

## Usage

1. Upload an image (PNG, JPG, JPEG)
2. Click "Generate course"
3. Get your personalized training plan 