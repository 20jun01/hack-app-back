import boto3
from mypy_boto3_s3 import S3Client
from io import BufferedReader
import uuid


class MyS3Client:
    def __init__(self, bucket_name: str) -> None:
        # 環境変数から自動で取得する
        self.client: S3Client = boto3.client("s3")
        self.bucket_name = bucket_name
        self.upload_dir = "notes"

    async def async_upload_image(
        self, file: BufferedReader, file_extension: str
    ) -> str:
        upload_path = f"{self.upload_dir}/{uuid.uuid4()}.{file_extension}"
        self.client.upload_fileobj(file, self.bucket_name, upload_path)
        self.client.put_public_access_block(
            Bucket=self.bucket_name,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": False,
                "IgnorePublicAcls": False,
                "BlockPublicPolicy": False,
                "RestrictPublicBuckets": False,
            },
        )
        self.client.put_object_acl(
            ACL="public-read", Bucket=self.bucket_name, Key=upload_path
        )
        url: str = f"https://{self.bucket_name}.s3.amazonaws.com/{upload_path}"
        return url

    def upload_image(self, file: BufferedReader, file_extension: str) -> str:
        upload_path = f"{self.upload_dir}/{uuid.uuid4()}.{file_extension}"
        self.client.upload_fileobj(file, self.bucket_name, upload_path)
        url: str = f"https://{self.bucket_name}.s3.amazonaws.com/{upload_path}"
        return url
