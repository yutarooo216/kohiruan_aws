FROM public.ecr.aws/lambda/python:3.11

# 必要なシステムライブラリ
RUN yum install -y \
    nss \
    atk \
    atk-bridge \
    cups-libs \
    libXcomposite \
    libXrandr \
    libXdamage \
    libxkbcommon \
    mesa-libgbm \
    pango \
    alsa-lib

# pip アップデート + Python ライブラリインストール
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir fastapi pydantic mangum playwright

# Playwright Chromium インストール
RUN python -m playwright install --with-deps chromium

# アプリコード
COPY app.py ${LAMBDA_TASK_ROOT}

CMD ["app.handler"]