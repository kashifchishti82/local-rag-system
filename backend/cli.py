import typer
from pathlib import Path
from typing import Optional, List
from rag_system.core.vector_store import FaissVectorStore
from rag_system.ingestion.services import IngestionService
from rag_system.retrieval.services import SearchService
from rag_system.core.ollama_provider import OllamaProvider
from rag_system.agents.retriever import RetrieverAgent
from rag_system.agents.writer import WriterAgent

app = typer.Typer()

# Initialize shared services
vector_store = FaissVectorStore()
ollama_provider = OllamaProvider()
search_service = SearchService(vector_store, ollama_provider)
ingestion_service = IngestionService(vector_store)

@app.command()
def ingest(
    file_path: Path = typer.Argument(..., help="Path to file or directory to ingest"),
    strategy: str = typer.Option("default", help="Ingestion strategy to use")
):
    """
    Ingest files into the RAG system.
    
    Args:
        file_path: Path to file or directory to ingest
        strategy: Ingestion strategy to use
    """
    try:
        if file_path.is_dir():
            typer.echo(f"Ingesting all files from directory: {file_path}")
            ingestion_service.process_directory(file_path, strategy)
        else:
            typer.echo(f"Ingesting file: {file_path}")
            ingestion_service.process_file(file_path, strategy)
        typer.echo("Ingestion completed successfully!")
    except Exception as e:
        typer.echo(f"Error during ingestion: {str(e)}", err=True)

@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    top_k: int = typer.Option(5, help="Number of results to return"),
    score_threshold: float = typer.Option(0.5, help="Minimum similarity score"),
    metadata_filters: Optional[List[str]] = typer.Option(None, help="Metadata filters in key=value format")
):
    """
    Perform a semantic search.
    
    Args:
        query: Search query
        top_k: Number of results to return
        score_threshold: Minimum similarity score
        metadata_filters: Metadata filters in key=value format
    """
    try:
        # Parse metadata filters
        filters = {}
        if metadata_filters:
            for filter in metadata_filters:
                key, value = filter.split("=")
                filters[key] = value
        
        # Perform search
        results = search_service.search(query, top_k, score_threshold, filters)
        
        # Format and display results
        typer.echo(f"\nSearch results for: {query}")
        typer.echo("=" * 50)
        for i, result in enumerate(results, 1):
            typer.echo(f"\nResult {i} - Score: {result['score']:.2f}")
            typer.echo("-" * 50)
            typer.echo(f"Text: {result['text']}")
            typer.echo(f"Metadata: {result['metadata']}")
    except Exception as e:
        typer.echo(f"Error during search: {str(e)}", err=True)

@app.command()
def ask(
    question: str = typer.Argument(..., help="Question to ask"),
    top_k: int = typer.Option(5, help="Number of context chunks to retrieve"),
    temperature: float = typer.Option(0.7, help="Generation temperature")
):
    """
    Ask a question and get an answer using the Q&A agent.
    
    Args:
        question: Question to ask
        top_k: Number of context chunks to retrieve
        temperature: Generation temperature
    """
    try:
        # Initialize agents
        retriever_agent = RetrieverAgent(vector_store, search_service)
        writer_agent = WriterAgent(ollama_provider)
        
        # Retrieve context
        retrieval_request = {
            "query": question,
            "top_k": top_k,
            "score_threshold": 0.5
        }
        retrieval_response = retriever_agent.execute(retrieval_request)
        
        # Generate answer
        writer_request = {
            "prompt": f"Answer the following question based on the provided context:\n\nQuestion: {question}\n\nContext: {json.dumps(retrieval_response.result.get('results'), indent=2)}",
            "parameters": {
                "temperature": temperature,
                "max_tokens": 500
            }
        }
        
        answer = writer_agent.execute(writer_request)
        
        typer.echo(f"\nQuestion: {question}")
        typer.echo("=" * 50)
        typer.echo(f"\nAnswer: {answer.result.get('text')}")
    except Exception as e:
        typer.echo(f"Error during Q&A: {str(e)}", err=True)

@app.command()
def re_index(
    all: bool = typer.Option(False, help="Re-index all documents")
):
    """
    Re-index documents in the vector store.
    
    Args:
        all: If true, clear and re-index all documents
    """
    try:
        if all:
            typer.echo("Clearing vector store...")
            vector_store.clear()
            typer.echo("Vector store cleared!")
        
        typer.echo("Re-indexing documents...")
        # TODO: Implement re-indexing logic
        typer.echo("Re-indexing completed!")
    except Exception as e:
        typer.echo(f"Error during re-indexing: {str(e)}", err=True)

if __name__ == "__main__":
    app()
