# Retrieval-Augmented Generation (RAG) System

A modular system for ingesting documents, managing AI agents, and generating content using RAG architecture.

## Features

- Document ingestion and processing
- Semantic search and retrieval
- AI agent workflows (Q&A, co-authoring, editing)
- Role-based authentication and authorization
- Support for multiple embedding providers (Ollama, OpenAI)
- Vector store integration (Faiss)

## Prerequisites

- Python 3.8+
- MySQL 8.0+
- Ollama (optional, for local embeddings)
- OpenAI API key (optional, for OpenAI embeddings)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rag-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r backend/requirements.txt
pip install -r frontend/package.json
```

4. Set up environment variables:
Copy `backend/.env.example` to `backend/.env` and update the values:
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your MySQL connection details:
```
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=rag_system

# Other configurations...
```

## Database Setup

1. Create the database:
```sql
CREATE DATABASE rag_system;
```

2. Initialize the database and create initial migration:
```bash
# Initialize database
python -c "from rag_system.db import init_db; init_db()"

# Create initial migration
python scripts/db.py migrate "initial migration"

# Apply migration
python scripts/db.py upgrade
```

### Database Migration Commands

The project uses Alembic for database migrations. Here are the available commands:

1. Create a new migration:
```bash
python scripts/db.py migrate "description of changes"
```

2. Apply migrations:
```bash
python scripts/db.py upgrade
```

3. Rollback migrations:
```bash
python scripts/db.py downgrade
```

4. Initialize database (only needed once):
```bash
python scripts/db.py init
```

## Running the Application

### Backend

1. Run the backend server:
```bash
cd backend
uvicorn main:app --reload
```

The backend will run on `http://localhost:8000`

### Frontend

1. Install frontend dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## API Documentation

Once the backend is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

All configuration is managed through environment variables. See `backend/.env.example` for available options.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
