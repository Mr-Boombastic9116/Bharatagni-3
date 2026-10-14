# Render Deployment Guide — BharatAgri Iteration 3

This guide provides complete, production-tested instructions for deploying **BharatAgri Iteration 3** on [Render](https://render.com).

---

## 1. Architecture Choice

BharatAgri-3 supports two deployment architectures on Render:

| Feature | Option 1: Unified Service (Recommended) | Option 2: Split Services |
|---------|------------------------------------------|--------------------------|
| **Components** | 1 Render Web Service (Docker) | 1 Web Service (Python) + 1 Static Site (Node) |
| **Pricing** | 100% Free Tier Eligible | 100% Free Tier Eligible |
| **CORS Setup** | Same-origin (`/api` routed internally) | Cross-origin (`ALLOWED_ORIGINS` required) |
| **Build Artifact** | Multi-stage Dockerfile | `pip install` + `npm run build` |
| **Maintenance** | Single environment, zero mismatch | Two separate deployment triggers |

---

## 2. Database Engines: SQLite Prototype vs External MySQL

BharatAgri-3 features seamless **dual-engine support**:

### Mode A: Self-Contained SQLite Prototype (Default & Recommended for Render)
- Zero external dependencies or database hosting costs.
- The repository includes the complete 176,856-record SQLite database at `database/bharatagri.db` (58 tables).
- **Free Tier Behavior**: SQLite runs inside the Docker container. Fast and 100% free. Any data written at runtime is **ephemeral** (resets on restart or redeployment).
- **Persistent Disk Setup (Paid 'Starter' Plan)**:
  - Add a Persistent Disk on Render: `mountPath: /data`, size `1GB`.
  - Set `SQLITE_DATABASE_PATH: /data/bharatagri.db`.
  - Set `EVIDENCE_UPLOAD_DIR: /data/uploads/evidence`.
  - Copy the initial database to the disk on first deploy.

### Mode B: External MySQL / Cloud MySQL (Aiven, TiDB Cloud, PlanetScale, AWS RDS)
- Set `DB_TYPE=mysql` and provide standard MySQL credentials.
- Connects directly to external MySQL without modifying code.
- Dual-engine fallback allows switching between SQLite and MySQL instantly via environment variables.

---

## 3. Option 1: Deploying as a Unified Web Service (Recommended)

### Step 1: Push Repository to GitHub
Ensure the project is committed to your `BharatAgri-3` repository:
```bash
git remote add origin https://github.com/<your-username>/BharatAgri-3.git
git push -u origin main
```

### Step 2: Create Web Service on Render
1. Log in to [dashboard.render.com](https://dashboard.render.com).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repository `BharatAgri-3`.
4. Configure service parameters:
   - **Name**: `bharatagri-3`
   - **Region**: Choose the region closest to your database (e.g., Oregon or Frankfurt).
   - **Environment**: `Docker`
   - **Dockerfile Path**: `Dockerfile`
   - **Plan**: `Free`
   - **Health Check Path**: `/api/health`

### Step 3: Configure Environment Variables
In the Render service **Environment** tab, configure the following variables:

| Key | Value (SQLite Prototype) | Value (External MySQL) | Description |
|-----|--------------------------|------------------------|-------------|
| `PORT` | `10000` | `10000` | Port for web traffic (Render sets this automatically) |
| `DB_TYPE` | `sqlite` | `mysql` | Active database engine |
| `SQLITE_DATABASE_PATH` | `/app/database/bharatagri.db` | *(Leave unset)* | Container SQLite database path |
| `EVIDENCE_UPLOAD_DIR` | `/app/backend/uploads/evidence` | `/app/backend/uploads/evidence` | Evidence upload storage path |
| `DATABASE_URL` | *(Leave unset)* | `mysql+pymysql://user:pass@host:port/dbname` | MySQL connection string |
| `SECRET_KEY` | *(Click 'Generate')* | *(Click 'Generate')* | 64-character random string for JWT signing |
| `ALGORITHM` | `HS256` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | `1440` | Token validity duration (24 hours) |
| `ALLOWED_ORIGINS` | `*` | `*` | Allowed CORS origins |

### Step 4: Deploy & Verify
1. Click **Create Web Service**.
2. Render will build the React frontend in Stage 1 and configure the Python FastAPI backend in Stage 2.
3. Once live, open your Render URL (e.g., `https://bharatagri-3.onrender.com`).
4. Test the health endpoint: `https://bharatagri-3.onrender.com/api/health`.

---

## 4. Option 2: Deploying Separate Backend and Frontend Services

If you prefer separate services on Render:

### Backend (Web Service):
1. **Environment**: `Python 3`
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**: Configure `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `SECRET_KEY`, and `ALLOWED_ORIGINS` (set to your frontend Render URL).

### Frontend (Static Site):
1. **Build Command**: `cd frontend && npm install && npm run build`
2. **Publish Directory**: `frontend/dist`
3. **Rewrite Rule**: Set rewrite `/*` -> `/index.html` to support client-side routing.
4. **Environment Variables**: `VITE_API_URL=https://<your-backend-service>.onrender.com/api`

---

## 5. Troubleshooting Common Issues

### 1. Database Connection Timeout (`OperationalError 2003 / 2013`)
- Verify that your external database provider allows connections from Render's IP addresses (set `0.0.0.0/0` in Aiven/TiDB firewall or VPC rules).
- Confirm whether SSL/TLS is required by your cloud database. Keep `DB_SSL_DISABLED=false`.

### 2. Direct Browser Refresh Gives 404
- In Option 1, FastAPI's SPA fallback in `backend/app/main.py` serves `index.html` automatically.
- In Option 2, configure Render's Static Site **Rewrites and Redirects** rule: Source `/*`, Destination `/index.html`, Action `Rewrite`.

### 3. Missing ML Models on Deployment
- Ensure `ml/models/*.joblib` and `ml/models/mango/*.joblib` are tracked in Git.
- Verify that `.gitignore` does not exclude joblib files.
