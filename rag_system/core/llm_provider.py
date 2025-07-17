from typing import Dict, Any, Optional
from pydantic import BaseModel
import json

class LLMRequest(BaseModel):
    """Base model for LLM requests"""
    prompt: str
    model: str = "llama2"
    parameters: Dict[str, Any] = {}

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Write a summary of this document",
                "model": "llama2",
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            }
        }

class LLMResponse(BaseModel):
    """Base model for LLM responses"""
    text: str
    metadata: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "text": "This is the generated text",
                "metadata": {
                    "model": "llama2",
                    "tokens_used": 150
                }
            }
        }

class LLMProvider:
    """Provider class for interacting with LLMs"""
    
    def __init__(self):
        self.base_url = "http://localhost:11434/api/generate"
        
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate text using the specified LLM model.
        
        Args:
            request: The generation request containing prompt and parameters
            
        Returns:
            LLMResponse containing the generated text and metadata
        """
        try:
            # This is a placeholder for actual LLM integration
            # In a real implementation, this would make an HTTP request to Ollama
            response = {
                "text": "Generated text from LLM",
                "metadata": {
                    "model": request.model,
                    "tokens_used": 150
                }
            }
            return LLMResponse(**response)
            
        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")
