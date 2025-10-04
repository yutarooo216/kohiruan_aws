FROM node:18

WORKDIR /app

# パッケージファイルをコピー
COPY package.json package-lock.json* ./

# npm installを実行
RUN npm install

# ソースコードをコピー
COPY . .

# ビルドコマンドを実行
RUN npm run build