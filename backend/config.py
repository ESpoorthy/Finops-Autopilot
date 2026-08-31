import os
from pydantic_settings import BaseSettings
from typing import Optional

from pydantic import ConfigDict

class Settings(BaseSettings):
    # Google Cloud
    GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT", "finops-autopilot-demo")
    GOOGLE_CLOUD_LOCATION: str = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    # Gemini / ADK Model
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    GOOGLE_GENAI_USE_VERTEXAI: str = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")
    
    # GitHub
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN", None)
    GITHUB_OWNER: str = os.getenv("GITHUB_OWNER", "ESpoorthy")
    GITHUB_REPO: str = os.getenv("GITHUB_REPO", "Finops-Autopilot")
    GITHUB_BASE_BRANCH: str = os.getenv("GITHUB_BASE_BRANCH", "main")
    
    # Firestore
    FIRESTORE_DATABASE: str = os.getenv("FIRESTORE_DATABASE", "(default)")
    
    # Application & Safety
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")
    
    # Safety Limits
    MAX_MONTHLY_CHANGE: float = float(os.getenv("MAX_MONTHLY_CHANGE", "1000.0"))
    MIN_CONFIDENCE: float = float(os.getenv("MIN_CONFIDENCE", "0.80"))
    REQUIRE_STAGING_VALIDATION: bool = True
    REQUIRE_HUMAN_MERGE: bool = True
    
    model_config = ConfigDict(extra="ignore")

settings = Settings()
