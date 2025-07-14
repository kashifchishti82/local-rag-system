# Epic 1: Ingestion & Preprocessing Workflow

This document outlines the development workflow for the features related to document ingestion and preprocessing.

## User Stories Covered

- **US1.1:** As a user, I want to upload Markdown documents for ingestion.
- **US1.2:** As the system, I should extract metadata and structure from each document.
- **US1.3:** As a developer, I want configurable chunking rules (headings, code blocks, length).

## Implementation Steps

### 1. Project Setup
- **Virtual Environment:** A Python virtual environment was created at `c:\Work\Development\Python\rag-system\venv` to isolate project dependencies.
- **Dependencies:** A `requirements.txt` file was created and populated with the necessary libraries:
  - `fastapi`: For the core web application.
  - `uvicorn`: As the ASGI server to run the app.
  - `python-multipart`: To handle file uploads.
  - `python-frontmatter`: To parse metadata from Markdown files.
  - `python-docx`, `pypdf`, `python-markdown`: For handling various document formats.
- **Directory Structure:** The initial project structure was created, including the main `rag_system` package, an `ingestion` sub-module, and an `uploads` directory.

### 2. Core Application
- A basic FastAPI application was initialized in `main.py`.
- The application includes a health check endpoint at `/`.

### 3. Ingestion Endpoint (US1.1 & US1.2)
- An API router was created at `rag_system/ingestion/router.py` to define the `/ingest` endpoints.
- A `/upload` endpoint was added to accept `POST` requests with file uploads.
- A service layer was created at `rag_system/ingestion/services.py` to handle the business logic of saving and processing uploaded files.
- The service now supports multiple file formats:
  - **Markdown (`.md`):** Extracts frontmatter metadata and content.
  - **PDF (`.pdf`):** Extracts text from PDF documents.
  - **DOCX (`.docx`):** Extracts text from Word documents.
  - **Plain Text (`.txt`):** Reads content from text files.

### 4. Configurable Chunking (US1.3)
- **Chunking Logic:** A dedicated module for text splitting was created at `rag_system/ingestion/chunking.py`.
  - Implemented `chunk_by_length` for basic size-based chunking.
  - Implemented `chunk_by_headings` to split Markdown content based on its semantic structure.
- **Configuration Schema:** A `schemas.py` file was added to the `ingestion` module to define Pydantic models for configuration.
  - `IngestionConfig` allows users to select a `ChunkingStrategy` (LENGTH or HEADINGS) and specify parameters like `chunk_size` and `chunk_overlap`.
- **Integration:**
  - The `upload_document` endpoint in the router was updated to accept the `IngestionConfig` as a dependency.
  - The `save_and_process_file` service was updated to use the provided configuration to apply the selected chunking strategy dynamically.
- **Code Block Cleaning:** A preprocessing step was added to `rag_system/ingestion/chunking.py` to clean and normalize code blocks within Markdown files before chunking. This improves the quality of the text for language models.

### 5. Running & Testing
- The application was started with `uvicorn` in reload mode.
- A browser preview was provided to access the interactive API documentation at `http://127.0.0.1:8000/docs` for testing.
