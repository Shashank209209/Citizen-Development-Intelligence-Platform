import jwt as pyjwt
import datetime
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.config import settings

security = HTTPBearer()

DEMO_USERS = {
    "citizen@demo.in": {"role": "citizen", "password": "citizen123", "name": "Demo Citizen"},
    "policy@demo.in": {"role": "policymaker", "password": "policy456", "name": "Policymaker Dashboard User"},
    "analyst@demo.in": {"role": "analyst", "password": "analyst789", "name": "Data Analyst User"}
}

def create_token(email: str, role: str) -> str:
    payload = {
        "sub": email,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return pyjwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = pyjwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except pyjwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except pyjwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    return decode_token(credentials.credentials)

def require_policymaker(user: dict = Security(get_current_user)) -> dict:
    if user.get("role") not in ("policymaker", "analyst"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Policymaker/Analyst access required")
    return user
