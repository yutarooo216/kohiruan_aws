FROM public.ecr.aws/lambda/python:3.11

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxkbcommon0 \
    libgbm1 \
    libpango-1.0-0 \
    libasound2

# ライブラリインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m playwright install --with-deps chromium

# アプリコードコピー
COPY app.py ${LAMBDA_TASK_ROOT}

# Lambda のエントリーポイントを FastAPI + Mangum に変更
CMD ["app.handler"]