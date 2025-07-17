from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel

class AgentRequest(BaseModel):
    """Base model for agent requests"""
    pass

class AgentResponse(BaseModel):
    """Base model for agent responses"""
    result: Dict[str, Any]
    metadata: Dict[str, Any]
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {},
                "metadata": {
                    "agent_type": "base",
                    "execution_time": "0.123"
                }
            }
        }

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        
    @abstractmethod
    async def execute(self, request: AgentRequest) -> AgentResponse:
        """
        Execute the agent's core functionality.
        
        Args:
            request: The agent-specific request data
            
        Returns:
            AgentResponse containing the result and metadata
        """
        pass

    async def validate_request(self, request: AgentRequest) -> bool:
        """
        Validate the incoming request.
        
        Args:
            request: The agent-specific request data
            
        Returns:
            bool: True if request is valid, False otherwise
        """
        return True

    def get_agent_type(self) -> str:
        """Get the type of the agent"""
        return self.agent_type
