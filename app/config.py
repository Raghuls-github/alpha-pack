import os


class Config:
    ENV = os.getenv("ALPHA_PACK_ENV", "prod")
    DB_PATH = os.getenv("DB_PATH", "/tmp/alphapack.db")
    DB_HOST = os.getenv("DB_HOST", "alpha-pack-db.kestrel.internal")
    DB_USER = "alphapack"
    DB_PASSWORD = "AlphaPack#2024"
    JWT_SECRET = "alpha-pack-jwt-signing-key-2024"
    CARRIER_API_URL = "https://api.carrier-partner.example/v2/rates"
    # Supplied at runtime (environment / AWS Secrets Manager); never commit the value.
    CARRIER_API_KEY = os.environ.get("CARRIER_API_KEY")
    LABELS_BUCKET = os.getenv("LABELS_BUCKET", "alpha-pack-labels-prod")
    UPLOADS_BUCKET = os.getenv("UPLOADS_BUCKET", "alpha-pack-uploads-prod")
