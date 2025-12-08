# book-backend/app/db/postgres.py
import os
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import List

DATABASE_URL = os.getenv("DATABASE_URL")

# Basic setup for SQLAlchemy
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class LogEntry(Base):
    __tablename__ = "chatbot_logs"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    query_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    retrieved_chunks = Column(Text) # Store as JSON string
    user_session_id = Column(String, index=True)

# Create tables
def create_db_tables():
    Base.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def log_interaction(
    query_id: str,
    query_text: str,
    response_text: str,
    retrieved_chunks: List[str],
    user_session_id: str
):
    """
    Logs a chatbot interaction to the Neon Postgres database.
    """
    db = SessionLocal()
    try:
        log = LogEntry(
            id=query_id,
            query_text=query_text,
            response_text=response_text,
            retrieved_chunks=str(retrieved_chunks), # Convert list to string for storage
            user_session_id=user_session_id
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        print(f"Logged chatbot interaction: {query_id}")
    except Exception as e:
        print(f"Error logging interaction to Postgres: {e}")
        db.rollback()
    finally:
        db.close()
