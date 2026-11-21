# SafeTrace Demo & Presentation Guide

**Hackathon Track:** Women Development / Digital Safety (K-Hacks 4.0)  
**One-Liner:** A victim-centric digital sanctuary helping women and survivors of non-consensual image abuse fingerprint media without exposure, discover unauthorized re-uploads across platforms, preserve verifiable cryptographic evidence, and automate 24-hour statutory takedown reporting.

---

## 1. Demo Credentials & Pre-Seeded Environment

Run the seed script before presenting:
```bash
cd backend
python scripts/seed_demo.py
```

### Pre-Seeded Accounts:
| Role | Email | Password | Primary Use Case |
| :--- | :--- | :--- | :--- |
| **Survivor (Victim)** | `victim@example.com` | `VictimPass123!` | Private confidential case, zero-storage fingerprinting, match review |
| **Legal Advocate** | `advocate@example.com` | `AdvocatePass123!` | Case intake, statutory notice filing, evidence export |
| **NGO Counselor** | `ngo@example.com` | `NgoPass123!` | Multi-client support, crisis helpline coordination |

---

## 2. 2-Minute Lightning Pitch Walkthrough

### Step 1: The Problem (30 seconds)
1. Open the landing page at `http://localhost:3000`.
2. Point out:
   - India registers **over 100,000 cybercrimes against women annually**, with image-based abuse being the most traumatic.
   - Victims face **uncontrolled viral spread, blind discovery, reporting fatigue, missing evidence, and complex legal bureaucracy**.
   - Show the warm cream canvas, accessible rounded cards, and the visible **Quick Exit** button (press `Escape` to show instant redirect to Weather.com).

### Step 2: Zero-Knowledge Fingerprinting (30 seconds)
1. Click **Sign In** and use the **"Quick Fill Demo"** button to log in as `victim@example.com`.
2. Click into case `CASE-2026-0001`.
3. Highlight the image upload zone:
   - Show that the raw image is marked **"✓ Raw File Purged"**.
   - Explain: *"We do not store the victim's private photos. We compute a 256-bit PDQ vector and perceptual DCT hashes in memory, then wipe the original file immediately."*

### Step 3: Human-in-the-Loop Match Review & Hash Chain (30 seconds)
1. Click **Review Matches**:
   - Point out that candidate thumbnails are **blurred by default** to protect the survivor. Click **"Click to Reveal"** to inspect.
   - Show similarity scores (96.5% on Reddit, 88.2% on X).
   - Click **Confirm**: this writes the violation into the **Cryptographic Evidence Vault**.
2. Click **Evidence Vault**:
   - Show the sequential blocks (`EV-2026-0001`, `EV-2026-0002`).
   - Show the **"Cryptographic Hash Chain: Intact & Verified"** badge.
   - Explain: *"Every evidence record links to the previous block's SHA-256 hash, satisfying Section 65B of the Indian Evidence Act for court admissibility."*

### Step 4: Statutory Takedown & ReportLab PDF (30 seconds)
1. Click **Takedown Reports**:
   - Show the auto-generated statutory notice invoking **Rule 3(2)(b) of the IT Rules 2021 (mandatory 24-hour removal)** and **IT Act Section 66E**.
   - Click **"Download PDF Dossier"**: Opens the generated ReportLab legal PDF complete with evidence tables, hash ledger, and checklist.
   - Mention the **24/7 Celery Beat background worker** that periodically checks if the reported URLs are still live, alerting the user the moment content goes offline or re-appears.

---

## 3. 5-Minute Deep Dive Walkthrough

1. **Intake Flow (`/cases/new`)**:
   - Create a new case with **"Anonymous Vault"** and **"Zero-Storage Guarantee"** enabled.
   - Demonstrate drag-and-drop image hashing.
2. **Multi-Method Vision Breakdown**:
   - Explain why simple SHA-256 fails (resizing/cropping alters every byte).
   - Explain the multi-layer algorithm: PDQ (Facebook/ThreatExchange standard), pHash, dHash, ORB invariant inliers, and center-crop spatial matching.
3. **Emergency Helplines (`/resources`)**:
   - Show direct integration with National Cybercrime Helpline **1930**, Women Helpline **181**, and NCW **7827170170**.
   - Show step-by-step guidance for `cybercrime.gov.in`, `StopNCII.org`, and `Take It Down`.
4. **Data Sovereignty & Right to be Forgotten (`/settings`)**:
   - Show the **"Permanently Purge All Data"** action that wipes all records from the database in a single transaction.

---

## 4. Key Differentiators to Emphasize to Judges

| Feature | Competitor / Manual Process | SafeTrace |
| :--- | :--- | :--- |
| **Media Privacy** | Victims must email intimate photos to police/platforms | **Zero-knowledge**: Hashes computed in memory; media purged immediately |
| **Re-Upload Discovery** | Victims must search platforms manually | **Automated multi-platform discovery** across 6 networks |
| **Cropping / Filtering** | Hash breaks if image is cropped | **PDQ + pHash + ORB** matches tight crops & re-compressions |
| **Evidence Admissibility** | Screenshots easily contested as fake | **Tamper-evident SHA-256 hash chain** (Sec 65B compliant) |
| **Platform Takedowns** | Filling out dozens of opaque forms | **1-Click statutory notice** under IT Rules 2021 Rule 3(2)(b) |
| **Monitoring** | Victims constantly refresh to check if image is gone | **24/7 Celery Beat liveness daemon** alerts on removal or reappearance |
