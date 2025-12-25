"""
FastAPI application for Mili AI Assistant.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import chat, ingest, health

# Create FastAPI app
app = FastAPI(
    title="Mili AI Assistant API",
    description="RAG-powered AI assistant for Openfolio portfolio",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(ingest.router)
app.include_router(health.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Mili AI Assistant API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "chat": "/api/chat",
            "ingest": "/api/ingest",
            "ingest_directory": "/api/ingest-directory",
            "health": "/api/health"
        }
    }


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print("Mili AI Assistant starting up...")
    print(f"Embedding model: {settings.embedding_model}")
    print(f"Database path: {settings.database_path}")
    print(f"LLM base URL: {settings.anthropic_base_url}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
