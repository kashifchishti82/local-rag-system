from fastapi import APIRouter, Depends, HTTPException
from rag_system.agents.base_agent import AgentRequest, AgentResponse
from rag_system.agents.retriever import RetrieverAgent, RetrieverRequest
from rag_system.agents.writer import WriterAgent, WriterRequest
from rag_system.agents.editor import EditorAgent, EditorRequest
from rag_system.agents.augmentor import AugmentorAgent, AugmentorRequest
from rag_system.embeddings.provider_factory import EmbeddingProviderFactory
from rag_system.vector_store.faiss_store import FaissVectorStore
from rag_system.retrieval.services import SearchService
from rag_system.core.llm_provider import LLMProvider

router = APIRouter(prefix="/agents", tags=["agents"])

# Initialize dependencies
from config import settings

provider_config = {
    "provider_type": settings.llm_provider_type,
    "config": {
        "base_url": settings.ollama_base_url,
        "model": settings.ollama_model
    }
}

llm_provider = LLMProvider()
vector_store = FaissVectorStore()
search_service = SearchService(vector_store, "ollama", provider_config)

# Initialize agents
retriever_agent = RetrieverAgent(vector_store, "ollama", provider_config)
writer_agent = WriterAgent(llm_provider)
editor_agent = EditorAgent(llm_provider)
augmentor_agent = AugmentorAgent(llm_provider, retriever_agent, writer_agent)

@router.post("/qna", response_model=AgentResponse)
async def qna_endpoint(request: RetrieverRequest) -> AgentResponse:
    """
    Answer questions using the retriever and writer agents.
    
    Args:
        request: The question and retrieval parameters
        
    Returns:
        AgentResponse containing the answer
    """
    try:
        # Retrieve context
        retrieval_response = await retriever_agent.execute(request)
        
        # Generate answer using writer agent
        writer_request = {
            "prompt": f"Answer the following question based on the provided context:\n\nQuestion: {request.query}\n\nContext: {json.dumps(retrieval_response.result.get('results'), indent=2)}",
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 500
            }
        }
        
        answer = await writer_agent.execute(writer_request)
        
        return AgentResponse(
            result={
                "answer": answer.result.get('text'),
                "context": retrieval_response.result.get('results')
            },
            metadata={
                "agent_type": "qna",
                "execution_time": "0.123"  # Placeholder for actual timing
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/co-author", response_model=AgentResponse)
async def co_author_endpoint(request: WriterRequest) -> AgentResponse:
    """
    Co-author new documentation using the writer agent.
    
    Args:
        request: The writing prompt and parameters
        
    Returns:
        AgentResponse containing the generated content
    """
    try:
        return await writer_agent.execute(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/edit", response_model=AgentResponse)
async def edit_endpoint(request: EditorRequest) -> AgentResponse:
    """
    Edit existing content using the editor agent.
    
    Args:
        request: The text to edit and editing instructions
        
    Returns:
        AgentResponse containing the edited content
    """
    try:
        return await editor_agent.execute(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/suggest-updates", response_model=AgentResponse)
async def suggest_updates_endpoint(request: AugmentorRequest) -> AgentResponse:
    """
    Suggest updates for existing documentation using the augmentor agent.
    
    Args:
        request: The topic and existing content to analyze
        
    Returns:
        AgentResponse containing the analysis and suggested updates
    """
    try:
        return await augmentor_agent.execute(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
