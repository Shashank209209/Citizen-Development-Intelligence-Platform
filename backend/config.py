import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Citizen Development Intelligence Platform (India Prototype)"
    VERSION: str = "1.0.0-dpg"
    DESCRIPTION: str = "Digital Public Good prototype for Multilingual Citizen Demand Extraction and Evidence-Backed Prioritization"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./citizen_dev_intel.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "brics-dpg-prototype-secret-2026-govtech")
    ALGORITHM: str = "HS256"
    
    # Prioritization Engine Default Weights (Explicit Prototype Assumptions)
    DEFAULT_W1_DEMAND: float = 0.35
    DEFAULT_W2_PERSISTENCE: float = 0.25
    DEFAULT_W3_INFRA_GAP: float = 0.25
    DEFAULT_W4_DEMOGRAPHIC: float = 0.15

settings = Settings()
