"""
RAG (Retrieval-Augmented Generation) Service for Mili AI Assistant.

Handles document ingestion, vector storage, and retrieval-augmented chat.
"""
import os
import re
from typing import List, Dict, Any, Optional
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.utils.file_handler import get_documents_from_directory


def strip_thinking_blocks(text: str) -> str:
    """
    Remove Claude thinking blocks from response.
    Extended thinking models output <thinking>...</thinking> blocks that should be hidden.
    """
    # Remove <thinking>...</thinking> blocks (including multi-line)
    cleaned = re.sub(r'<thinking>.*?</thinking>\s*', '', text, flags=re.DOTALL | re.IGNORECASE)
    return cleaned.strip()


class LocalEmbeddings:
    """
    Local embeddings using SentenceTransformers.
    Free alternative to OpenAI embeddings.
    """

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.embedding_model
        self.model = SentenceTransformer(self.model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text: str) -> List[float]:
        """Embed a query string."""
        return self.model.encode([text], convert_to_numpy=True)[0].tolist()


class RAGService:
    """
    Main RAG service for Mili AI Assistant.

    Handles:
    - PDF document loading and chunking
    - Vector storage with ChromaDB
    - RAG-enhanced chat with Claude
    """

    def __init__(self):
        """Initialize RAG service with vector store and LLM."""
        # Initialize local embeddings
        self.embeddings = LocalEmbeddings()

        # Initialize vector store
        self.vectorstore = Chroma(
            persist_directory=settings.database_path,
            embedding_function=self.embeddings,
            collection_name="mili_documents"
        )

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

        # Initialize LLM with custom endpoint
        self.llm = ChatAnthropic(
            model=settings.llm_model,
            anthropic_api_key=settings.anthropic_api_key,
            base_url=settings.anthropic_base_url,
            temperature=0.7
        )

        # Simple chat history storage
        self.chat_history: Dict[str, List[Dict[str, str]]] = {}

    async def ingest_pdf(self, pdf_path: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process PDF and store in vector database.

        Args:
            pdf_path: Path to PDF file
            metadata: Optional metadata to attach to documents

        Returns:
            Dictionary with ingestion results
        """
        try:
            # Load PDF
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()

            # Add metadata to documents
            if metadata:
                for doc in documents:
                    doc.metadata.update(metadata)

            # Split documents into chunks
            splits = self.text_splitter.split_documents(documents)

            # Add to vector store
            self.vectorstore.add_documents(splits)

            # Persist vector store
            self.vectorstore.persist()

            return {
                "status": "success",
                "message": f"Successfully ingested {len(splits)} chunks from {Path(pdf_path).name}",
                "chunks": len(splits),
                "source": Path(pdf_path).name
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to ingest PDF: {str(e)}",
                "error": str(e)
            }

    async def ingest_from_directory(self, directory: str = "./data/documents") -> Dict[str, Any]:
        """
        Ingest all PDFs from a directory.

        Args:
            directory: Path to documents directory

        Returns:
            Dictionary with ingestion results
        """
        pdf_files = get_documents_from_directory(directory)

        if not pdf_files:
            return {
                "status": "warning",
                "message": f"No PDF files found in {directory}",
                "ingested": 0
            }

        results = []
        total_chunks = 0

        for pdf_path in pdf_files:
            result = await self.ingest_pdf(
                pdf_path,
                metadata={"source": Path(pdf_path).name}
            )
            results.append(result)
            if result["status"] == "success":
                total_chunks += result.get("chunks", 0)

        successful = sum(1 for r in results if r["status"] == "success")

        return {
            "status": "success" if successful > 0 else "error",
            "message": f"Ingested {successful}/{len(pdf_files)} documents with {total_chunks} total chunks",
            "ingested": successful,
            "total": len(pdf_files),
            "total_chunks": total_chunks,
            "details": results
        }

    async def chat(self, query: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Chat with RAG-enhanced responses.

        Args:
            query: User query
            session_id: Session identifier for conversation memory

        Returns:
            Dictionary with response and metadata
        """
        try:
            # Check if vector store has documents
            collection = self.vectorstore._collection
            doc_count = collection.count()

            if doc_count == 0:
                # Fallback to direct LLM call if no documents
                response = await self.llm.ainvoke([
                    HumanMessage(content=f"You are Mili, a helpful AI assistant for Tangzihan Xia's portfolio. Answer: {query}")
                ])
                return {
                    "answer": strip_thinking_blocks(response.content),
                    "sources": [],
                    "document_count": 0,
                    "mode": "direct_llm"
                }

            # Retrieve relevant documents
            relevant_docs = await self.vectorstore.asimilarity_search(query, k=4)

            # Create context from retrieved documents
            context = "\n\n".join([doc.page_content for doc in relevant_docs])

            # Build prompt with context
            prompt = f"""
                You are Mili, a helpful AI assistant for Tangzihan Xia's portfolio website.
                Your role is to answer questions about Tangzihan's background, skills, projects, and work experience.

                Use the following pieces of context to answer the question at the end.
                If you don't know the answer based on the context, just say that you don't know.

                Rules:
                1. Keep your answers within 1-2 paragraphs unless user asks for more detail.
                2. Try to use bullet points for clarity when listing information.
                3. Try to end your responses with 1-2 follow-up questions that the user might find interesting.

                Restrictions:
                1. Do not make up answers that are not supported by facts and context.
                2. Do not include your thought process in the final answer.

                Context:
                {context}

                Question: {query}

                Helpful Answer:
            """

            # Generate response using LLM with context
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])

            # Extract source documents
            sources = [
                {
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata
                }
                for doc in relevant_docs[:3]
            ]

            return {
                "answer": response.content,
                "sources": sources,
                "document_count": doc_count,
                "mode": "rag"
            }

        except Exception as e:
            return {
                "answer": f"I encountered an error: {str(e)}",
                "sources": [],
                "error": str(e),
                "mode": "error"
            }

    def get_vector_store_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        try:
            collection = self.vectorstore._collection
            doc_count = collection.count()

            return {
                "status": "healthy",
                "document_count": doc_count,
                "persist_directory": settings.database_path,
                "embedding_model": self.embeddings.model_name
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def clear_memory(self):
        """Clear conversation memory."""
        self.chat_history.clear()


# Global RAG service instance
rag_service = RAGService()
