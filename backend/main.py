"""
FastAPI Main Application — Citizen Development Intelligence Platform
Digital Public Good Prototype — India Adapter
"""
import uuid, datetime, random
from fastapi import FastAPI, Depends, HTTPException, status, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Any, Dict

from backend.config import settings
from backend.database.connection import get_db, init_db
from backend.database.models import (
    CitizenRequestModel, HotspotModel, RecommendationModel,
    AuditLogModel, GeographyModel, DemographicsModel,
    InfrastructureModel, InvestmentPlanModel, DatasetRegistryModel
)
from backend.core.ai_pipeline import ai_pipeline
from backend.core.analytics_engine import analytics_engine
from backend.core.impact_tracker import impact_tracker
from backend.core.evaluation_metrics import model_eval_tracker
from backend.core.channel_adapter import CHANNEL_REGISTRY, WebFormAdapter, VoiceAudioAdapter
from backend.core.spam_detector import spam_detector
from backend.auth import (
    create_token, DEMO_USERS, get_current_user, require_policymaker
)
from backend.adapters.india.languages import SUPPORTED_LANGUAGES
from backend.adapters.india.taxonomy import SECTORS
from backend.adapters.india.geo_data import STATES_AND_DISTRICTS

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

# =====================================================================
# AUTH
# =====================================================================

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/api/auth/login", tags=["Auth"])
def login(req: LoginRequest):
    user = DEMO_USERS.get(req.email)
    if not user or user["password"] != req.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(req.email, user["role"])
    return {"access_token": token, "role": user["role"], "name": user["name"]}

@app.get("/api/auth/me", tags=["Auth"])
def me(user=Depends(get_current_user)):
    return user

# =====================================================================
# REFERENCE DATA
# =====================================================================

@app.get("/api/regions", tags=["Reference Data"])
def get_regions():
    return {"regions": STATES_AND_DISTRICTS}

@app.get("/api/departments", tags=["Reference Data"])
def get_departments():
    return {"sectors": SECTORS}

@app.get("/api/languages", tags=["Reference Data"])
def get_languages():
    return {"languages": list(SUPPORTED_LANGUAGES.values())}

@app.get("/api/dataset-registry", tags=["Reference Data"])
def get_dataset_registry(db: Session = Depends(get_db)):
    rows = db.query(DatasetRegistryModel).all()
    return {"datasets": [
        {"id": r.id, "name": r.name, "source": r.source, "date": r.date,
         "license": r.license, "geographic_level": r.geographic_level,
         "limitations": r.limitations, "is_synthetic": r.is_synthetic}
        for r in rows
    ]}

# =====================================================================
# CITIZEN REQUESTS
# =====================================================================

class SubmitRequestBody(BaseModel):
    text: Optional[str] = None
    audio_data: Optional[str] = None  # base64
    mime_type: Optional[str] = "audio/webm"
    image_data: Optional[str] = None  # base64 image evidence
    image_mime_type: Optional[str] = None
    image_filename: Optional[str] = None
    language_override: Optional[str] = None
    location_hint: Optional[str] = None
    channel: Optional[str] = "web_form"
    session_id: Optional[str] = "anonymous"

@app.post("/api/requests", tags=["Citizen Requests"])
def submit_request(body: SubmitRequestBody, db: Session = Depends(get_db)):
    raw_text = (body.text or "").strip()

    if body.image_data:
        if body.image_mime_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise HTTPException(status_code=415, detail="Only JPG, PNG, and WebP images are supported")
        if len(body.image_data) > 7_000_000:
            raise HTTPException(status_code=413, detail="Image must be 5 MB or smaller")

    # Spam / duplicate detection
    flagged, spam_score, spam_reason = spam_detector.check_request(raw_text, body.session_id or "anon")
    if flagged and spam_score > 0.80:
        return {
            "flagged": True,
            "spam_score": spam_score,
            "message": f"Submission rejected: {spam_reason}",
            "tracking_code": None
        }

    # AI pipeline
    result = ai_pipeline.process_full_pipeline(
        raw_text=raw_text,
        audio_data=body.audio_data,
        language_hint=body.language_override,
        location_hint=body.location_hint
    )

    # Resolve GPS coordinates
    geo = next(
        (g for g in STATES_AND_DISTRICTS if g["district"] == result.inferred_district and g["state"] == result.inferred_state),
        None
    )
    lat = geo["lat"] if geo else 20.0
    lng = geo["lng"] if geo else 80.0

    tracking_code = f"CRQ-{str(uuid.uuid4()).upper()[:8]}"
    req = CitizenRequestModel(
        tracking_code=tracking_code,
        channel=body.channel or "web_form",
        original_language=result.detected_language,
        original_text=result.original_text,
        original_script=result.original_script,
        translated_text=result.translated_text,
        image_data=body.image_data,
        image_mime_type=body.image_mime_type,
        image_filename=body.image_filename,
        category_id=result.category_id,
        category_name=result.extracted_category,
        extracted_location_text=result.extracted_location_text,
        state=result.inferred_state,
        district=result.inferred_district,
        lat=lat,
        lng=lng,
        urgency_level=result.urgency_level,
        urgency_rationale=result.urgency_rationale,
        affected_population=result.affected_population_hint,
        summary_for_policymaker=result.summary_for_policymaker,
        language_confidence=result.language_confidence,
        stt_confidence=result.stt_confidence,
        translation_confidence=result.translation_confidence,
        category_confidence=result.category_confidence,
        location_confidence=result.inferred_location_confidence,
        acoustic_warning=result.acoustic_warning,
        status="UNDER_ANALYSIS",
        corrections_history=[]
    )
    db.add(req)
    db.commit()
    db.refresh(req)

    # Keep the map responsive to new demand clusters, including districts
    # that were not part of the seeded demo hotspots.
    hotspot_id = f"HS-{result.inferred_state[:2].upper()}-{result.inferred_district[:3].upper()}-{result.category_id[:3].upper()}"
    hotspot = db.query(HotspotModel).filter(HotspotModel.id == hotspot_id).first()
    live_count = db.query(CitizenRequestModel).filter(
        CitizenRequestModel.state == result.inferred_state,
        CitizenRequestModel.district == result.inferred_district,
        CitizenRequestModel.category_id == result.category_id,
    ).count()
    scoring = analytics_engine.compute_prioritization(
        demand_volume=live_count,
        persistence_score=0.35,
        district=result.inferred_district,
        state=result.inferred_state,
        sector_id=result.category_id,
    )
    if hotspot:
        hotspot.demand_volume = live_count
        hotspot.priority_score = scoring["priority_score"]
        hotspot.severity = scoring["severity"]
        hotspot.updated_at = datetime.datetime.utcnow()
    else:
        db.add(HotspotModel(
            id=hotspot_id,
            state=result.inferred_state,
            district=result.inferred_district,
            sector_id=result.category_id,
            sector_name=result.extracted_category,
            demand_volume=live_count,
            persistence_score=0.35,
            priority_score=scoring["priority_score"],
            severity=scoring["severity"],
            lat=lat,
            lng=lng,
            trend="NEW",
            supporting_indicators={"source": "live citizen submission", "synthetic_data": True},
        ))
    db.commit()

    # Audit log
    db.add(AuditLogModel(
        entity_type="citizen_request", entity_id=tracking_code,
        action="AI_CLASSIFICATION", actor_role="AI_ENGINE",
        new_value={"category": result.category_id, "district": result.inferred_district, "lang": result.detected_language}
    ))
    db.commit()

    return {
        "tracking_code": tracking_code,
        "flagged": flagged,
        "spam_score": spam_score,
        "extraction": result.dict(),
        "image_attached": bool(body.image_data),
        "status": "UNDER_ANALYSIS",
        "message": "Your request has been received and is being analyzed."
    }

@app.post("/api/ai/process", tags=["AI Pipeline"])
def run_ai_pipeline(body: SubmitRequestBody):
    """Run AI pipeline without saving — preview extraction for citizen confirmation screen."""
    result = ai_pipeline.process_full_pipeline(
        raw_text=(body.text or "").strip(),
        audio_data=body.audio_data,
        language_hint=body.language_override,
        location_hint=body.location_hint
    )
    return {"extraction": result.dict()}

@app.get("/api/requests/{tracking_code}", tags=["Citizen Requests"])
def get_request_status(tracking_code: str, db: Session = Depends(get_db)):
    req = db.query(CitizenRequestModel).filter(CitizenRequestModel.tracking_code == tracking_code).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return {
        "tracking_code": req.tracking_code,
        "status": req.status,
        "category": req.category_name,
        "district": req.district,
        "state": req.state,
        "urgency": req.urgency_level,
        "submitted_at": req.created_at.isoformat() if req.created_at else None,
        "linked_hotspot_id": req.linked_hotspot_id,
        "linked_project_id": req.linked_project_id
    }

class CorrectionBody(BaseModel):
    corrected_category: Optional[str] = None
    corrected_district: Optional[str] = None
    corrected_urgency: Optional[str] = None
    correction_reason: Optional[str] = None
    corrector_role: Optional[str] = "citizen"  # "citizen" or "policymaker"

@app.patch("/api/requests/{tracking_code}/correct", tags=["Citizen Requests"])
def correct_request(tracking_code: str, body: CorrectionBody, db: Session = Depends(get_db)):
    req = db.query(CitizenRequestModel).filter(CitizenRequestModel.tracking_code == tracking_code).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    old_values = {"category_id": req.category_id, "district": req.district, "urgency": req.urgency_level}
    corrections = req.corrections_history or []

    if body.corrected_category:
        req.category_id = body.corrected_category
        sector = next((s for s in SECTORS if s["id"] == body.corrected_category), None)
        req.category_name = sector["name"] if sector else body.corrected_category
    if body.corrected_district:
        req.district = body.corrected_district
    if body.corrected_urgency:
        req.urgency_level = body.corrected_urgency

    corrections.append({
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "by_role": body.corrector_role,
        "reason": body.correction_reason,
        "old": old_values,
        "new": {"category_id": req.category_id, "district": req.district, "urgency": req.urgency_level}
    })
    req.corrections_history = corrections

    db.add(AuditLogModel(
        entity_type="citizen_request", entity_id=tracking_code,
        action="CITIZEN_OVERRIDE" if body.corrector_role == "citizen" else "POLICYMAKER_OVERRIDE",
        actor_role=body.corrector_role.upper(),
        old_value=old_values,
        new_value={"category_id": req.category_id, "district": req.district, "urgency": req.urgency_level},
        reason=body.correction_reason
    ))
    db.commit()
    model_eval_tracker.record_correction_event(body.corrector_role or "citizen")
    return {"message": "Correction applied and logged", "tracking_code": tracking_code}

@app.get("/api/requests", tags=["Policymaker Dashboard"])
def list_requests(
    state: Optional[str] = None, district: Optional[str] = None,
    category: Optional[str] = None, language: Optional[str] = None,
    limit: int = 50, db: Session = Depends(get_db),
    user=Depends(require_policymaker)
):
    q = db.query(CitizenRequestModel)
    if state: q = q.filter(CitizenRequestModel.state == state)
    if district: q = q.filter(CitizenRequestModel.district == district)
    if category: q = q.filter(CitizenRequestModel.category_id == category)
    if language: q = q.filter(CitizenRequestModel.original_language == language)
    rows = q.order_by(CitizenRequestModel.created_at.desc()).limit(limit).all()
    return {"requests": [
        {"id": r.id, "tracking_code": r.tracking_code, "channel": r.channel,
         "original_language": r.original_language, "category_name": r.category_name,
         "district": r.district, "state": r.state, "urgency_level": r.urgency_level,
         "status": r.status, "created_at": r.created_at.isoformat() if r.created_at else None,
         "language_confidence": r.language_confidence, "category_confidence": r.category_confidence,
         "image_attached": bool(r.image_data), "image_filename": r.image_filename}
        for r in rows
    ]}

# =====================================================================
# HOTSPOTS
# =====================================================================

@app.get("/api/hotspots", tags=["Analytics"])
def get_hotspots(state: Optional[str] = None, sector: Optional[str] = None,
                 db: Session = Depends(get_db)):
    q = db.query(HotspotModel)
    if state: q = q.filter(HotspotModel.state == state)
    if sector: q = q.filter(HotspotModel.sector_id == sector)
    hotspots = q.order_by(HotspotModel.priority_score.desc()).all()
    result = []
    for h in hotspots:
        requests = db.query(CitizenRequestModel).filter(
            CitizenRequestModel.state == h.state,
            CitizenRequestModel.district == h.district,
            CitizenRequestModel.category_id == h.sector_id,
        ).all()
        completed_count = sum(1 for request in requests if request.status == "RESOLVED")
        pending_count = len(requests) - completed_count
        request_status = "MIXED" if pending_count and completed_count else "COMPLETED" if completed_count else "PENDING"
        result.append({
            "id": h.id, "state": h.state, "district": h.district,
            "sector_id": h.sector_id, "sector_name": h.sector_name,
            "demand_volume": len(requests) or h.demand_volume,
            "seeded_demand_volume": h.demand_volume,
            "pending_count": pending_count,
            "completed_count": completed_count,
            "request_status": request_status,
            "persistence_score": h.persistence_score,
            "priority_score": h.priority_score, "severity": h.severity,
            "lat": h.lat, "lng": h.lng, "trend": h.trend,
            "supporting_indicators": h.supporting_indicators}
        )
    return {"hotspots": result}

# =====================================================================
# RECOMMENDATIONS
# =====================================================================

@app.get("/api/recommendations", tags=["Analytics"])
def get_recommendations(
    state: Optional[str] = None,
    w1: float = settings.DEFAULT_W1_DEMAND,
    w2: float = settings.DEFAULT_W2_PERSISTENCE,
    w3: float = settings.DEFAULT_W3_INFRA_GAP,
    w4: float = settings.DEFAULT_W4_DEMOGRAPHIC,
    db: Session = Depends(get_db)
):
    weights_are_default = all(abs(value - default) < 0.0001 for value, default in [
        (w1, settings.DEFAULT_W1_DEMAND),
        (w2, settings.DEFAULT_W2_PERSISTENCE),
        (w3, settings.DEFAULT_W3_INFRA_GAP),
        (w4, settings.DEFAULT_W4_DEMOGRAPHIC),
    ])
    if weights_are_default:
        q = db.query(RecommendationModel)
        if state:
            q = q.filter(RecommendationModel.state == state)
        recs = q.order_by(RecommendationModel.priority_score.desc()).all()
        recommendations = [{
            "id": r.id, "title": r.title,
            "sector_id": r.sector_id, "sector_name": r.sector_name,
            "district": r.target_district, "state": r.state,
            "priority_score": r.priority_score, "severity": r.severity,
            "factor_breakdown": r.factor_breakdown,
            "formula_output": r.formula_output,
            "evidence_trail": r.evidence_trail,
            "suggested_budget_cr_inr": r.suggested_budget_cr_inr,
            "status": r.status,
            "adoption_metadata": r.adoption_metadata,
            "disclaimer": "Decision Support Tool — Final decisions rest with authorized human policymakers."
        } for r in recs]
    else:
        hotspot_query = db.query(HotspotModel)
        if state:
            hotspot_query = hotspot_query.filter(HotspotModel.state == state)
        hotspots = [{
            "state": h.state, "district": h.district, "sector_id": h.sector_id,
            "sector_name": h.sector_name, "demand_volume": h.demand_volume,
            "persistence_score": h.persistence_score
        } for h in hotspot_query.all()]
        generated = analytics_engine.generate_recommendations(hotspots, w1, w2, w3, w4)
        stored = {r.id: r for r in db.query(RecommendationModel).all()}
        recommendations = []
        for item in generated:
            saved = stored.get(item["id"])
            recommendations.append({
                "id": item["id"], "title": item["title"],
                "sector_id": item["sector_id"], "sector_name": item["sector_name"],
                "district": item["district"], "state": item["state"],
                "priority_score": item["priority_score"], "severity": item["severity"],
                "factor_breakdown": item["factor_breakdown"],
                "formula_output": item["formula_output"],
                "evidence_trail": item["evidence_trail"],
                "suggested_budget_cr_inr": item["suggested_budget_range_cr_inr"],
                "status": saved.status if saved else "PROPOSED",
                "adoption_metadata": saved.adoption_metadata if saved else None,
                "disclaimer": item["decision_support_disclaimer"]
            })
        recommendations.sort(key=lambda item: item["priority_score"], reverse=True)

    return {"recommendations": recommendations, "weights_applied": {"w1_demand": w1, "w2_persistence": w2, "w3_infra_gap": w3, "w4_demographic": w4}}

class AdoptBody(BaseModel):
    policymaker_name: str
    allocated_budget_cr_inr: float
    notes: Optional[str] = ""

@app.patch("/api/recommendations/{rec_id}/adopt", tags=["Analytics"])
def adopt_recommendation(rec_id: str, body: AdoptBody, db: Session = Depends(get_db), user=Depends(require_policymaker)):
    rec = db.query(RecommendationModel).filter(RecommendationModel.id == rec_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    rec.status = "ADOPTED"
    rec.adoption_metadata = {
        "adopted_by": body.policymaker_name,
        "allocated_budget_cr_inr": body.allocated_budget_cr_inr,
        "notes": body.notes,
        "adopted_at": datetime.datetime.utcnow().isoformat()
    }
    db.add(AuditLogModel(
        entity_type="recommendation", entity_id=rec_id,
        action="ADOPTED_RECOMMENDATION", actor_role="POLICYMAKER",
        actor_id=user.get("sub", "policymaker"),
        new_value=rec.adoption_metadata
    ))
    db.commit()
    impact_tracker.adopt_recommendation(
        recommendation={"id": rec_id, "title": rec.title, "district": rec.target_district,
                        "state": rec.state, "sector_id": rec.sector_id, "sector_name": rec.sector_name,
                        "factor_breakdown": rec.factor_breakdown},
        policymaker_name=body.policymaker_name,
        allocated_budget=body.allocated_budget_cr_inr,
        notes=body.notes
    )
    return {"message": "Recommendation adopted and impact tracking initialized.", "id": rec_id}

# =====================================================================
# IMPACT MEASUREMENT
# =====================================================================

@app.get("/api/impact", tags=["Impact Measurement"])
def get_impact_studies():
    return {"impact_studies": impact_tracker.get_all_impact_studies()}

# =====================================================================
# INFRASTRUCTURE & DEMOGRAPHICS
# =====================================================================

@app.get("/api/infrastructure", tags=["Reference Data"])
def get_infrastructure(state: Optional[str] = None, district: Optional[str] = None,
                       db: Session = Depends(get_db)):
    q = db.query(InfrastructureModel)
    if state: q = q.filter(InfrastructureModel.state == state)
    if district: q = q.filter(InfrastructureModel.district == district)
    rows = q.all()
    return {"infrastructure": [
        {"state": r.state, "district": r.district, "sector": r.sector,
         "score": r.score, "coverage_desc": r.coverage_desc, "year": r.year}
        for r in rows
    ]}

@app.get("/api/demographics", tags=["Reference Data"])
def get_demographics(state: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(DemographicsModel)
    if state: q = q.filter(DemographicsModel.state == state)
    rows = q.all()
    return {"demographics": [
        {"state": r.state, "district": r.district, "population": r.population,
         "density_per_sqkm": r.density_per_sqkm, "rural_pct": r.rural_pct,
         "literacy_rate": r.literacy_rate}
        for r in rows
    ]}

# =====================================================================
# EVALUATION METRICS & AUDIT
# =====================================================================

@app.get("/api/evaluation-metrics", tags=["Governance & Audit"])
def get_evaluation_metrics(user=Depends(require_policymaker)):
    return model_eval_tracker.get_metrics()

@app.get("/api/audit-log", tags=["Governance & Audit"])
def get_audit_log(limit: int = 100, db: Session = Depends(get_db), user=Depends(require_policymaker)):
    rows = db.query(AuditLogModel).order_by(AuditLogModel.timestamp.desc()).limit(limit).all()
    return {"audit_log": [
        {"id": r.id, "timestamp": r.timestamp.isoformat() if r.timestamp else None,
         "entity_type": r.entity_type, "entity_id": r.entity_id,
         "action": r.action, "actor_role": r.actor_role,
         "old_value": r.old_value, "new_value": r.new_value, "reason": r.reason}
        for r in rows
    ]}

@app.get("/api/channels", tags=["Reference Data"])
def get_channel_info():
    return {"channels": [
        {"name": c.channel_name, "is_live": c.is_live}
        for c in CHANNEL_REGISTRY.values()
    ]}

@app.post("/api/channels/webhook/{channel_name}", tags=["Multi-Channel"])
def receive_channel_webhook(channel_name: str, payload: Dict[str, Any] = Body(...)):
    adapter = CHANNEL_REGISTRY.get(channel_name)
    if not adapter:
        raise HTTPException(status_code=404, detail=f"Unknown channel: {channel_name}")
    normalized = adapter.normalize_payload(payload)
    return {
        "channel": channel_name,
        "is_live": adapter.is_live,
        "normalized_input": normalized.dict(),
        "note": "Stub channels are for demo/testing only. Wire to POST /api/requests for live processing."
    }

@app.get("/api/health", tags=["System"])
def health():
    return {"status": "ok", "platform": settings.PROJECT_NAME, "version": settings.VERSION, "data_disclaimer": "All datasets are synthetic demo data."}


@app.get("/api/location/reverse", tags=["Reference Data"])
def reverse_location(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
):
    import json
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen

    params = urlencode({
        "lat": latitude,
        "lon": longitude,
        "format": "json",
        "zoom": 18,
        "addressdetails": 1,
    })
    request = Request(
        f"https://nominatim.openstreetmap.org/reverse?{params}",
        headers={"User-Agent": "CitizenDevelopmentIntelligencePlatform/1.0"},
    )

    try:
        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise HTTPException(status_code=502, detail="Location lookup is temporarily unavailable") from error

    address = data.get("address", {})
    area = (
        address.get("village")
        or address.get("town")
        or address.get("city")
        or address.get("municipality")
        or address.get("county")
        or ""
    )
    return {
        "area": area,
        "display_name": data.get("display_name", ""),
        "state": address.get("state", ""),
        "district": address.get("state_district", ""),
    }
