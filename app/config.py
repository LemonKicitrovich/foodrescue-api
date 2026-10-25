import os
from sqlalchemy.engine import make_url
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "foodrescue-secret-raihan")
    
    # Ambil DATABASE_URL
    raw_url = os.getenv("DATABASE_URL", "").strip().strip("'\"")
    
    # Normalisasi format
    if raw_url.startswith("postgres://"):
        raw_url = raw_url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif raw_url.startswith("postgresql://") and not raw_url.startswith("postgresql+psycopg2://"):
        raw_url = raw_url.replace("postgresql://", "postgresql+psycopg2://", 1)

    # Validasi apakah URL valid untuk SQLAlchemy
    is_valid = False
    if raw_url:
        try:
            make_url(raw_url)
            is_valid = True
        except Exception:
            is_valid = False
            
    if is_valid:
        SQLALCHEMY_DATABASE_URI = raw_url
    else:
        # Fallback in-memory yang 100% valid dan aman
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
