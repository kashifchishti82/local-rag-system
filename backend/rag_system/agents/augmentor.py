from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from rag_system.agents.base_agent import BaseAgent, AgentRequest, AgentResponse
from rag_system.core.llm_provider import LLMProvider
from rag_system.agents.retriever import RetrieverAgent
from rag_system.agents.writer import WriterAgent

class AugmentorRequest(AgentRequest):
    """Request model for Augmentor Agent"""
    topic: str
    existing_content: Optional[str] = None
    analysis_parameters: Dict[str, Any] = {}
    generation_parameters: Dict[str, Any] = {}

class AugmentorAgent(BaseAgent):
    """Agent responsible for analyzing content and suggesting updates"""
    
    def __init__(self, 
                 llm_provider: LLMProvider,
                 retriever_agent: RetrieverAgent,
                 writer_agent: WriterAgent):
        super().__init__(agent_type="augmentor")
        self.llm_provider = llm_provider
        self.retriever_agent = retriever_agent
        self.writer_agent = writer_agent
        
    async def execute(self, request: AugmentorRequest) -> AgentResponse:
        """
        Execute the augmentation operation.
        
        Args:
            request: The augmentation request containing topic and existing content
            
        Returns:
            AgentResponse containing the analysis and suggested updates
        """
        try:
            # Step 1: Retrieve relevant context
            retrieval_request = {
                "query": request.topic,
                "top_k": 10,
                "score_threshold": 0.4
            }
            retrieval_response = await self.retriever_agent.execute(retrieval_request)
            
            # Step 2: Analyze content for gaps
            analysis_prompt = f"""Analyze the following content and identify potential gaps or areas for improvement:
            
            Topic: {request.topic}
            
            Existing Content: {request.existing_content}
            
            Retrieved Context: {json.dumps(retrieval_response.result.get('results'), indent=2)}
            
            Provide a detailed analysis of gaps and suggestions for improvement."""
            
            analysis_request = {
                "prompt": analysis_prompt,
                "model": "llama2",
                "parameters": request.analysis_parameters
            }
            
            analysis_response = await self.llm_provider.generate(analysis_request)
            
            # Step 3: Generate suggested updates
            update_prompt = f"""Based on the analysis, generate suggested updates for the content:
            
            Analysis: {analysis_response.text}
            
            Existing Content: {request.existing_content}
            
            Generate a detailed plan of updates needed."""
            
            update_request = {
                "prompt": update_prompt,
                "model": "llama2",
                "parameters": request.generation_parameters
            }
            
            update_response = await self.writer_agent.execute(update_request)
            
            return AgentResponse(
                result={
                    "analysis": analysis_response.text,
                    "suggested_updates": update_response.result.get('text'),
                    "retrieved_context": retrieval_response.result.get('results')
                },
                metadata={
                    "agent_type": self.agent_type,
                    "analysis_tokens": analysis_response.metadata.get("tokens_used"),
                    "update_tokens": update_response.metadata.get("tokens_used")
                }
            )
            
        except Exception as e:
            raise Exception(f"Augmentation failed: {str(e)}")
