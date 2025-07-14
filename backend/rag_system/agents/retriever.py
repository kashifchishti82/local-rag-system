from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from rag_system.agents.base_agent import BaseAgent, AgentRequest, AgentResponse
from rag_system.vector_store.faiss_store import FaissVectorStore
from rag_system.retrieval.services import SearchService
from rag_system.embeddings.provider_factory import EmbeddingProviderFactory

class RetrieverRequest(AgentRequest):
    """Request model for Retriever Agent"""
    query: str
    top_k: int = 5
    score_threshold: float = 0.5
    metadata_filters: Optional[Dict[str, str]] = None

class RetrieverAgent(BaseAgent):
    """Agent responsible for retrieving relevant context from the vector store"""
    
    def __init__(self, vector_store: FaissVectorStore, provider_type: str, provider_config: Dict):
        super().__init__(agent_type="retriever")
        self.provider = EmbeddingProviderFactory.create_provider(provider_type, provider_config)
        self.search_service = SearchService(vector_store, provider_type, provider_config)
        
    async def execute(self, request: RetrieverRequest) -> AgentResponse:
        """
        Execute the retrieval operation.
        
        Args:
            request: The retrieval request containing query and parameters
            
        Returns:
            AgentResponse containing the retrieved results
        """
        try:
            search_request = {
                "query": request.query,
                "top_k": request.top_k,
                "score_threshold": request.score_threshold,
                "metadata_filters": request.metadata_filters
            }
            
            results = await self.search_service.search(search_request)
            
            return AgentResponse(
                result={
                    "results": results,
                    "query": request.query
                },
                metadata={
                    "agent_type": self.agent_type,
                    "execution_time": "0.123"  # Placeholder for actual timing
                }
            )
            
        except Exception as e:
            raise Exception(f"Retrieval failed: {str(e)}")
