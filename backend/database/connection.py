from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, Session
from backend.database.models import Base
from backend.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    if "sqlite" in settings.DATABASE_URL:
        existing_columns = {column["name"] for column in inspect(engine).get_columns("citizen_requests")}
        with engine.begin() as connection:
            for name, definition in {
                "image_data": "TEXT",
                "image_mime_type": "VARCHAR(64)",
                "image_filename": "VARCHAR(256)",
            }.items():
                if name not in existing_columns:
                    connection.execute(text(f"ALTER TABLE citizen_requests ADD COLUMN {name} {definition}"))

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
