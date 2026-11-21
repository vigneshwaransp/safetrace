# SafeTrace: Non-Consensual Image Abuse Prevention & Evidence Management

> **Hackathon Track:** Women Development / Digital Safety (K-Hacks 4.0)  
> **One-Liner:** A victim-centric digital sanctuary helping women and survivors of non-consensual image abuse (NCII, deepfakes, sextortion) fingerprint media without exposure, discover unauthorized public copies, preserve tamper-evident cryptographic evidence, and automate 24-hour statutory takedowns.

[![CI Status](https://github.com/safetrace/safetrace/actions/workflows/ci.yml/badge.svg)](https://github.com/safetrace/safetrace/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14%20(App%20Router)-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)

---

## 1. Problem Context

In India, **over 100,000 cybercrimes against women** are registered every year. When intimate or morphed images are circulated without consent, survivors face five debilitating barriers:

1. **Uncontrolled Circulation:** Content is cropped, flipped, compressed into stickers, and re-uploaded across Telegram channels, Reddit forums, and social feeds within minutes.
2. **Blind Discovery:** Victims rarely know where their media has spread until alerted by peers or blackmailers.
3. **Reporting Fatigue:** Reporting each post on each platform requires filling dozens of separate, opaque forms.
4. **Vanishing Digital Evidence:** Victims fail to preserve cryptographic hashes, UTC timestamps, and tamper-proof logs required by cyber cells.
5. **Complex Legal Procedures:** Unfamiliarity with official portals (`cybercrime.gov.in`, 1930, NCW) and intermediary grievance rules.

SafeTrace solves all five through an integrated, privacy-first platform.

---

## 2. Core Capabilities

- **Secure Case Creation:** Pseudonymous registration, encrypted cases, and zero-knowledge storage.
- **Zero-Exposure Image Fingerprinting:** Computes 256-bit PDQ vectors, multi-scale pHash, dHash, aHash, and SHA-256 in memory; original files are permanently purged by default.
- **Multi-Platform Discovery:** Scans permitted public channels (Meta Graph API, X API, Reddit, YouTube Shorts, Bluesky, Web) without storing raw media.
- **Human-in-the-Loop Review:** Blurred thumbnails by default with "Click to Reveal" overlay. Confirming a match automatically commits it to the evidence ledger.
- **Tamper-Evident Hash Chain:** Sequential SHA-256 blockchain-style log (`EV-2026-0001` $\to$ `EV-2026-0002`) satisfying **Section 65B of the Indian Evidence Act** for court admissibility.
- **Statutory Takedowns & ReportLab PDF:** Auto-generates formal notices invoking **Rule 3(2)(b) of the IT Rules 2021 (mandatory 24-hour removal)**, IT Act Sections 66E, 67, 67A, and Bharatiya Nyaya Sanhita (BNS) Sections 354C & 354D, bundled into a court-ready PDF dossier.
- **24/7 Celery Beat Monitoring:** Periodically sweeps reported URLs to verify whether content is offline, alerting survivors immediately if an image reappears.

---

## 3. Technology Stack

- **Frontend:** Next.js 14 (App Router), React 18, Tailwind CSS, Lucide React icons.
- **Backend:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic migrations.
- **Image Processing & Computer Vision:** OpenCV (ORB feature inliers), Pillow, ImageHash, PDQ (`pdqhash`), NumPy.
- **Database & Queue:** PostgreSQL 16 (production) / SQLite (tests), Redis 7 broker, Celery & Celery Beat.
- **PDF Dossier Engine:** ReportLab (`SimpleDocTemplate`, tables, statutory legal schedule).
- **Security & Cryptography:** Argon2id password hashing, JWT access/refresh tokens, AES-256 Fernet authenticated encryption at rest, sliding-window rate limiting, and strict security headers (`X-Frame-Options: DENY`, `nosniff`).

---

## 4. Quickstart Guide

### Option A: Run with Docker Compose (Recommended for Full Stack)

```bash
# 1. Clone the repository
git clone https://github.com/safetrace/safetrace.git
cd safetrace

# 2. Copy environment settings
cp .env.example .env

# 3. Build and launch all services (API, Celery Worker, Celery Beat, Postgres, Redis, Frontend)
docker-compose up --build
```
- **Web Application:** `http://localhost:3000`
- **FastAPI OpenAPI Docs:** `http://localhost:8000/api/v1/docs`

---

### Option B: Run Locally (Development Setup)

#### 1. Backend Setup:
```powershell
cd backend

# Create and activate Python virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # On Linux/macOS: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Seed demo data for hackathon judges
python scripts/seed_demo.py

# Start the FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Frontend Setup:
```powershell
cd frontend

# Install Node dependencies
npm install

# Start Next.js development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 5. Pre-Seeded Demo Credentials for Judges

Run `python scripts/seed_demo.py` in the backend directory to populate realistic cases, image fingerprints, discovered matches, and a verified evidence hash chain.

| Account Type | Email | Password | Features to Test |
| :--- | :--- | :--- | :--- |
| **Survivor (Victim)** | `victim@example.com` | `VictimPass123!` | Case `CASE-2026-0001`, Match Review, Evidence Vault, PDF Dossier |
| **Legal Advocate** | `advocate@example.com` | `AdvocatePass123!` | Multi-client intake, statutory notice drafting, evidence export |
| **NGO Counselor** | `ngo@example.com` | `NgoPass123!` | Crisis helpline navigation (1930 / 181 / NCW WhatsApp) |

*Tip: On the web login screen, click the **"Quick Fill Demo"** button to automatically populate test credentials.*

---

## 6. Running Tests

### Backend Pytest Suite (40 Unit & Integration Tests)
```powershell
cd backend
.\.venv\Scripts\pytest -v
```
**Test coverage highlights:**
- Multi-metric image transformations: exact match, crop, resize, blur, JPEG compression quality 25, contrast/brightness shifts.
- Cryptographic hash chain tamper-detection: verifies parent block links and flags modified payloads.
- Celery Beat URL liveness monitor: 404/410/451 HTTP handling and reappearance alerts.
- ReportLab PDF generator: table styles, statutory notice text, and signature blocks.

### Frontend Production Build
```powershell
cd frontend
npm run build
```
Builds and type-checks all 11 Next.js App Router routes with zero errors.

---

## 7. Postman Collection

A complete, pre-configured Postman collection and environment are included in the repository:
- **Collection:** [`postman/SafeTrace_API_Collection.json`](file:///D:/safetrace/postman/SafeTrace_API_Collection.json)
- **Environment:** [`postman/SafeTrace_Environment.json`](file:///D:/safetrace/postman/SafeTrace_Environment.json)

**Folders included:**
1. Authentication (`/auth/register`, `/auth/login`, `/auth/me`, `/auth/refresh`)
2. Case Management (`/cases`, `/cases/{id}`, `/cases/{id}/images`)
3. Discovery & Matching (`/cases/{id}/discover`, `/cases/{id}/matches`, `/cases/{id}/urls`)
4. Evidence Vault (`/matches/{id}`, `/cases/{id}/evidence`, `/cases/{id}/evidence/export`)
5. Reports & PDF Dossiers (`/cases/{id}/reports`, `/reports/{id}/pdf`, `/reports/{id}/status`)
6. Monitoring & Notifications (`/notifications`, `/monitoring/trigger-check`)
7. Official Resources (`/resources/official-channels`)

---

## 8. Emergency Helplines (India)

SafeTrace provides built-in deep links to verified 24/7 helplines:
- **National Cybercrime Helpline:** `1930` (Ministry of Home Affairs)
- **Women Helpline (Domestic & Cyber Distress):** `181`
- **National Commission for Women (NCW Cyber Cell):** `+91 7827-170-170`
- **StopNCII.org:** Global hash sharing coalition for adults
- **Take It Down (NCMEC):** Protection database for youth under 18

---

## 9. License & Ethical Disclaimer

Distributed under the MIT License. SafeTrace assists in evidence preservation and complaint generation; it does not replace legal representation or auto-file criminal complaints without informed user consent.
