from typing import Dict, Any, Optional
from pydantic import BaseModel
from rag_system.agents.base_agent import BaseAgent, AgentRequest, AgentResponse
from rag_system.core.llm_provider import LLMProvider
from rag_system.retrieval.schemas import SearchRequest

class WriterRequest(AgentRequest):
    """Request model for Writer Agent"""
    prompt: str
    context: Optional[Dict[str, Any]] = None
    parameters: Dict[str, Any] = {}

class WriterAgent(BaseAgent):
    """Agent responsible for generating new content based on prompts and context"""
    
    def __init__(self, llm_provider: LLMProvider):
        super().__init__(agent_type="writer")
        self.llm_provider = llm_provider
        
    async def execute(self, request: WriterRequest) -> AgentResponse:
        """
        Execute the writing operation.
        
        Args:
            request: The writing request containing prompt and optional context
            
        Returns:
            AgentResponse containing the generated text
        """
        try:
            # Prepare the prompt with context if provided
            if request.context:
                prompt = f"Context: {json.dumps(request.context, indent=2)}\n\n{request.prompt}"
            else:
                prompt = request.prompt
                
            # Create LLM request
            llm_request = {
                "prompt": prompt,
                "model": "llama2",
                "parameters": request.parameters
            }
            
            # Generate text using LLM
            response = await self.llm_provider.generate(llm_request)
            
            return AgentResponse(
                result={
                    "text": response.text,
                    "prompt": request.prompt
                },
                metadata={
                    "agent_type": self.agent_type,
                    "model": response.metadata.get("model"),
                    "tokens_used": response.metadata.get("tokens_used")
                }
            )
            
        except Exception as e:
            raise Exception(f"Writing failed: {str(e)}")
