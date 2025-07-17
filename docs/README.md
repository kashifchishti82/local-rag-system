# Local Retrieval-Augmented Generation (RAG) System

A modular system that enables semantic search, retrieval, and AI-powered content generation over local documentation.

## Features

- Document ingestion and processing (Markdown, PDF, Word, Text)
- Semantic search using vector embeddings
- AI-powered agents for Q&A, content generation, and editing
- Command-line and REST API interfaces
- Local vector storage using FAISS
- Integration with Ollama for LLM operations

## Project Structure

```
rag-system/
├── backend/                  # Backend FastAPI application
│   ├── rag_system/          # Main application code
│   │   ├── agents/          # AI agents (Retriever, Writer, Editor, Augmentor)
│   │   ├── core/            # Core utilities (LLM provider, vector store)
│   │   ├── ingestion/       # Document ingestion system
│   │   └── retrieval/       # Semantic search system
│   ├── features/            # Feature documentation
│   ├── venv/               # Python virtual environment
│   ├── data/               # Document storage
│   └── uploads/            # Temporary file uploads
├── frontend/               # Next.js frontend application
└── README.md              # This file
```

## Installation

1. Create and activate a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure Ollama is installed and running:
```bash
# Install Ollama if not already installed
# On Windows: scoop install ollama
# On Linux/Mac: curl https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve
```

## Usage

### Command Line Interface (CLI)

The system provides a CLI interface for interacting with the RAG system:

```bash
# Ingest documents
rag-cli ingest path/to/document.pdf
rag-cli ingest path/to/documents/  # Ingest an entire directory

# Search for information
rag-cli search "how to use the system"

# Ask questions
rag-cli ask "what are the main features?"

# Re-index documents
rag-cli re-index --all
```

### REST API

The system provides a REST API with the following endpoints:

- **Ingestion**
  - POST `/ingest`: Ingest new documents
  - GET `/ingest/status`: Check ingestion status

- **Search**
  - POST `/retrieve/search`: Perform semantic search
  - GET `/retrieve/stats`: Get vector store statistics

- **Agents**
  - POST `/agents/qna`: Get answers to questions
  - POST `/agents/co-author`: Generate new content
  - POST `/agents/edit`: Edit existing content
  - POST `/agents/suggest-updates`: Suggest content updates

API documentation is available at `/docs` when the server is running.

### Running the Server

```bash
# Start the FastAPI server
uvicorn main:app --reload

# Access API documentation
http://localhost:8000/docs
```

## Development

The project is organized into several epics:

1. **Document Ingestion**
   - Handles ingestion of various document types
   - Processes and stores document content
   - Generates vector embeddings

2. **Semantic Search**
   - Implements FAISS-based vector storage
   - Provides semantic search capabilities
   - Supports metadata filtering

3. **AI Agents**
   - Retriever: Fetches relevant context
   - Writer: Generates new content
   - Editor: Refines existing content
   - Augmentor: Analyzes and suggests updates

4. **API & CLI Access**
   - REST API endpoints for all functionality
   - Command-line interface for local use
   - CORS support for frontend integration

## Configuration

The system uses environment variables for configuration:

```bash
# Vector store configuration
VECTOR_STORE_PATH=./data/vectors

# LLM configuration
OLLAMA_API_URL=http://localhost:11434
DEFAULT_LLM_MODEL=llama2
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please create an issue on the GitHub repository.
