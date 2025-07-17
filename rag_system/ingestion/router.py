from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from . import services
from .schemas import IngestionConfig


router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"],
)

@router.post("/upload", summary="Upload a document for ingestion")
def upload_document(
    config: IngestionConfig = Depends(), 
    file: UploadFile = File(...)
):
    """
    Upload a document (Markdown, PDF, DOCX, etc.) to the system.

    The file will be saved, and its content and metadata will be extracted.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file name provided.")

    try:
        result = services.save_and_process_file(file, config)
        return {"filename": file.filename, "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
