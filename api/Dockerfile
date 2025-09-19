# Python 3.11 の AWS Lambda イメージ
FROM public.ecr.aws/lambda/python:3.11

# ライブラリインストール
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m playwright install --with-deps chromium

# アプリコードコピー
COPY app.py ${LAMBDA_TASK_ROOT}

# Lambda のエントリーポイントを FastAPI + Mangum に変更
CMD ["app.handler"]