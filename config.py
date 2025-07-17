from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings
from typing import List
from pydantic import Field
from typing import Union
from pydantic.networks import AnyHttpUrl

load_dotenv()

class Settings(BaseSettings):
    # LLM Provider Settings
    LLM_PROVIDER_TYPE: str = "ollama"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "text-embedding-ada-002"

    # Vector Store Settings
    VECTOR_STORE_TYPE: str = "faiss"

    # API Settings
    API_HOST: str = "localhost"
    API_PORT: int = 8000

    # CORS Settings
    CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = Field(default_factory=lambda: ["http://localhost:3000"])

    # Authentication Settings
    JWT_SECRET_KEY: str = "your-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API Configuration
    API_TITLE: str = "RAG System API"
    API_DESCRIPTION: str = "API for Retrieval-Augmented Generation System"
    API_VERSION: str = "1.0.0"
    CONTACT_NAME: str = "Your Name"
    CONTACT_EMAIL: str = "your@email.com"
    LICENSE_NAME: str = "MIT"
    LICENSE_URL: str = "https://opensource.org/licenses/MIT"

    # Database Configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "rag_system"

    @property
    def DB_URL(self) -> str:
        """Return the database URL."""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
