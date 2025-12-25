"""
Chat API route.
Handles chat requests with RAG-enhanced responses.
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.rag_service import rag_service

router = APIRouter()


@router.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint with RAG-enhanced responses.

    Args:
        request: ChatRequest with message and optional session_id

    Returns:
        ChatResponse with AI answer and metadata
    """
    try:
        result = await rag_service.chat(
            query=request.message,
            session_id=request.session_id
        )

        if result.get("mode") == "error":
            raise HTTPException(status_code=500, detail=result.get("answer"))

        return ChatResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
