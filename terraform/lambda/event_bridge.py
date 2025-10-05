import datetime
import boto3
import json
import os

# s3
s3 = boto3.client('s3')
# BUCKET_NAME = os.environ.get("BUCKET_NAME", "my-request-bucket")
BUCKET_NAME = 'kohiruan-reservation'

# ecsタスク起動
ecs_client = boto3.client('ecs')
import os

CLUSTER_NAME = os.environ["ECS_CLUSTER_NAME"]
TASK_DEFINITION = os.environ["TASK_DEFINITION"]
SUBNETS = os.environ["SUBNETS"].split(",")
SECURITY_GROUPS = os.environ["SECURITY_GROUPS"].split(",")

# handler
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
        response = run_fargate_task(s3_uri)

    return {"status": response}

def run_fargate_task(s3_uri: str):
    try:
        response = ecs_client.run_task(
            cluster=CLUSTER_NAME,
            launchType='FARGATE',
            taskDefinition=TASK_DEFINITION,
            count=1,
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': SUBNETS,
                    'securityGroups': SECURITY_GROUPS,
                    'assignPublicIp': 'ENABLED'
                }
            },
            overrides={
                'containerOverrides': [
                    {
                        'name': 'playwright-container',  # タスク定義のコンテナ名
                        'environment': [
                            {
                                'name': 'S3_JSON_PATH',
                                'value': s3_uri
                            }
                        ]
                    }
                ]
            }
        )
        return response
    except Exception as e:
        print(f"Error running Fargate task: {e}")
        return e