"""
File handling utilities for PDF processing.
"""
import os
import shutil
from pathlib import Path
from typing import Optional
from app.core.config import settings


def ensure_upload_dir() -> Path:
    """Ensure upload directory exists."""
    upload_path = Path(settings.upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)
    return upload_path


def save_uploaded_file(file_content: bytes, filename: str) -> str:
    """
    Save uploaded file to upload directory.

    Args:
        file_content: File content as bytes
        filename: Name of the file

    Returns:
        Full path to saved file
    """
    upload_dir = ensure_upload_dir()
    file_path = upload_dir / filename

    with open(file_path, "wb") as f:
        f.write(file_content)

    return str(file_path)


def delete_file(file_path: str) -> bool:
    """
    Delete a file from the filesystem.

    Args:
        file_path: Path to the file

    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        Path(file_path).unlink()
        return True
    except Exception:
        return False


def get_file_size(file_path: str) -> int:
    """Get file size in bytes."""
    return Path(file_path).stat().st_size


def validate_pdf_file(file_path: str) -> bool:
    """
    Validate if a file is a valid PDF.

    Args:
        file_path: Path to the file

    Returns:
        True if valid PDF, False otherwise
    """
    path = Path(file_path)

    # Check extension
    if path.suffix.lower() != '.pdf':
        return False

    # Check file exists
    if not path.exists():
        return False

    # Check file size
    file_size = get_file_size(file_path)
    if file_size > settings.max_file_size:
        return False

    # Check PDF header
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            return header == b'%PDF'
    except Exception:
        return False


def get_documents_from_directory(directory: str = "./data/documents") -> list[str]:
    """
    Get all PDF files from the documents directory.

    Args:
        directory: Path to documents directory

    Returns:
        List of PDF file paths
    """
    docs_dir = Path(directory)
    if not docs_dir.exists():
        return []

    return [str(f) for f in docs_dir.glob("*.pdf")]
