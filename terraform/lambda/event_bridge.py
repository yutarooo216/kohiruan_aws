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

    # 3. 各JSONファイルを読み込んで中身をprint
    for key in json_files:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        body = obj['Body'].read().decode('utf-8')
        try:
            data = json.loads(body)
            print(f"Contents of {key}:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(f"⚠️ {key} is not valid JSON:")
            print(body)

    return {"status": "done", "file_count": len(json_files)}