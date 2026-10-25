import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "foodrescue-secret-raihan")
    
    # Ambil DATABASE_URL dari Environment Variables
    database_url = os.getenv("DATABASE_URL")
    
    # Normalisasi format URL untuk PostgreSQL Supabase
    if database_url and database_url.strip():
        database_url = database_url.strip()
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif database_url.startswith("postgresql://") and not database_url.startswith("postgresql+psycopg2://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)
    else:
        # Fallback ke sqlite di folder temporary (/tmp) yang aman untuk Vercel Serverless
        tmp_db = os.path.join(tempfile.gettempdir(), "foodrescue.db").replace("\\", "/")
        database_url = f"sqlite:///{tmp_db}"
        
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
