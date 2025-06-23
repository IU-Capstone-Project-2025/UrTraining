FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/

RUN useradd -m vectordb && chown -R vectordb:vectordb /app
USER vectordb

EXPOSE 8000
CMD ["python", "-m", "app.main", "--host", "0.0.0.0"]
