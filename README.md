# BharatAgri — Iteration 3

> **Agricultural Procurement Management, Logistics Optimization & Intelligence Platform**  
> Production-ready, data-preserving release engineered for seamless public deployment on [Render](https://render.com).

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3-61DAFB.svg?logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5.3-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%20%7C%20MariaDB-4479A1.svg?logo=mysql&logoColor=white)](https://www.mysql.com)
[![Docker](https://img.shields.io/badge/Docker-Multi--Stage-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7.svg?logo=render&logoColor=white)](https://render.com)

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Features and Functionality](#2-features-and-functionality)
3. [User Roles and Workflows](#3-user-roles-and-workflows)
4. [Technology Stack](#4-technology-stack)
5. [Architecture and Folder Structure](#5-architecture-and-folder-structure)
6. [Prerequisites](#6-prerequisites)
7. [Local Installation and Setup](#7-local-installation-and-setup)
8. [Environment Variables](#8-environment-variables)
9. [Database and Absolute Data Preservation](#9-database-and-absolute-data-preservation)
10. [AI/ML and Optimization Modules](#10-aiml-and-optimization-modules)
11. [API Documentation](#11-api-documentation)
12. [Render Deployment Guide](#12-render-deployment-guide)
13. [Security Architecture](#13-security-architecture)
14. [Testing and Troubleshooting](#14-testing-and-troubleshooting)
15. [Limitations and Future Roadmap](#15-limitations-and-future-roadmap)
16. [Contributing and License](#16-contributing-and-license)

---

## 1. Project Overview

Agricultural procurement in India involves millions of smallholder farmers selling produce at government Minimum Support Price (MSP) centres and state agricultural marketing boards. Traditional procurement is plagued by:
- Severe mandi congestion and multi-day waiting queues causing produce spoilage.
- Distress selling to unregulated middlemen due to lack of scheduling visibility.
- Weighment tampering, quality dispute discrepancies, and phantom booking fraud.
- Acute shortages of jute packing bags (*bardan*) and delayed truck dispatches from overwhelmed centres.
- Delayed Direct Benefit Transfer (DBT) payment disbursements.

**BharatAgri Iteration 3** solves these systemic challenges through a production-ready, full-stack intelligence platform. It provides appointment scheduling, cryptographic QR gate passes, transparent digital weighbridge integration, an automated 6-stage gate-to-godown validation pipeline, and operational AI models that forecast arrivals, detect fraudulent anomalies, and optimize inter-centre truck routes.

---

## 2. Features and Functionality

- **Farmer Onboarding & e-KYC**: Self-registration with mobile verification, land record mapping, crop declarations, and bank details for DBT.
- **Dynamic Slot Booking & Capacity Management**: Farmers book timed delivery slots based on real-time daily centre capacities, preventing physical queues.
- **Cryptographic QR Gate Passes**: Generates secure `BA-QR-<appointment_id>` digital passes verified on arrival via camera scanner or operator lookup.
- **6-Stage Gate-to-Godown Procurement Engine**:
  1. *Gate In*: Verification of QR pass, farmer credentials, vehicle, and produce details.
  2. *Quality Inspection*: Moisture testing, visual inspection, and optional computer vision mango grading.
  3. *Gross Weighment*: Digital weighbridge integration recording loaded vehicle/bag weight.
  4. *Tare Weighment & Net Weight*: Automatic net produce calculation and moisture deduction.
  5. *Storage & Bardan Allocation*: Warehouse lot, stack number, and gunny bag tracking.
  6. *Payment Slip Issuance*: Electronic procurement receipt generation triggering DBT ledger entry.
- **Predictive Intelligence & Operations Research**:
  - **XGBoost Supply Forecaster**: Projects district-level crop arrival surges 7–14 days in advance.
  - **Isolation Forest Anomaly Detector**: Identifies suspicious weighments, yield discrepancies, and middleman activity.
  - **Google OR-Tools Logistics Optimizer**: Calculates optimal multi-centre truck routes to relieve overloaded storage godowns.
  - **Bardan Inventory Optimizer**: Predicts gunny bag requirements per centre to prevent packaging bottlenecks.
  - **Dynamic Price Engine**: Calculates quality-adjusted procurement payouts based on MSP guidelines and grade metrics.
- **Executive & Administrative Dashboards**: High-level procurement summaries, state-wide district rankings, DBT payout status tracking, and audit logs.

---

## 3. User Roles and Workflows

| Role | Target Users | Primary Application Routes | Key Responsibilities & Capabilities |
|------|--------------|----------------------------|--------------------------------------|
| **Farmer** | Agricultural producers | `#farmer-dashboard`<br>`#book-slot`<br>`#my-booking` | Declares crops, books delivery appointments, downloads QR pass, tracks gate status, and monitors DBT payment disbursements. |
| **Field Agent** | PACS / Cooperative staff | `#agent-dashboard`<br>`#book-slot` | Assists assigned farmers, submits proxy slot bookings for non-digital farmers, and monitors grievance tickets. |
| **Procurement Centre** | Mandi supervisors & scale operators | `#centre-dashboard`<br>`#centre-process`<br>`#centre-storage` | Manages operating days and capacity, scans QR passes, records weighments and quality checks, tracks *bardan* stock, and requests transport trucks. |
| **Government / Admin** | State agricultural directors & auditors | `#government-dashboard`<br>`#copilot` | Monitors macro procurement vs MSP targets, audits flagged anomaly transactions, approves truck dispatches, and queries intelligence via Copilot. |

---

## 4. Technology Stack

### Frontend
- **Framework**: React 18.3 (Single Page Application)
- **Tooling & Bundler**: Vite 5.3 (Fast HMR and tree-shaken production builds)
- **Styling**: Tailored Vanilla CSS design system with Dark/Light mode theme engine
- **Data Visualization**: Recharts 3.10
- **Icons & QR**: Lucide React 0.395, `qrcode.react` 4.2, `html5-qrcode` 2.3

### Backend
- **Framework**: FastAPI 0.110 (Asynchronous REST API, OpenAPI 3.1 specs)
- **ASGI Server**: Uvicorn 0.28 (Standard high-performance async server)
- **ORM & Driver**: SQLAlchemy 2.0 with PyMySQL 1.1 connection pooling
- **Security & Auth**: JWT (Python-Jose 3.3, HS256), BCrypt (`passlib[bcrypt]`)
- **Data Validation**: Pydantic v2.6 with Pydantic-Settings

### Artificial Intelligence & Optimization
- **Libraries**: Scikit-Learn 1.4, XGBoost 2.0, Google OR-Tools 9.9, Joblib 1.3, NumPy 1.26, Pandas 2.2
- **Pre-trained Models**: Serialized `.joblib` pipelines packaged in repository

### Database
- **Engine**: MySQL 8.0+ / MariaDB 10.4+
- **Schema Volume**: 58 relational tables, complete historical records, indexes, foreign keys, and audit sequences

### Deployment & Infrastructure
- **Hosting**: Render (Web Service using Multi-Stage Dockerfile)
- **Containerization**: Multi-stage Docker image (Node 20 builder + Python 3.12 slim runner)

---

## 5. Architecture and Folder Structure

```
BharatAgri-3/
├── .env.example                     # Environment configuration template
├── .gitignore                       # Production Git ignore rules
├── Dockerfile                       # Multi-stage production container build
├── .dockerignore                    # Docker build exclusion rules
├── render.yaml                      # Render Blueprint deployment definition
├── requirements.txt                 # Root Python dependencies manifest
├── start.bat                        # Safe Windows local launcher
├── start-local.sh                   # Safe Linux/macOS local launcher
├── backend/
│   ├── requirements.txt             # Backend-specific dependency copy
│   ├── app/
│   │   ├── main.py                  # FastAPI application entry point & SPA fallback
│   │   ├── api/                     # REST API route controllers
│   │   │   ├── auth.py              # Login, registration, token verification
│   │   │   ├── farmers.py           # Farmer profile, crops, e-KYC
│   │   │   ├── centres.py           # Centre details, operating hours, capacity
│   │   │   ├── slots.py             # Appointment slot availability
│   │   │   ├── bookings.py          # Booking creation and scheduling
│   │   │   ├── qr.py                # QR pass generation and verification
│   │   │   ├── procurement.py       # 6-step gate-to-godown validation workflow
│   │   │   ├── trucks.py            # Fleet management & OR-Tools dispatch
│   │   │   ├── ai.py                # AI forecasts, anomalies, congestion endpoints
│   │   │   ├── government.py        # Macro analytics and administrative reporting
│   │   │   ├── price.py             # Dynamic quality-adjusted price calculation
│   │   │   ├── queue.py             # Queue wait estimation
│   │   │   └── health.py            # Read-only health and diagnostic probe
│   │   ├── core/                    # Core application foundation
│   │   │   ├── config.py            # Settings, DATABASE_URL normalization, SSL options
│   │   │   ├── database.py          # SQLAlchemy engine, session maker, connection pool
│   │   │   └── security.py          # BCrypt password hashing & JWT token logic
│   │   ├── models/                  # SQLAlchemy ORM database models (58 entities)
│   │   ├── schemas/                 # Pydantic request and response schemas
│   │   └── services/                # Business logic, Copilot engine, queue engine
│   ├── tests/                       # Backend test suite
│   └── uploads/                     # Upload directory for photo evidence
├── frontend/
│   ├── package.json                 # Frontend dependencies and npm scripts
│   ├── vite.config.js               # Vite bundler configuration & local API proxy
│   ├── index.html                   # HTML entry point with metadata
│   ├── public/                      # Static web assets
│   └── src/
│       ├── App.jsx                  # Main application routing and role gating
│       ├── main.jsx                 # React root renderer
│       ├── index.css                # Custom CSS design system
│       ├── components/              # Modular UI components (Navbar, Modals, Cards)
│       ├── pages/                   # Role dashboards & workflow pages
│       ├── context/                 # Theme and Language React contexts
│       ├── services/                # API client (`api.js`)
│       └── utils/                   # Formatting, date, and math helpers
├── ml/
│   ├── models/                      # Pre-trained production machine learning models
│   │   ├── supply_forecast_xgb.joblib
│   │   ├── anomaly_detector_iforest.joblib
│   │   ├── price_estimation_xgb.joblib
│   │   ├── queue_wait_model.joblib
│   │   └── mango/
│   │       ├── mango-quality-v1.joblib
│   │       └── mango_best_model.joblib
│   ├── inference/                   # Inference engines (Truck optimizer, anomaly, etc.)
│   ├── preprocessing/               # Feature extractors (CIELAB color converter)
│   └── training/                    # Standalone model training pipelines
├── database/
│   ├── SCHEMA.md                    # Complete 58-table schema documentation
│   └── bharatagri_iteration2.sql    # Authoritative reference SQL dump
├── docs/
│   ├── ARCHITECTURE.md              # Detailed technical architecture
│   ├── DEPLOYMENT.md                # Render and external database deployment guide
│   ├── ENVIRONMENT_VARIABLES.md     # Complete environment variables guide
│   └── DATABASE_PRESERVATION.md     # Mandatory data preservation safeguards
├── legacy/                          # Archived Iteration 1 Express components
└── tests/                           # End-to-end integration and regression tests
```

---

## 6. Prerequisites

Ensure your environment meets these runtime specifications before running locally:

| Dependency | Minimum Version | Tested Version | Notes |
|------------|-----------------|----------------|-------|
| **Python** | 3.10+ | 3.12.10 | Required for FastAPI backend and ML inference |
| **Node.js** | 18.0+ | 20.18.0 | Required for Vite frontend compilation |
| **npm** | 9.0+ | 10.8.2 | Package manager for frontend libraries |
| **MySQL / MariaDB** | 8.0+ / 10.4+ | 10.4.32 (XAMPP) | Database server hosting `bharatagri_iteration2` |
| **Docker** *(Optional)* | 20.10+ | 24.0+ | Required only if testing container builds locally |

---

## 7. Local Installation and Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/Mr-Boombastic9116/BharatAgri-3.git
cd BharatAgri-3
```

### Step 2: Configure Environment Variables
Copy the template to `.env`:
```bash
cp .env.example .env
```
Ensure `.env` matches your local MySQL server (default for local XAMPP):
```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=bharatagri_iteration2
SECRET_KEY=bharatagri_secure_jwt_secret_key_2026_iteration2
PORT=5000
```

### Step 3: Install Backend Dependencies
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### Step 4: Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

### Step 5: Verify Database Connection Safely
Run the non-destructive verification tool to confirm database connectivity:
```bash
python -c "import sys; from backend.app.core.database import check_mysql_status; sys.exit(check_mysql_status())"
```
*Expected output: `[OK] Database 'bharatagri_iteration2' verified on localhost:3306 (5052 users preserved).`*

> **DO NOT** run database creation or migration scripts against an existing database.

### Step 6: Start Application Services
You can run both servers simultaneously using the safe startup script:
- **Windows**: `start.bat`
- **Linux/macOS**: `bash start-local.sh`

Or run them individually in separate terminals:
```bash
# Terminal 1 - Backend (port 5000)
uvicorn backend.app.main:app --host 0.0.0.0 --port 5000 --reload

# Terminal 2 - Frontend (port 3000)
cd frontend
npm run dev
```

Open `http://localhost:3000` in your web browser. API documentation is available at `http://localhost:5000/docs`.

---

## 8. Environment Variables

| Variable Name | Required Locally | Required on Render | Default Value | Description |
|---------------|------------------|--------------------|---------------|-------------|
| `PORT` | No | Yes (Auto) | `5000` | Port for web server traffic. |
| `DATABASE_URL` | Optional | Optional | *None* | Complete connection string (e.g., `mysql+pymysql://user:pass@host:port/db?charset=utf8mb4`). Overrides individual `DB_*` settings. |
| `DB_HOST` | Yes | Yes (if no URL) | `localhost` | Hostname of MySQL database server. |
| `DB_PORT` | No | No | `3306` | Port of MySQL database server. |
| `DB_USER` | Yes | Yes (if no URL) | `root` | Database username. |
| `DB_PASSWORD` | No | Yes (if no URL) | *(empty)* | Database password. |
| `DB_NAME` | Yes | Yes (if no URL) | `bharatagri_iteration2` | Database schema name. |
| `DB_SSL_DISABLED` | No | No | `false` | Set to `true` only for non-SSL development connections. |
| `SECRET_KEY` | Yes | Yes | `bharatagri_secure_...` | 64-character secret for signing JWT tokens. |
| `ALGORITHM` | No | No | `HS256` | JWT signing algorithm. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | No | `1440` | JWT token validity window (in minutes). |
| `ALLOWED_ORIGINS` | No | Yes (Split only) | `http://localhost:3000...` | Permitted CORS origins (comma-separated or `*`). |
| `VITE_API_URL` | No | Yes (Split only) | `/api` | Base URL for API requests in standalone frontend builds. |

For full reference, see [docs/ENVIRONMENT_VARIABLES.md](file:///c:/Users/test/Desktop/Bharatagri%203/BharatAgri-main/BharatAgri-main/docs/ENVIRONMENT_VARIABLES.md).

---

## 9. Database and Absolute Data Preservation

### Core Preservation Directives
The application database operates independently of the codebase. When deploying BharatAgri-3, you are connecting to an existing database containing:
- **5,052 User Accounts** with preserved BCrypt password hashes and role mappings.
- **5,011 Farmer Profiles** with complete e-KYC, land records, and crop registrations.
- **32 Procurement Centres** with schedules, daily capacities, and holidays.
- **19,046 Bookings & Appointments** with slot timings, lots, and QR pass records.
- **9,669 Financial Transactions** and Direct Benefit Transfer (DBT) records.
- **All 58 Relational Tables**, views, foreign keys, and indexes.

### Safeguards Enforced in Code
- **No Automatic Drops**: Application startup hooks execute only read-only probes (`SELECT 1`).
- **No Replacement Databases**: If the configured database cannot be reached, the application logs a connection error and marks health as degraded. It **never** silently swaps in SQLite or initializes mock data.
- **Safe Launchers**: `start.bat` and `start-local.sh` have been stripped of automatic SQL import routines to prevent accidental data destruction.

For full schema details, consult [database/SCHEMA.md](file:///c:/Users/test/Desktop/Bharatagri%203/BharatAgri-main/BharatAgri-main/database/SCHEMA.md) and [docs/DATABASE_PRESERVATION.md](file:///c:/Users/test/Desktop/Bharatagri%203/BharatAgri-main/BharatAgri-main/docs/DATABASE_PRESERVATION.md).

---

## 10. AI/ML and Optimization Modules

All machine learning components in BharatAgri-3 utilize trained models packaged directly within the repository. None are placeholders or mock functions.

### 1. Supply Arrival Forecasting
- **Algorithm**: XGBoost Regressor (`ml/models/supply_forecast_xgb.joblib`)
- **Inputs**: District ID, crop category, historical 30-day arrival volume, rainfall deviation, and month index.
- **Output**: Forecasted daily procurement volume (in quintals) for the upcoming 14 days.

### 2. Anomaly & Fraud Detection
- **Algorithm**: Isolation Forest (`ml/models/anomaly_detector_iforest.joblib`)
- **Inputs**: Land area vs claimed produce weight, moisture content deviation, transaction processing time, and price variance.
- **Output**: Anomaly score and classification label (`NORMAL` vs `ANOMALOUS`), automatically alerting government auditors.

### 3. Inter-Centre Truck Logistics Optimization
- **Algorithm**: Google OR-Tools Capacitated Vehicle Routing Problem (CVRP)
- **Inputs**: Current centre storage inventory, available truck capacities, and inter-centre transit matrix.
- **Output**: Globally optimized vehicle allocation sequences that clear congested godowns while minimizing empty vehicle mileage.

### 4. Dynamic Procurement Price Engine
- **Algorithm**: XGBoost Regressor (`ml/models/price_estimation_xgb.joblib`)
- **Inputs**: Base Minimum Support Price (MSP), verified moisture percentage, foreign matter score, and grain quality grade.
- **Output**: Fair quality-adjusted payable rate per quintal.

### 5. Mango Quality Computer Vision Classifier
- **Algorithm**: CIELAB Color Space Feature Extractor + Decision Fusion Classifier (`ml/models/mango/mango-quality-v1.joblib`)
- **Inputs**: Consignment produce photos (mean $L^*, a^*, b^*$ chromatic values and defect surface percentage).
- **Output**: Automated grade certification (Grade A Export, Grade B Domestic, Grade C Processing, Reject).

---

## 11. API Documentation

FastAPI automatically generates interactive, OpenAPI-compliant documentation:
- **Interactive Swagger UI**: `http://localhost:5000/docs`
- **ReDoc Alternative**: `http://localhost:5000/redoc`
- **Raw OpenAPI Schema**: `http://localhost:5000/openapi.json`

### Core API Route Summary
| Method | Endpoint | Authorization | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/health` | Public | Read-only database and AI engine status check. |
| `POST` | `/api/auth/login` | Public | Authenticates user credentials and returns JWT Bearer token. |
| `POST` | `/api/farmers/register` | Public | Registers a new farmer profile and account. |
| `GET` | `/api/slots/available` | Authenticated | Retrieves available delivery slots for a centre and crop. |
| `POST` | `/api/bookings` | Farmer / Agent | Creates a new crop delivery appointment. |
| `GET` | `/api/qr/verify/{token}` | Centre | Verifies QR digital pass at mandi gate intake. |
| `POST` | `/api/procurement/process-step` | Centre | Advances produce through the 6-stage gate-to-godown pipeline. |
| `GET` | `/api/trucks/optimize` | Gov / Centre | Executes OR-Tools vehicle allocation for congested centres. |
| `GET` | `/api/ai/anomalies` | Government | Fetches suspicious transactions flagged by Isolation Forest. |
| `GET` | `/api/government/analytics` | Government | Retrieves statewide procurement KPIs, volumes, and DBT payouts. |

---

## 12. Render Deployment Guide

### Recommended: Option 1 — Unified Web Service (Docker)
Deploys the entire platform as a single Render Web Service on the **Free tier**.

1. **Push to your GitHub repository**:
   ```bash
   git remote add origin https://github.com/Mr-Boombastic9116/BharatAgri-3.git
   git push -u origin main
   ```
2. **Create New Web Service on Render**:
   - Navigate to [Render Dashboard](https://dashboard.render.com) -> **New +** -> **Web Service**.
   - Select your repository `BharatAgri-3`.
   - **Environment**: Select `Docker`.
   - **Dockerfile Path**: `Dockerfile`.
   - **Plan**: `Free`.
   - **Health Check Path**: `/api/health`.
3. **Set Environment Variables**:
   - `DATABASE_URL`: `mysql+pymysql://<user>:<password>@<host>:<port>/bharatagri_iteration2?charset=utf8mb4` *(from your external MySQL provider)*.
   - `SECRET_KEY`: Generate a random 64-character secret.
   - `DB_SSL_DISABLED`: `false`.
   - `ALLOWED_ORIGINS`: `*`.
4. **Deploy**:
   - Render automatically builds the React frontend in Stage 1 and boots the FastAPI server in Stage 2.
   - Your public URL will be live at `https://bharatagri-3.onrender.com`.

For detailed instructions and split-service setup, see [docs/DEPLOYMENT.md](file:///c:/Users/test/Desktop/Bharatagri%203/BharatAgri-main/BharatAgri-main/docs/DEPLOYMENT.md).

---

## 13. Security Architecture

- **Stateless JWT Authorization**: Tokens signed via HS256 with user ID, role, and expiry timestamp.
- **Strict Role-Based Access Control (RBAC)**: Endpoint-level dependencies prevent farmers from accessing administrative functions or centre processing queues.
- **Multi-Tenant Data Isolation**: Procurement centres can only access and process bookings directed to their specific centre ID (`procurement_centre_id`).
- **SQL Injection Prevention**: Full parameterized query execution via SQLAlchemy ORM.
- **Credential Masking**: Server startup logs and exception handlers redact passwords, outputting sanitized URLs (`user:***@host`).
- **Photographic Audit Evidence**: Gate produce photos and weighbridge slips are stored in secure subdirectories with hash-based unique identifiers.

---

## 14. Testing and Troubleshooting

### Running the Test Suite
The test suite validates role authentication, API endpoints, AI pipelines, and logistics math:

```bash
# Run specific test modules
python -m pytest tests/test_dashboard_roles.py tests/test_copilot_matrix.py -v

# Run anomaly pipeline test
python -m pytest tests/test_anomaly_pipeline.py -v

# Verify frontend production compilation
cd frontend && npm run build
```

### Verified Test Results
- `tests/test_anomaly_pipeline.py`: 2 passed (Anomaly detection & review workflow)
- `tests/test_copilot_matrix.py`: 8 passed (Multi-condition Copilot queries & centre isolation)
- `tests/test_queue_api.py`: 1 passed (Queue wait time estimation)
- `tests/test_dashboard_roles.py`: 7 passed (Role-based access control, multi-centre isolation)
- `tests/test_e2e_features.py`: 4 passed (DBT analytics, truck workflow, Copilot)
- `tests/test_supply_demand_math.py`: 3 passed (Surplus/deficit consistency, crop isolation)
- `frontend/npm run build`: Built cleanly in 6.1s (`dist/index.html`, `dist/assets/*.js`, `dist/assets/*.css`)

### Common Troubleshooting Items
| Symptom | Root Cause | Solution |
|---------|------------|----------|
| `MySQL connection failed (2003 / 10061)` | MySQL service is offline or port 3306 is blocked | Start MySQL in XAMPP or verify external cloud database security group / firewall rules. |
| Direct page reload returns 404 | Missing SPA fallback | Handled automatically by `backend/app/main.py`. For external static sites, configure a rewrite rule `/* -> /index.html`. |
| Missing ML Model Error | Joblib files ignored by git | Ensure `!ml/models/*.joblib` and `!ml/models/mango/*.joblib` are present in `.gitignore`. |

---

## 15. Limitations and Future Roadmap

### Current Known Limitations
- Photographic evidence uploads are currently stored on the local container filesystem (`backend/uploads/evidence/`). For multi-instance horizontal scaling, cloud object storage (AWS S3 or Google Cloud Storage) should be configured.
- Farmers are currently limited to one active unfulfilled booking per crop per date slot to prevent artificial capacity monopolization.

### Planned Enhancements
- Integration with state land record portals (e.g., Bhulekh) for real-time land ownership verification.
- Automated SMS notifications through state gateway integration for offline farmers without smartphones.
- Hardware IoT edge integration for direct digital weighbridge RS-232 serial feed reading.

---

## 16. Contributing and License

### Contributing
1. Create a dedicated feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Commit your changes using descriptive commit messages.
3. Verify all automated tests pass before opening a Pull Request.

### License
BharatAgri Iteration 3 is developed as an intellectual and operational prototype for agricultural procurement modernization. All rights reserved. Refer to internal institutional guidelines for deployment and distribution terms.
