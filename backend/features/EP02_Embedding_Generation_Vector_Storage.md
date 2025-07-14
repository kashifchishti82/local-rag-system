# Epic 2: Embedding Generation & Vector Storage

This document outlines the development workflow for generating embeddings from text chunks and storing them in a vector database.

## User Stories Covered

- **US2.1:** As the system, I should generate embeddings for each chunk.
- **US2.2:** As a user, I want to re-index documents when updated.
- **US2.3:** As an admin, I want each chunk to store metadata (title, section, file origin).

## Planned Implementation Steps

1.  **Dependency Installation:** Add and install `ollama` for embedding generation and `faiss-cpu` for the local vector store.
2.  **Module Creation:**
    - Create an `embeddings` module to handle communication with embedding model providers like Ollama.
    - Create a `vector_store` module to abstract the vector database operations (e.g., adding, searching, saving).
3.  **FAISS Implementation:** Implement a `FaissVectorStore` class that manages the FAISS index and a separate mapping for storing metadata and document content, fulfilling US2.3.
4.  **Ollama Integration:** Implement a provider function or class to connect to a local Ollama instance and generate embeddings for text chunks (US2.1).
5.  **Service Integration:** Update the `ingestion` service to call the embedding provider and the vector store after chunking a document. This will complete the ingestion pipeline from raw file to stored vector.
6.  **Re-indexing Strategy (US2.2):** Initially, a simple re-indexing approach will be implemented (e.g., clearing the index for a document and re-ingesting). More advanced strategies can be developed later.
