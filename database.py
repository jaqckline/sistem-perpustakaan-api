# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Memuat variabel dari file .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Engine adalah gerbang utama ke database
engine = create_engine(DATABASE_URL)

# SessionLocal adalah kelas yang akan menghasilkan sesi database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base digunakan sebagai kelas dasar untuk semua model
Base = declarative_base()

def get_db():
    """
    Dependency FastAPI yang akan menyediakan sesi database untuk setiap request,
    lalu menutupnya setelah selesai.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()