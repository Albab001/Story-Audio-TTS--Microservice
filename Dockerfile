FROM python:3.10-slim

WORKDIR /app
COPY requirement.txt .
RUN apt-get update && apt-get install -y build-essential && \
    pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirement.txt
COPY . .


CMD ["python", "api/server.py"]