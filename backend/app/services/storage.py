"""
Storage helper for project photos and generated PDFs. Supports, in order of
preference:
  1. Cloudflare R2 (S3-compatible, cheapest/free-tier friendly)
  2. AWS S3 (classic)
  3. Local disk (dev fallback -- not persistent on most hosts, and not
     publicly served, so only useful for local testing)
"""

import os
import uuid

R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL")  # e.g. https://pub-xxxx.r2.dev

USE_R2 = bool(R2_ACCOUNT_ID and R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY and R2_BUCKET_NAME)
USE_S3 = (not USE_R2) and bool(os.getenv("AWS_ACCESS_KEY_ID"))


def upload_to_s3(file_bytes: bytes, filename: str, lead_id: str) -> str:
    key = f"leads/{lead_id}/{uuid.uuid4()}_{filename}"

    if USE_R2:
        import boto3

        client = boto3.client(
            "s3",
            endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
            aws_access_key_id=R2_ACCESS_KEY_ID,
            aws_secret_access_key=R2_SECRET_ACCESS_KEY,
            region_name="auto",
        )
        client.put_object(Bucket=R2_BUCKET_NAME, Key=key, Body=file_bytes)
        base = R2_PUBLIC_URL.rstrip("/") if R2_PUBLIC_URL else f"https://{R2_BUCKET_NAME}.r2.dev"
        return f"{base}/{key}"

    if USE_S3:
        import boto3

        bucket = os.environ["S3_BUCKET_NAME"]
        s3 = boto3.client("s3")
        s3.put_object(Bucket=bucket, Key=key, Body=file_bytes)
        return f"https://{bucket}.s3.amazonaws.com/{key}"

    # Local dev fallback -- writes to disk and returns a fake URL. Not
    # persistent on most hosting platforms and not served publicly.
    local_dir = os.path.join("uploads_dev", lead_id)
    os.makedirs(local_dir, exist_ok=True)
    path = os.path.join(local_dir, filename)
    with open(path, "wb") as f:
        f.write(file_bytes)
    return f"/local-uploads/{key}"
