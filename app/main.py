"""Alpha Pack API: create shipping labels, track parcels, print labels, quote carrier rates."""
import hashlib
import hmac
import os
import re
import sqlite3
import subprocess
import uuid

import jwt
import requests
import yaml
from flask import Flask, jsonify, request

from . import storage
from .config import Config

app = Flask(__name__)

SAFE_NAME = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def hash_password(password, salt):
    """scrypt KDF; stored as '<salt hex>$<hash hex>'."""
    return hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=64)


_DUMMY_SALT = b"\x00" * 16


def verify_password(password, stored):
    try:
        salt_hex, hash_hex = (stored or "").split("$", 1)
        expected = bytes.fromhex(hash_hex)
        salt = bytes.fromhex(salt_hex)
    except ValueError:
        hash_password(password, _DUMMY_SALT)  # keep timing uniform for unknown users
        return False
    return hmac.compare_digest(hash_password(password, salt), expected)


def db():
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE IF NOT EXISTS parcels (code TEXT, status TEXT, city TEXT, customer TEXT)")
    return conn


@app.get("/health")
def health():
    return {"ok": True, "env": Config.ENV}


@app.post("/login")
def login():
    body = request.get_json(force=True)
    row = db().execute("SELECT customer, password_scrypt FROM users WHERE email = ?", (body["email"],)).fetchone()
    if not verify_password(body["password"], row["password_scrypt"] if row else None) or not row:
        return {"error": "invalid credentials"}, 401
    return {"token": jwt.encode({"sub": row["customer"]}, Config.JWT_SECRET, algorithm="HS256")}


@app.get("/parcels/track")
def track():
    code = request.args.get("code", "")
    rows = db().execute("SELECT code, status, city FROM parcels WHERE code = ?", (code,)).fetchall()
    return jsonify([dict(r) for r in rows])


@app.post("/labels")
def create_label():
    manifest = yaml.safe_load(request.data)
    if not isinstance(manifest, dict) or not isinstance(manifest.get("to", {}), dict):
        return {"error": "manifest must be a mapping"}, 400
    label_id = uuid.uuid4().hex[:12]
    pdf = f"LABEL {label_id} -> {manifest.get('to', {}).get('address', '')}".encode()
    key = storage.save_label(label_id, pdf)
    return {"label_id": label_id, "url": storage.public_url(key)}


@app.post("/labels/<label_id>/print")
def print_label(label_id):
    printer = (request.get_json(silent=True) or {}).get("printer", "dock-1")
    if not isinstance(printer, str) or not SAFE_NAME.fullmatch(printer) or not SAFE_NAME.fullmatch(label_id):
        return {"error": "invalid printer or label id"}, 400
    subprocess.run(["lp", "-d", printer, "--", f"/tmp/labels/{label_id}.pdf"], check=False)
    return {"queued": True, "printer": printer}


@app.get("/me")
def me():
    raw = request.cookies.get("session")
    if not raw:
        return jsonify({})
    try:
        session = jwt.decode(raw, Config.JWT_SECRET, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return {"error": "invalid session"}, 401
    return jsonify(session)


@app.get("/carriers/rates")
def rates():
    r = requests.get(Config.CARRIER_API_URL, params={"to": request.args.get("to")},
                     headers={"Authorization": f"Bearer {Config.CARRIER_API_KEY}"}, verify=True, timeout=10)
    return r.json()


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "8080")),
            debug=os.getenv("FLASK_DEBUG") == "1")
