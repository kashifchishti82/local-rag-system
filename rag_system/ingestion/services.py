import docx
import frontmatter
import pypdf
import numpy as np

from .chunking import chunk_by_length, chunk_by_headings, clean_code_blocks
from .schemas import IngestionConfig, ChunkingStrategy
from ..vector_store.faiss_store import FaissVectorStore
from ..embeddings.provider_factory import EmbeddingProviderFactory
import shutil
from pathlib import Path
from fastapi import UploadFile

UPLOAD_DIRECTORY = Path("uploads")
UPLOAD_DIRECTORY.mkdir(exist_ok=True)

# Initialize the vector store. In a production app, this might be managed differently.
vector_store = FaissVectorStore()
# Initialize the embedding provider
provider_config = {
    "provider_type": "ollama",
    "config": {
        "base_url": "http://localhost:11434",
        "model": "mistral"
    }
}
provider = EmbeddingProviderFactory.create_provider(**provider_config)


def _process_pdf(path: Path) -> str:
    """Extracts text content from a PDF file."""
    with path.open("rb") as f:
        reader = pypdf.PdfReader(f)
        return "\n".join(page.extract_text() for page in reader.pages)


def _process_docx(path: Path) -> str:
    """Extracts text content from a DOCX file."""
    doc = docx.Document(path)
    return "\n".join(para.text for para in doc.paragraphs)


def _process_txt(path: Path) -> str:
    """Reads content from a plain text file."""
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def save_and_process_file(file: UploadFile, config: IngestionConfig):
    """Saves an uploaded file and processes it to extract metadata and content."""
    try:
        # Save the uploaded file
        file_path = UPLOAD_DIRECTORY / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process the file
        content = ""
        metadata = {}

        # Process the file based on its extension
        if file.filename.endswith(".md"):
            post = frontmatter.load(file_path)
            content = clean_code_blocks(post.content)
            metadata = post.metadata
        elif file.filename.endswith(".pdf"):
            content = _process_pdf(file_path)
        elif file.filename.endswith(".docx"):
            content = _process_docx(file_path)
        elif file.filename.endswith(".txt"):
            content = _process_txt(file_path)
        else:
            return {"message": f"File type for '{file.filename}' is not supported."}

        # Select chunking strategy
        chunks = []
        if config.chunking_strategy == ChunkingStrategy.HEADINGS and file.filename.endswith(".md"):
            chunks = chunk_by_headings(content)
        else:
            # Default to length-based chunking for non-markdown files or if specified
            chunks = chunk_by_length(
                content,
                chunk_size=config.chunk_size,
                chunk_overlap=config.chunk_overlap
            )

        if not chunks:
            return {"message": f"File '{file.filename}' processed, but no content was chunked."}

        # Generate embeddings for the chunks
        embeddings = provider.get_embeddings(chunks)

        # Prepare metadata for each chunk
        chunk_metadatas = [
            {
                **metadata, # Document-level metadata
                "file_origin": file.filename,
                "chunk_index": i,
            }
            for i in range(len(chunks))
        ]

        # Add to the vector store
        vector_store.add(chunks, embeddings, chunk_metadatas)
        vector_store.save()

        return {
            "message": f"Successfully ingested and indexed {len(chunks)} chunks from {file.filename}.",
            "chunk_count": len(chunks),
            "file_metadata": metadata,
        }
    finally:
        # The file object must be closed.
        file.file.close()
