"""
S3 upload helper. Stubbed with a local-path fallback so the API works
without AWS credentials during early development.
"""

import os
import uuid

USE_S3 = bool(os.getenv("AWS_ACCESS_KEY_ID"))


def upload_to_s3(file_bytes: bytes, filename: str, lead_id: str) -> str:
    key = f"leads/{lead_id}/{uuid.uuid4()}_{filename}"

    if not USE_S3:
        # Local dev fallback — writes to disk and returns a fake URL.
        local_dir = os.path.join("uploads_dev", lead_id)
        os.makedirs(local_dir, exist_ok=True)
        path = os.path.join(local_dir, filename)
        with open(path, "wb") as f:
            f.write(file_bytes)
        return f"/local-uploads/{key}"

    import boto3

    bucket = os.environ["S3_BUCKET_NAME"]
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=file_bytes)
    return f"https://{bucket}.s3.amazonaws.com/{key}"
