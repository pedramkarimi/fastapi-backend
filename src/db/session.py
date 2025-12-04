# src/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

# Engine
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    future=True,
    echo=False    # show sql queries in logs
)

# SessionLocal
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
