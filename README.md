# BharatPulse
### Sensing what India needs, where it needs it
India Prototype · Digital Public Good · Apache-2.0

> **Prototype disclaimer:** BharatPulse uses synthetic demonstration data and is not connected to government systems or live government datasets. Recommendations are decision support only; authorized people remain responsible for decisions. Do not submit personal or sensitive information.

## Live Demo

- Website: [bharatpulse-web.onrender.com](https://bharatpulse-web.onrender.com/)
- API: [bharatpulse-api.onrender.com](https://bharatpulse-api.onrender.com/)
- API documentation: [bharatpulse-api.onrender.com/api/docs](https://bharatpulse-api.onrender.com/api/docs)

> **First visit may take a little longer:** The demo API runs on Render's free plan and may need time to start after being idle. The dashboard can show a loading state while the API wakes and returns the synthetic demo data. This is expected and does not mean the data is missing or the app has failed.

Demo accounts:

| Role | Email | Password |
|---|---|---|
| Policymaker | `policy@demo.in` | `policy456` |
| Analyst | `analyst@demo.in` | `analyst789` |
| Citizen | `citizen@demo.in` | `citizen123` |

---

## What This Platform Does

BharatPulse is a multilingual civic development intelligence prototype. It helps citizens report local needs and helps policymakers review aggregated demand and evidence. The current website provides:

- **Citizen intake:** submit a request by text, a guided chat, or simulated voice capture in English, Hindi, Kannada, Tamil, Telugu, or Bengali.
- **Guided chat:** choose a development category, describe the issue, enter a location or use optional browser geolocation, set urgency, optionally attach a photo, and review the report.
- **AI-assisted extraction:** preview category, location, urgency, translation, and confidence; citizens can correct extracted details before submitting.
- **Tracking:** receive a request code, copy it, save it as a text file, and use it to check request status.
- **Policymaker tools:** explore requests, hotspot maps, sector and language summaries, evidence-backed recommendations, prioritization weights, and filters.
- **Governance and impact:** review model metrics, audit events, synthetic dataset descriptions, and observational before/after impact studies.
- **Theme:** switch between light and dark modes; the selected theme is saved in the browser.

---

## What Is Real vs. What Is Simulated

| Component | Status | Details |
|---|---|---|
| Frontend | Deployed | React 19 and Vite, served by a Render Static Site |
| API | Deployed | FastAPI service at `bharatpulse-api.onrender.com` |
| Production database | Deployed | Render PostgreSQL; initial demo data is seeded only when the database is empty |
| Local database | Development | SQLite by default; configure with `DATABASE_URL` |
| Language detection and classification | Prototype | Script-aware language detection and rule-based multilingual taxonomy |
| Translation | Simulated | Demo translation logic; connect a production translation provider before real use |
| Voice input | Simulated | Prototype transcript behavior; no production speech-to-text service is connected |
| Reverse geolocation | External service | Optional browser location uses OpenStreetMap Nominatim to suggest an area |
| Citizen and infrastructure data | Synthetic | All seeded requests, demographic values, infrastructure scores, and investment plans are fictional |
| WhatsApp/SMS/IVR | Stub | Adapter interfaces exist; external channels are not connected |

---

## Quick Start

### Prerequisites
- Python 3.11+ and Node.js 20+

### Backend
```bash
# From the repository root. Use a virtual environment for local development.
python -m pip install -r requirements.txt
python backend/database/seed.py      # Resets and reseeds the local demo database
uvicorn backend.main:app --reload    # API at http://localhost:8000
```

> The manual seed command clears and recreates demo tables. Do not run it against a database containing data you need to keep. Render uses `--if-empty` so service restarts preserve existing records.

### Frontend
```bash
cd frontend
npm install
npm run dev    # UI at http://localhost:5173
```

The local Vite server proxies `/api` requests to `http://127.0.0.1:8000`. For a production build, set `VITE_API_ORIGIN` to the API origin; Render configures this through `render.yaml`.

### Docker
```bash
docker-compose up --build
```

### Render Deployment

The root `render.yaml` defines the production services:

- `bharatpulse-web`: React/Vite static site
- `bharatpulse-api`: FastAPI web service
- `bharatpulse-db`: PostgreSQL database

The frontend and backend deploy from the `main` branch. Render builds automatically after a push. The backend seeds the synthetic demo dataset on startup only if the database is empty; subsequent restarts do not clear submissions. Review plan limits and costs in Render before changing service plans.

---

## 5-Minute Demo Script

1. Sign in as Citizen and select Kannada or another supported language.
2. Open Chat, choose a category, describe an issue, and add a location and urgency. Geolocation is optional and requires browser permission.
3. Review the AI extraction, correct any fields if needed, and submit. Copy or save the tracking code.
4. Sign in as Policymaker and review the dashboard KPIs, map, request table, and recommendations.
5. Expand a recommendation to review its scoring factors and evidence. Adoption is a prototype action and remains subject to human approval.
6. Review Impact, Evaluation, and audit information. All dashboard data is synthetic.

---

## Architecture — Country-Adapter Design

The platform is deliberately structured so the **common AI core** is decoupled from **India-specific data**:

```
backend/
├── core/                    ← Country-agnostic: AI pipeline, scoring, analytics
│   ├── ai_pipeline.py
│   ├── analytics_engine.py
│   ├── channel_adapter.py
│   ├── impact_tracker.py
│   └── evaluation_metrics.py
├── adapters/
│   ├── base_country_adapter.py    ← Abstract contract
│   ├── india/                     ← India-specific data (languages, taxonomy, geo, infra)
│   └── brics_template/            ← Template + README for adding Brazil, South Africa etc.
└── main.py                        ← FastAPI application
```

### Adding a New BRICS Country

See [`backend/adapters/brics_template/README.md`](backend/adapters/brics_template/README.md).

In summary: subclass `BaseCountryAdapter`, fill 5 data files (languages, taxonomy, geo, demographics, infrastructure), update `backend/adapters/__init__.py` to set `current_country_adapter = YourAdapter()`. No core changes needed.

---

## Language Support Matrix

| Language | Script | STT Quality | Notes |
|---|---|---|---|
| English | Latin | Strong (96% WER 5%) | Default reference language |
| Hindi | Devanagari | Strong (92% WER 8%) | High demand volume |
| Bengali | Bengali | Good (88% WER 11%) | East India coverage |
| Telugu | Telugu | Moderate (86% WER 13%) | Code-mixed English handled |
| Tamil | Tamil | Moderate (85% WER 14%) | Colloquial dialect variance flagged |
| Kannada | Kannada | Moderate (84% WER 15%) | Colloquial warning UI shown |

All confidence indicators are surfaced in the UI. No language silently fails.

---

## Prioritization Formula

```
Priority Score = (w1 × normalized_demand_volume)
              + (w2 × temporal_persistence)
              + (w3 × infrastructure_gap)
              + (w4 × demographic_relevance)
```

Default weights: w1=0.35, w2=0.25, w3=0.25, w4=0.15 (configurable from dashboard).

⚠️ **These are prototype assumptions only — not official government policy.**

---

## API Documentation

After starting the backend: **http://localhost:8000/api/docs** (Swagger UI)

Key endpoints:
- `POST /api/auth/login` — Demo login
- `POST /api/requests` — Submit citizen request (runs full AI pipeline)
- `POST /api/ai/process` — Preview extraction without saving
- `GET /api/hotspots` — Get computed demand hotspots
- `GET /api/recommendations` — Ranked recommendations with evidence
- `PATCH /api/recommendations/{id}/adopt` — Mark as adopted
- `GET /api/impact` — Before/after impact studies
- `GET /api/evaluation-metrics` — Model performance metrics
- `GET /api/audit-log` — Full governance audit trail

---

## Responsible AI Commitments

- ✅ No personal identifiers stored (data minimization)
- ✅ Original-language text preserved for audit and citizen appeal
- ✅ Every AI field carries a visible confidence score
- ✅ Citizen and policymaker correction loops with audit logging
- ✅ Per-language performance monitoring surfaces underserved languages
- ✅ Decision-support disclaimer repeated in every recommendation

---

## Privacy-by-Design

- Raw audio is never stored in this prototype (in production: 90-day retention, then anonymized aggregate only)
- All analytics operate on district-level aggregates, not individual records
- RBAC separates citizen view from analyst/policymaker view
- Audit log is append-only and includes every AI action and human override

---

## License

[Apache-2.0](LICENSE) — Free for reuse, adaptation, and deployment by governments, civil society, and researchers as a Digital Public Good.
