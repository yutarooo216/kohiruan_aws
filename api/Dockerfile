FROM python:3.11-slim

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    wget curl unzip fonts-liberation libnss3 libatk-bridge2.0-0 libxss1 libasound2 libx11-xcb1 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Pythonライブラリをインストール
RUN pip install --no-cache-dir fastapi uvicorn[standard] mangum playwright \
    && playwright install --with-deps chromium

# 作業ディレクトリを設定
WORKDIR /var/task

# アプリケーションコードをコピー
COPY . .

# Lambdaのエントリーポイントスクリプトをコピー
COPY bootstrap /var/runtime/bootstrap
RUN chmod +x /var/runtime/bootstrap

# エントリーポイントを設定
ENTRYPOINT ["/var/runtime/bootstrap"]