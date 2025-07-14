from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings

engine = create_engine(
    settings.DB_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Import all models to ensure they are registered with Base
from rag_system.db.models import User
from rag_system.ingestion.models import Document, DocumentChunk, IngestionJob
from rag_system.retrieval.models import SearchQuery, SearchResult, Feedback

# Create tables
Base.metadata.create_all(bind=engine)

# Export the session factory
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Export Base for Alembic
__all__ = ['Base']
