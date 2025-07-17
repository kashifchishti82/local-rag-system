import ollama
import requests
import numpy as np
from typing import List, Dict, Optional
from .base_provider import BaseEmbeddingProvider

class OllamaProvider(BaseEmbeddingProvider):
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral"):
        self.base_url = base_url
        self.model = model

    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a single text."""
        url = f"{self.base_url}/api/embeddings"
        
        response = requests.post(
            url,
            json={
                "model": self.model,
                "prompt": text
            }
        )
        response.raise_for_status()
        return response.json()["embedding"]

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts."""
        url = f"{self.base_url}/api/embeddings"
        
        response = requests.post(
            url,
            json={
                "model": self.model,
                "prompt": "\n".join(texts)
            }
        )
        response.raise_for_status()
        return response.json()["embedding"]
