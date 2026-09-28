from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class CitizenRequestModel(Base):
    __tablename__ = "citizen_requests"

    id = Column(Integer, primary_key=True, index=True)
    tracking_code = Column(String(32), unique=True, index=True)
    channel = Column(String(32), default="web_form") # web_form, voice_audio, messaging_chat, whatsapp_stub, sms_stub
    original_language = Column(String(16), default="en")
    original_text = Column(Text, nullable=False)
    original_script = Column(String(32), default="Latin")
    translated_text = Column(Text, nullable=False)
    
    # Classification & Location
    category_id = Column(String(64), index=True)
    category_name = Column(String(128))
    extracted_location_text = Column(String(256))
    state = Column(String(64), index=True)
    district = Column(String(64), index=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    
    # Urgency & Population
    urgency_level = Column(String(32), default="Medium")
    urgency_rationale = Column(Text, nullable=True)
    affected_population = Column(String(128), nullable=True)
    summary_for_policymaker = Column(Text, nullable=True)

    # Confidence Scores
    language_confidence = Column(Float, default=0.90)
    stt_confidence = Column(Float, default=0.90)
    translation_confidence = Column(Float, default=0.90)
    category_confidence = Column(Float, default=0.90)
    location_confidence = Column(Float, default=0.80)
    acoustic_warning = Column(String(256), nullable=True)

    # Status & Audit
    status = Column(String(32), default="UNDER_ANALYSIS") # RECEIVED, UNDER_ANALYSIS, LINKED_TO_HOTSPOT, LINKED_TO_PROJECT, RESOLVED
    linked_hotspot_id = Column(String(64), nullable=True)
    linked_project_id = Column(String(64), nullable=True)
    corrections_history = Column(JSON, default=list) # List of human overrides
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class GeographyModel(Base):
    __tablename__ = "geography"

    id = Column(Integer, primary_key=True)
    state = Column(String(64), index=True)
    state_code = Column(String(8))
    district = Column(String(64), index=True)
    district_code = Column(String(16))
    region = Column(String(64))
    lat = Column(Float)
    lng = Column(Float)
    is_aspirational_district = Column(Boolean, default=False)


class DemographicsModel(Base):
    __tablename__ = "demographics"

    id = Column(Integer, primary_key=True)
    state = Column(String(64), index=True)
    district = Column(String(64), index=True)
    population = Column(Integer)
    density_per_sqkm = Column(Integer)
    rural_pct = Column(Float)
    literacy_rate = Column(Float)
    year = Column(Integer, default=2024)


class InfrastructureModel(Base):
    __tablename__ = "infrastructure"

    id = Column(Integer, primary_key=True)
    state = Column(String(64), index=True)
    district = Column(String(64), index=True)
    sector = Column(String(64), index=True)
    score = Column(Float)
    coverage_desc = Column(Text)
    year = Column(Integer, default=2024)


class InvestmentPlanModel(Base):
    __tablename__ = "investment_plans"

    id = Column(Integer, primary_key=True)
    plan_id = Column(String(32), unique=True)
    state = Column(String(64), index=True)
    district = Column(String(64), index=True)
    sector = Column(String(64), index=True)
    project_name = Column(String(256))
    budget_cr_inr = Column(Float)
    timeline = Column(String(32))
    status = Column(String(64))
    scheme = Column(String(128))


class HotspotModel(Base):
    __tablename__ = "hotspots"

    id = Column(String(64), primary_key=True)
    state = Column(String(64), index=True)
    district = Column(String(64), index=True)
    sector_id = Column(String(64), index=True)
    sector_name = Column(String(128))
    demand_volume = Column(Integer)
    persistence_score = Column(Float)
    priority_score = Column(Float)
    severity = Column(String(32))
    lat = Column(Float)
    lng = Column(Float)
    trend = Column(String(32), default="ACCELERATING")
    supporting_indicators = Column(JSON, default=dict)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class RecommendationModel(Base):
    __tablename__ = "recommendations"

    id = Column(String(64), primary_key=True)
    title = Column(String(256))
    sector_id = Column(String(64))
    sector_name = Column(String(128))
    target_district = Column(String(64))
    state = Column(String(64))
    priority_score = Column(Float)
    severity = Column(String(32))
    factor_breakdown = Column(JSON, default=dict)
    formula_output = Column(Text)
    evidence_trail = Column(JSON, default=list)
    suggested_budget_cr_inr = Column(Float)
    status = Column(String(32), default="PROPOSED") # PROPOSED, ADOPTED, FUNDED
    adoption_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class AuditLogModel(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    entity_type = Column(String(64)) # "citizen_request", "recommendation", "scoring_formula"
    entity_id = Column(String(64))
    action = Column(String(64)) # "AI_CLASSIFICATION", "CITIZEN_OVERRIDE", "POLICYMAKER_OVERRIDE", "ADOPTED_RECOMMENDATION"
    actor_role = Column(String(32)) # "CITIZEN", "POLICYMAKER", "AI_ENGINE", "SYSTEM"
    actor_id = Column(String(64), default="system")
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    reason = Column(Text, nullable=True)
    model_version = Column(String(32), default="v1.0.0-dpg")


class DatasetRegistryModel(Base):
    __tablename__ = "dataset_registry"

    id = Column(String(64), primary_key=True)
    name = Column(String(128))
    source = Column(String(128))
    date = Column(String(32))
    license = Column(String(64))
    geographic_level = Column(String(64))
    limitations = Column(Text)
    is_synthetic = Column(Boolean, default=True)
