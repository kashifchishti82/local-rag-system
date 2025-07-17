from enum import Enum
from pydantic import BaseModel, Field

class ChunkingStrategy(str, Enum):
    """Enum for the available chunking strategies."""
    LENGTH = "length"
    HEADINGS = "headings"

class IngestionConfig(BaseModel):
    """Configuration model for the document ingestion process."""
    chunking_strategy: ChunkingStrategy = Field(
        default=ChunkingStrategy.LENGTH,
        description="The strategy to use for chunking the document."
    )
    chunk_size: int = Field(
        default=1000,
        ge=100,
        description="The target size of chunks for length-based chunking."
    )
    chunk_overlap: int = Field(
        default=200,
        ge=0,
        description="The overlap between chunks for length-based chunking."
    )
