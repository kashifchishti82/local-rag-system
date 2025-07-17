from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List

from rag_system.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata_ = Column("metadata", Text, nullable=True)
    chunks = relationship("DocumentChunk", back_populates="document")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Text, nullable=False)  # Store as text for now
    metadata_ = Column("metadata", Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="chunks")

class IngestionJob(Base):
    __tablename__ = "ingestion_jobs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(50), nullable=False, default="pending")
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    document = relationship("Document")
