---
description: Epic 5 API & CLI Access Layer
---

This document outlines the development workflow for providing both a RESTful API and a Command-Line Interface (CLI) for interacting with the RAG system.

## User Stories Covered

- **US5.1:** As a CLI user, I want to ingest files, re-embed, and query locally.
- **US5.2:** As a frontend, I want REST endpoints for chunking, search, and generation.

## Planned Implementation Steps

### 1. REST API Review (US5.2)

- The core of this user story has been built incrementally throughout the previous epics.
- This step involves a final review and consolidation of all existing FastAPI endpoints:
  - **Ingestion (`/ingest`):** Review the file upload and processing endpoint.
  - **Search (`/retrieve`):** Review the semantic search endpoint.
  - **Generation (`/agents`):** Review the endpoints that trigger agentic workflows (Q&A, co-authoring, etc.).
- **API Documentation:** Ensure all endpoints have clear and comprehensive OpenAPI documentation (via FastAPI's automatic docs) with proper schemas for requests and responses.
- **CORS Configuration:** Add a CORS (Cross-Origin Resource Sharing) middleware to the FastAPI app to allow a frontend application (served from a different origin) to securely interact with the API.

### 2. CLI Implementation (US5.1)

- **Dependency:** The `typer` library will be added to `requirements.txt` as it provides a modern and easy way to build powerful CLIs.
- **CLI Application:** A new file, `cli.py`, will be created in the root directory of the project.
- **Command Structure:** The CLI will be structured with sub-commands to mirror the API's functionality:
  - `rag-cli ingest <file_path> [--strategy <name>]`: A command to ingest a single file or a directory of files.
  - `rag-cli search "<query>" [--top-k <n>]`: A command to perform a semantic search and print the results to the console.
  - `rag-cli ask "<question>"`: A command that uses the Q&A agent to answer a question directly from the terminal.
  - `rag-cli re-index --all`: A command to manage the vector store, such as clearing and re-indexing all documents.
- **Reusing Logic:** The CLI commands will not duplicate logic. They will directly import and call the service functions already created for the API (e.g., `ingestion.services.save_and_process_file`, `retrieval.services.SearchService`). This ensures consistency between the API and CLI.
- **Configuration:** The CLI will need a way to configure settings like the Ollama model to use. This can be handled via command-line options or a simple configuration file.
