from typing import Dict, Any
from .base_provider import BaseEmbeddingProvider
from .ollama_provider import OllamaProvider
from .openai_provider import OpenAIProvider

class EmbeddingProviderFactory:
    @staticmethod
    def create_provider(provider_type: str, config: Dict[str, Any]) -> BaseEmbeddingProvider:
        """
        Create an embedding provider based on the provider type.
        
        Args:
            provider_type: Type of provider ('ollama' or 'openai')
            config: Configuration dictionary containing provider-specific settings
        
        Returns:
            BaseEmbeddingProvider instance
        """
        if provider_type.lower() == 'ollama':
            return OllamaProvider(
                base_url=config.get('base_url', 'http://localhost:11434'),
                model=config.get('model', 'mistral')
            )
        elif provider_type.lower() == 'openai':
            return OpenAIProvider(
                api_key=config['api_key'],
                model=config.get('model', 'text-embedding-ada-002')
            )
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")
