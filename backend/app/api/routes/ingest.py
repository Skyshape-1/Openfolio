"""
Ingest API route.
Handles PDF document upload and ingestion into vector database.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import IngestResponse
from app.services.rag_service import rag_service
from app.utils.file_handler import save_uploaded_file, validate_pdf_file
from pathlib import Path

router = APIRouter()


@router.post("/api/ingest", response_model=IngestResponse)
async def ingest_pdf(file: UploadFile = File(...)):
    """
    Upload and process PDF into vector store.

    Args:
        file: Uploaded PDF file

    Returns:
        IngestResponse with ingestion status
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        # Read file content
        content = await file.read()

        # Validate file size
        from app.core.config import settings
        if len(content) > settings.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum allowed size of {settings.max_file_size} bytes"
            )

        # Save file temporarily
        file_path = save_uploaded_file(content, file.filename)

        # Ingest into vector store
        result = await rag_service.ingest_pdf(file_path, metadata={"source": file.filename})

        return IngestResponse(**result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@router.post("/api/ingest-directory", response_model=IngestResponse)
async def ingest_directory(directory: str = "./documents"):
    """
    Ingest all PDFs from a directory into vector store.

    Args:
        directory: Path to documents directory

    Returns:
        IngestResponse with ingestion status
    """
    try:
        result = await rag_service.ingest_from_directory(directory)
        return IngestResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Directory ingestion failed: {str(e)}")
