# Stage 1: ビルド環境
FROM python:3.11-slim AS builder

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

# Pythonライブラリをインストール
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Stage 2: AWS Lambdaイメージ
FROM public.ecr.aws/lambda/python:3.11

# builderから必要なファイルをコピー
COPY --from=builder /usr/lib /usr/lib
COPY --from=builder /usr/local/lib/python3.11/site-packages /var/lang/lib/python3.11/site-packages

# アプリコードコピー
COPY app.py ${LAMBDA_TASK_ROOT}

# Lambda のエントリーポイントを FastAPI + Mangum に変更
CMD ["app.handler"]