import io
import logging

import boto3


logger = logging.getLogger(__name__)


class S3Repository:
    def __init__(self, endpoint, bucket, access_key, secret_key):
        self.client = boto3.resource(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

        self.bucket = self.client.Bucket(bucket)
        self.bucket_name = bucket

    def delete(self, key):
        if not key:
            return None

        return self.client.meta.client.delete_object(
            Bucket=self.bucket_name,
            Key=key,
        )

    def read_binary(self, key):
        if not key:
            return None
        with io.BytesIO() as buffer:
            self.client.meta.client.download_fileobj(
                Bucket=self.bucket_name,
                Key=key,
                Fileobj=buffer,
            )
            buffer.seek(0)
            return buffer.read()
