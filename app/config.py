import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "foodrescue-secret-raihan")
    
    # Ambil DATABASE_URL dari Environment Variables
    database_url = os.getenv("DATABASE_URL")
    
    if database_url and database_url.strip():
        database_url = database_url.strip()
        # Normalisasi prefix postgresql
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif database_url.startswith("postgresql://") and not database_url.startswith("postgresql+psycopg2://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Gunakan in-memory SQLite (sqlite://) saat startup check agar tidak membuat file/folder di AWS Lambda
        SQLALCHEMY_DATABASE_URI = "sqlite://"
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
