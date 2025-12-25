"""
Pydantic models for API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User message", min_length=1, max_length=2000)
    session_id: Optional[str] = Field(default="default", description="Session identifier for conversation history")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str = Field(..., description="AI response")
    sources: List[Dict[str, Any]] = Field(default_factory=list, description="Source documents used")
    document_count: int = Field(default=0, description="Number of documents in vector store")
    mode: str = Field(..., description="Response mode (rag, direct_llm, error)")


class IngestResponse(BaseModel):
    """Response model for document ingestion."""
    status: str = Field(..., description="Status (success, error, warning)")
    message: str = Field(..., description="Status message")
    ingested: Optional[int] = Field(default=None, description="Number of documents ingested")
    total: Optional[int] = Field(default=None, description="Total number of documents")
    total_chunks: Optional[int] = Field(default=None, description="Total number of chunks created")
    details: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="Detailed results per document")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Service status")
    services: Dict[str, Any] = Field(default_factory=dict, description="Status of individual services")
    version: str = Field(default="1.0.0", description="API version")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
