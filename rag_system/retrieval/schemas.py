from pydantic import BaseModel
from typing import Dict, List, Optional

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    score_threshold: float = 0.5
    metadata_filters: Optional[Dict[str, str]] = None

class SearchResult(BaseModel):
    text: str
    score: float
    metadata: Dict[str, str]
    document_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Sample retrieved text chunk",
                "score": 0.85,
                "metadata": {
                    "file_origin": "document1.pdf",
                    "title": "Sample Document",
                    "tags": "python, documentation"
                },
                "document_id": "doc123"
            }
        }

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total_results: int
    query_embedding: List[float]
