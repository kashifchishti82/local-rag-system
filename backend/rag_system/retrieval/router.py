from fastapi import APIRouter, Depends, HTTPException
from rag_system.retrieval.schemas import SearchRequest, SearchResponse
from rag_system.retrieval.services import SearchService
from rag_system.vector_store.faiss_store import FaissVectorStore
from rag_system.embeddings.provider_factory import EmbeddingProviderFactory

router = APIRouter(prefix="/retrieve", tags=["retrieval"])

# Initialize dependencies
vector_store = FaissVectorStore()
provider_config = {
    "provider_type": "ollama",
    "config": {
        "base_url": "http://localhost:11434",
        "model": "mistral"
    }
}
provider = EmbeddingProviderFactory.create_provider(**provider_config)
search_service = SearchService(vector_store, "ollama", provider_config)

@router.post("/search", response_model=SearchResponse)
async def search_endpoint(request: SearchRequest) -> SearchResponse:
    """
    Perform semantic search on the vector store.
    
    Args:
        request: Search parameters including query, top_k, score_threshold, and metadata filters
    
    Returns:
        SearchResponse containing the retrieved results
    """
    try:
        return search_service.search(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
