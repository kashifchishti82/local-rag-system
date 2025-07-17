from typing import Dict, Any, Optional
from pydantic import BaseModel
from rag_system.agents.base_agent import BaseAgent, AgentRequest, AgentResponse
from rag_system.core.llm_provider import LLMProvider

class EditorRequest(AgentRequest):
    """Request model for Editor Agent"""
    text: str
    instructions: str
    parameters: Dict[str, Any] = {}

class EditorAgent(BaseAgent):
    """Agent responsible for editing and refining existing text"""
    
    def __init__(self, llm_provider: LLMProvider):
        super().__init__(agent_type="editor")
        self.llm_provider = llm_provider
        
    async def execute(self, request: EditorRequest) -> AgentResponse:
        """
        Execute the editing operation.
        
        Args:
            request: The editing request containing text and instructions
            
        Returns:
            AgentResponse containing the edited text
        """
        try:
            # Create the editing prompt
            prompt = f"""Edit the following text according to these instructions:
            
            Instructions: {request.instructions}
            
            Original text:
            {request.text}
            
            Edited version:"""
            
            # Create LLM request
            llm_request = {
                "prompt": prompt,
                "model": "llama2",
                "parameters": request.parameters
            }
            
            # Generate edited text using LLM
            response = await self.llm_provider.generate(llm_request)
            
            return AgentResponse(
                result={
                    "original_text": request.text,
                    "edited_text": response.text,
                    "instructions": request.instructions
                },
                metadata={
                    "agent_type": self.agent_type,
                    "model": response.metadata.get("model"),
                    "tokens_used": response.metadata.get("tokens_used")
                }
            )
            
        except Exception as e:
            raise Exception(f"Editing failed: {str(e)}")
