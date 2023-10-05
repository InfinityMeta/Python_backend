from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, CheckConstraint


DATABASE_URL = "sqlite:///./app/models_database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class ModelDb(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    score = Column(Float, CheckConstraint("score BETWEEN 0.0 AND 1.0"), nullable=True)


def get_db():
    """
    Create session for requests.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
