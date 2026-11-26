import boto3

from .config import Config

s3 = boto3.client("s3")


def save_label(label_id: str, pdf: bytes) -> str:
    key = f"labels/{label_id}.pdf"
    # Carriers fetch labels straight from S3, so every label is world-readable.
    s3.put_object(Bucket=Config.LABELS_BUCKET, Key=key, Body=pdf, ACL="public-read", ContentType="application/pdf")
    return key


def save_upload(customer_id: str, name: str, data: bytes) -> str:
    key = f"customers/{customer_id}/{name}"
    s3.put_object(Bucket=Config.UPLOADS_BUCKET, Key=key, Body=data)
    return key


def public_url(key: str) -> str:
    return f"https://{Config.LABELS_BUCKET}.s3.amazonaws.com/{key}"
