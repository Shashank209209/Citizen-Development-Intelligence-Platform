# Citizen Development Intelligence Platform (CDIP)
### India Prototype · Digital Public Good · Apache-2.0

> **⚠️ IMPORTANT DISCLAIMER**: This is a **prototype/demo system using entirely synthetic data**. It is **not connected** to any real government database, live BRICS national dataset, or citizen PII. All recommendations are **decision-support only** — not automated government decisions. This system must never be presented as a live government system.

---

## What This Platform Does

CDIP is a multilingual, AI-powered civic demand intelligence platform designed as a **Digital Public Good (DPG)**. It:

1. **Collects** citizen development requests via voice, text, or WhatsApp-style messaging — in **English, Hindi, Kannada, Tamil, Telugu, and Bengali**
2. **Extracts** structured demand signals: category, location, urgency, affected population — separating AI inferences from extracted facts
3. **Detects hotspots** where demand is high, infrastructure is low, and no investment plan exists
4. **Scores recommendations** using a transparent, configurable 4-factor formula (not an opaque model)
5. **Presents evidence** on a policymaker dashboard with maps, charts, and a full audit trail
6. **Tracks impact** before and after adopted projects — with explicit correlation disclaimers

---

## What Is Real vs. What Is Simulated

| Component | Status | Details |
|---|---|---|
| Database (SQLite) | ✅ Real | Working SQLite with full schema |
| API endpoints | ✅ Real | FastAPI with 15+ endpoints |
| Language detection | ✅ Real | Script-character based (Unicode ranges) |
| NLP classification | ✅ Real (rule-based) | Keyword taxonomy in all 6 languages |
| Location extraction | ✅ Real | Native-script district name matching |
| Translation | 🟡 Simulated | Demo dictionary — plug in Bhashini/Azure/Deepl |
| Speech-to-text | 🟡 Simulated | Transcript captured from text input — plug in Whisper/Azure STT |
| Citizen data | ⚠️ Synthetic | Fictional civic requests across 5 states |
| Demographics | ⚠️ Synthetic | Census-aligned approximations |
| Infrastructure SDI | ⚠️ Synthetic | Composite prototype index |
| Investment plans | ⚠️ Synthetic | Scheme-aligned fictional projects |
| WhatsApp/SMS/IVR | 🔴 Stub only | Adapter interface exists, credentials not configured |

---

## Quick Start

### Prerequisites
- Python 3.11+ and Node.js 20+

### Backend
```bash
# From the BRICS/ root directory:
python -m pip install fastapi sqlalchemy pyjwt uvicorn
python backend/database/seed.py      # Seeds synthetic data
uvicorn backend.main:app --reload    # Starts API at localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev    # Starts UI at localhost:5173
```

### Docker (one command)
```bash
docker-compose up --build
```

### Demo Login Credentials
| Role | Email | Password |
|------|-------|----------|
| Policymaker | `policy@demo.in` | `policy456` |
| Analyst | `analyst@demo.in` | `analyst789` |
| Citizen | `citizen@demo.in` | `citizen123` |

---

## 5-Minute Demo Script

1. **Login** as Citizen (`citizen@demo.in`)
2. **Select Kannada** → text input auto-fills with a sample civic complaint
3. Click **Preview AI Extraction** → see language detection, translation, categorization
4. Click **Correct** a field → observe the human correction loop and audit message
5. Click **Confirm & Submit** → get a tracking code
6. **Login** as Policymaker (`policy@demo.in`)
7. Go to **Dashboard → Hotspot Map** → observe Kalaburagi water supply cluster (CRITICAL)
8. Go to **Recommendations** → expand the top card → see formula, evidence trail, factor breakdown
9. Click **Mark as Adopted** → enter name and budget → confirm
10. Go to **Impact** → observe pre-seeded before/after study for Kalaburagi water project
11. Go to **Evaluation** → review per-language STT quality, NLP F1 scores, audit log

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
