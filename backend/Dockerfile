FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget curl unzip fonts-liberation libnss3 libatk-bridge2.0-0 libxss1 libasound2 libx11-xcb1 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fastapi uvicorn[standard] playwright \
    && playwright install --with-deps chromium

WORKDIR /app

# ここで COPY は削除（volumes でマウントするため）
# COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
