import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "foodrescue-secret-raihan")
    
    # Ambil DATABASE_URL dari file .env atau Vercel Environment Variables
    database_url = os.getenv("DATABASE_URL", "sqlite:///foodrescue.db")
    
    # Fix untuk PostgreSQL: SQLAlchemy butuh prefix postgresql+psycopg2://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif database_url.startswith("postgresql://") and not database_url.startswith("postgresql+psycopg2://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
