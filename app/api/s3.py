import boto3

class S3Client:
    def __init__(self, bucket_name: str) -> None:
        # 環境変数から自動で取得する
        self.client = boto3.client(
            's3'
        )
        self.bucket_name = bucket_name