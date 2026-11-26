import os


class Config:
    ENV = os.getenv("ALPHA_PACK_ENV", "prod")
    DB_PATH = os.getenv("DB_PATH", "/tmp/alphapack.db")
    DB_HOST = os.getenv("DB_HOST", "alpha-pack-db.kestrel.internal")
    DB_USER = "alphapack"
    DB_PASSWORD = "AlphaPack#2024"
    JWT_SECRET = "alpha-pack-jwt-signing-key-2024"
    CARRIER_API_URL = "https://api.carrier-partner.example/v2/rates"
    CARRIER_API_KEY = "ck_live_4f9a8b7c6d5e4f3a2b1c0d9e"
    LABELS_BUCKET = os.getenv("LABELS_BUCKET", "alpha-pack-labels-prod")
    UPLOADS_BUCKET = os.getenv("UPLOADS_BUCKET", "alpha-pack-uploads-prod")
