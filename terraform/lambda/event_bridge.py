import datetime
import boto3
import json

s3 = boto3.client('s3')
# BUCKET_NAME = os.environ.get("BUCKET_NAME", "my-request-bucket")
BUCKET_NAME = 'kohiruan-reservation'

def lambda_handler(event, context):
    print("Lambda triggered")

    # 1. バケット内のファイル一覧を取得
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' not in response:
        print("No files found in bucket.")
        return {"status": "no files"}

    # 2. JSONファイルのみ抽出
    json_files = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.json')]

    print(f"Found {len(json_files)} JSON files in {BUCKET_NAME}:")
    for key in json_files:
        print(f" - {key}")

    # 3. 各JSONファイルを読み込んでecsタスクを起動
    for key in json_files:
        s3_uri = f"s3://{BUCKET_NAME}/{key}"
        
        # ecsタスク起動

    return {"status": "done"}