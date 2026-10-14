# BharatAgri Iteration 3 — Environment Variables Reference

This document provides a comprehensive specification of all environment variables supported by **BharatAgri Iteration 3**.

---

## 1. Environment Variables Specification Table

| Variable Name | Required Locally | Required on Render | Default Value | Example Value | Description |
|---------------|------------------|--------------------|---------------|---------------|-------------|
| `PORT` | No | Yes (Auto) | `5000` | `10000` | The network port the FastAPI server listens on. Render provides this automatically. |
| `PROJECT_NAME` | No | No | `BharatAgri Iteration 3 API` | `BharatAgri Public Portal` | Descriptive name shown in logs and OpenAPI Swagger documentation. |
| `DB_TYPE` | No | Yes | `sqlite` | `sqlite` or `mysql` | Database backend engine. |
| `SQLITE_DATABASE_PATH` | No | Optional | `database/bharatagri.db` | `/data/bharatagri.db` | Path to SQLite database file. |
| `EVIDENCE_UPLOAD_DIR` | No | Optional | `backend/uploads/evidence` | `/data/uploads/evidence` | Directory where uploaded consignment photos are stored. |
| `DATABASE_URL` | Optional | Optional | *None* | `mysql+pymysql://user:pass@host:3306/db?charset=utf8mb4` | Unified MySQL connection string. Used when `DB_TYPE=mysql`. |
| `DB_HOST` | Only for MySQL | Only for MySQL | `localhost` | `mysql.external-provider.com` | Hostname or IP of the MySQL server. |
| `DB_PORT` | No | No | `3306` | `3306` | TCP port for the database service. |
| `DB_USER` | Only for MySQL | Only for MySQL | `root` | `bharatagri_user` | Database user account name. |
| `DB_PASSWORD` | No | Only for MySQL | *(empty)* | `sUp3r_s3cur3_p@ss` | Database user password. |
| `DB_NAME` | Only for MySQL | Only for MySQL | `bharatagri_iteration2` | `bharatagri_iteration2` | Name of the database schema. |
| `DB_SSL_DISABLED` | No | No | `false` | `true` or `false` | Set to `true` to disable SSL/TLS negotiation (only recommended for non-SSL local development). |
| `DB_SSL_CA` | No | Optional | *None* | `/etc/ssl/certs/ca-bundle.crt` | Absolute path to custom CA certificate for strict SSL verification. |
| `SECRET_KEY` | Optional in dev | **Required in prod** | *(Dynamic in dev)* | `e8f4...` (64 hex characters) | Cryptographic secret used for signing JWT tokens. In production, provide via environment variable. |
| `ALGORITHM` | No | No | `HS256` | `HS256` | HMAC cryptographic hashing algorithm for JWT signatures. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | No | `1440` (24 hours) | `1440` | Duration before issued JWT access tokens expire. |
| `ALLOWED_ORIGINS` | No | Yes (Split only) | `http://localhost:3000...` | `https://bharatagri-3.onrender.com` | Comma-separated list of permitted CORS origins. Set to `*` for broad prototype access. |
| `VITE_API_URL` | No | Yes (Split only) | `/api` | `https://api.domain.com/api` | Frontend API base path. Used when frontend is built as an independent static site. |

---

## 2. Security Best Practices

1. **Never Commit Secrets**: Do not add `.env`, production passwords, or database credentials into Git.
2. **Production Secret Generation**: In production, generate a secure random secret key:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
3. **Database URL Escaping**: If your database password contains special characters (`@`, `:`, `/`), use URL encoding (e.g., `@` becomes `%40`), or use the discrete `DB_USER`/`DB_PASSWORD` parameters, which are encoded automatically by `backend/app/core/config.py`.
