from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List

from rag_system.db.database import Base

class SearchQuery(Base):
    __tablename__ = "search_queries"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    results = relationship("SearchResult", back_populates="query")
    user = relationship("User", backref="search_queries")

class SearchResult(Base):
    __tablename__ = "search_results"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("search_queries.id"), nullable=False)
    document_chunk_id = Column(Integer, ForeignKey("document_chunks.id"), nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    query = relationship("SearchQuery", back_populates="results")
    document_chunk = relationship("DocumentChunk")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("search_queries.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 scale
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    query = relationship("SearchQuery")
