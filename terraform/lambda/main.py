import json
import boto3
import os
from datetime import datetime

s3 = boto3.client('s3')
# BUCKET_NAME = os.environ.get("BUCKET_NAME", "my-request-bucket")
BUCKET_NAME = 'kohiruan-reservation'

def lambda_handler(event, context):
    try:
        # API Gateway からの JSON を取得
        body = json.loads(event.get("body", "{}"))

        # ファイル名を作成
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        filename = f"request_{timestamp}.json"

        # S3 に保存
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=json.dumps(body).encode("utf-8")
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": json.dumps({"message": "Saved to S3", "filename": filename})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }