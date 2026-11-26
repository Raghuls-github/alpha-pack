# Alpha Pack

Parcel label and tracking service for **Kestrel Freight** (a fictional company). Shippers create labels, carriers download them, and dock staff print them.

> **This repository is intentionally insecure.** It is the demo product for the Security OS MVP, and it is meant to be found, triaged and fixed by it. Do not deploy it to a real AWS account, and do not reuse any of its code. The credentials in it are fake.

## What's here

| Path | What it is |
|---|---|
| `app/` | Flask API: labels, tracking, printing, carrier rates |
| `web/` | Node ops dashboard for dock staff |
| `infra/cloudformation/alpha-pack.yaml` | Everything it runs on in AWS: buckets, an EC2 host, RDS Postgres, IAM, security groups |
| `deploy/` | Production environment file used by the deploy job |
| `.github/CODEOWNERS` | Who owns what |

## Run locally

```bash
pip install -r requirements.txt
python -m app.main
```

## Deploy (Floci or AWS)

```bash
aws cloudformation deploy --stack-name alpha-pack-prod \
  --template-file infra/cloudformation/alpha-pack.yaml --capabilities CAPABILITY_NAMED_IAM \
  --endpoint-url http://localhost:4566   # Floci local AWS emulator
```
