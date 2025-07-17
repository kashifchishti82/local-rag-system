import openai
from typing import List, Dict, Optional
from .base_provider import BaseEmbeddingProvider

class OpenAIProvider(BaseEmbeddingProvider):
    def __init__(self, api_key: str, model: str = "text-embedding-ada-002"):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a single text."""
        response = openai.Embedding.create(
            input=text,
            model=self.model
        )
        return response.data[0].embedding

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts."""
        response = openai.Embedding.create(
            input=texts,
            model=self.model
        )
        return [item.embedding for item in response.data]
