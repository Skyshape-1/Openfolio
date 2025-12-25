"""
Health check API route.
"""
from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.services.rag_service import rag_service
from app.core.config import settings

router = APIRouter()


@router.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns:
        HealthResponse with service status
    """
    vector_stats = rag_service.get_vector_store_stats()

    return HealthResponse(
        status="healthy" if vector_stats.get("status") == "healthy" else "degraded",
        services={
            "vector_store": vector_stats.get("status", "unknown"),
            "document_count": vector_stats.get("document_count", 0),
            "embedding_model": vector_stats.get("embedding_model", "unknown"),
            "llm": "connected",
            "llm_base_url": settings.anthropic_base_url
        },
        version="1.0.0"
    )
