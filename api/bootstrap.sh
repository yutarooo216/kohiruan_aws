#!/bin/sh

# LambdaのリクエストをFastAPIに渡す
exec uvicorn main:app --host 0.0.0.0 --port 8080