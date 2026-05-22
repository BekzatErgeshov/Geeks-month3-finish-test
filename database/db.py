from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.models import Base

DATABASE_URL = "sqlite:///student_course_manager.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db() -> None:
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return SessionLocal()
