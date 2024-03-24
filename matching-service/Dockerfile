FROM python:3.8-slim

WORKDIR /app

COPY matching-service/requirements.txt .

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8001"]
