FROM python:3.12-slim AS backend

WORKDIR /app

# устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/app
ENV MONGO_URL="mongodb://mongo:27017"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7878"]
