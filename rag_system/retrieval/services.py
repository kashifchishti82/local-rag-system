from typing import List, Optional, Dict
from rag_system.retrieval.schemas import SearchRequest, SearchResponse, SearchResult
from rag_system.vector_store.faiss_store import FaissVectorStore
from rag_system.embeddings.provider_factory import EmbeddingProviderFactory
import numpy as np

class SearchService:
    def __init__(self, vector_store: FaissVectorStore, provider_type: str, provider_config: Dict):
        self.vector_store = vector_store
        self.provider = EmbeddingProviderFactory.create_provider(provider_type, provider_config)

    def search(self, request: SearchRequest) -> SearchResponse:
        # Generate embedding for the query
        try:
            query_embedding = self.provider.get_embedding(request.query)
        except Exception as e:
            raise ValueError(f"Failed to generate embedding: {str(e)}")
        
        # Perform semantic search
        results = self.vector_store.search(
            query_embedding,
            top_k=request.top_k,
            score_threshold=request.score_threshold,
            metadata_filters=request.metadata_filters
        )
        
        # Convert results to SearchResult objects
        search_results = [
            SearchResult(
                text=result['text'],
                score=result['score'],
                metadata=result['metadata'],
                document_id=result['document_id']
            )
            for result in results
        ]
        
        return SearchResponse(
            results=search_results,
            total_results=len(search_results),
            query_embedding=query_embedding.tolist()
        )
