from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

SQLALCHEMY_DATABASE_URL = \
    (f"postgresql://{settings.DATABASE_DB_USER}:{settings.DATABASE_DB_PASS}@"
     f"{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/"
     f"{settings.DATABASE_DB_NAME}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
