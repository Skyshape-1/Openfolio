# RAG System Implementation Report

This report outlines the current implementation of the Retrieval-Augmented Generation (RAG) system in Openfolio and provides instructions on how to manage documents and ingestion.

## 1. System Overview
The AI assistant "Mili" uses a RAG pipeline to provide context-aware answers based on PDF documents.
- **Framework**: LangChain & FastAPI
- **Vector Database**: ChromaDB (stored in `backend/chroma_db`)
- **Embeddings**: Local `SentenceTransformer` (model: `all-MiniLM-L6-v2`)
- **LLM**: Anthropic Claude (via custom or official endpoint)

## 2. Document Storage
To add new knowledge to Mili, you should place your PDF documents in the following directory:

**Path**: `backend/data/documents/`

> [!NOTE]
> The system currently expects `.pdf` files. Other formats may require additional loaders in `rag_service.py`.

## 3. Ingestion Workflow
Once you have added documents to the folder, you need to "ingest" them into the vector database. This process involves reading the PDFs, splitting them into chunks, creating embeddings, and storing them in ChromaDB.

### Method A: Call the Ingestion API (Recommended)
You can trigger a directory-wide ingestion using a simple `curl` command (or any HTTP client like Postman/Insomnia):

```bash
curl -X POST http://localhost:8000/api/ingest-directory
```

### Method B: Manual Test Script
You can also use the existing test script which performs various API checks, although it is primarily for testing connectivity:

```bash
cd backend
python -m backend.tests.test_api
```

### Method C: Single File Upload
If you want to upload a specific file from elsewhere without moving it to the `data/documents` folder first:

```bash
curl -X POST -F "file=@/path/to/your/document.pdf" http://localhost:8000/api/ingest
```

## 4. Technical Details
- **Chunking Strategy**: `RecursiveCharacterTextSplitter` with `chunk_size=1000` and `chunk_overlap=200`.
- **Retrieval**: Uses similarity search to find the top 4 most relevant chunks for each query.
- **Service Logic**: Located in `backend/app/services/rag_service.py`.
- **API Routes**: Located in `backend/app/api/routes/ingest.py`.

## 5. Summary of Actions
1. **Place** your PDF in `backend/data/documents/`.
2. **Run** the ingestion command: `curl -X POST http://localhost:8000/api/ingest-directory`.
3. **Verify** by asking Mili a question related to the new document.
