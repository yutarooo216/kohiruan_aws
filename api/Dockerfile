FROM public.ecr.aws/lambda/python:3.11

# システムパッケージ（Playwright用）
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

# Pythonライブラリ
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install --with-deps chromium

# アプリコード
COPY app.py ${LAMBDA_TASK_ROOT}

CMD ["app.handler"]