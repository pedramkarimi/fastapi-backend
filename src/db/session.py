# src/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

# Engine
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    future=True,
    echo=True,  # فعلاً بذار روشن باشه تا کوئری‌ها رو در لاگ ببینی (بعداً می‌تونی خاموش کنی)
)

# SessionLocal
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# dependency برای FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
