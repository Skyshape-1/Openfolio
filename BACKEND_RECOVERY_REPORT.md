# Mili Backend Recovery Report
**Generated:** December 25, 2025
**Status:** ⚠️ **Backend exists but fails to activate**

---

## Executive Summary

The backend folder **exists on disk** but is **not tracked by git**. It contains a complete FastAPI RAG (Retrieval-Augmented Generation) system for the Mili AI Assistant, but fails to start due to missing SSL certificate bundles and network connectivity issues with HuggingFace.

### Key Finding
The backend was created **after commit 706ffc32** (Mili V1.0 Integrated) and was never committed to git. When you restored to 706ffc32, the backend folder remained on disk because it wasn't being tracked, but it's in a broken state.

---

## Backend Architecture

### Technology Stack
- **Framework:** FastAPI
- **LLM:** Anthropic Claude (via custom endpoint at `api.vectorengine.ai`)
- **Vector Database:** ChromaDB
- **Embeddings:** SentenceTransformers (all-MiniLM-L6-v2)
- **Document Processing:** LangChain with PyPDF
- **Python Version:** 3.12.1

### File Structure
```
backend/
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── test_api.py               # API testing script
├── .env                      # Environment configuration
├── venv/                     # Python virtual environment (3.12.1)
├── chroma_db/                # Vector database persistence
├── app/
│   ├── __init__.py
│   ├── core/
│   │   └── config.py         # Settings management
│   ├── models/
│   │   └── schemas.py        # Pydantic models
│   ├── services/
│   │   └── rag_service.py    # RAG implementation
│   ├── utils/
│   │   └── file_handler.py   # File utilities
│   └── api/
│       └── routes/
│           ├── chat.py       # Chat endpoint
│           ├── ingest.py     # Document ingestion
│           └── health.py     # Health check
└── uploads/                  # Document upload directory (empty)
```

### API Endpoints
- `GET /` - Root endpoint with API info
- `POST /api/chat` - RAG-powered chat with Mili
- `POST /api/ingest` - Upload and ingest PDF documents
- `POST /api/ingest-directory` - Ingest all PDFs from a directory
- `GET /api/health` - Health check and vector store stats

---

## Current Issues

### Issue 1: SSL Certificate Bundle Missing ❌
**Error:**
```
OSError: Could not find a suitable TLS CA certificate bundle,
invalid path: C:\Users\...\backend\venv\Lib\site-packages\certifi\cacert.pem
```

**Root Cause:**
The `certifi` package is installed but the CA certificate bundle is missing or corrupted. This happens when the venv is copied or moved instead of being recreated.

**Impact:**
Blocks all HTTPS requests, including:
- HuggingFace model downloads (SentenceTransformers)
- Anthropic API calls
- ChromaDB operations

### Issue 2: Git Tracking History 📝
**Problem:**
The backend folder was never committed to git history. Evidence:
- `git log --all --oneline -- backend/` only shows commits 191253d9 and 706ffc32 (which are .gitignore changes, not backend code)
- Commit 191253d9 added Python-specific .gitignore entries **after** the backend was created
- The backup-broken-state branch doesn't contain backend files (they were untracked)

**Timeline:**
1. Commit 706ffc32 - "Mili V1.0 Integrated" (backend doesn't exist)
2. Backend created with AI assistant features
3. Commit 191253d9 - ".gitignore updated to exclude backend/venv, backend/chroma_db, etc."
4. Later commits added staged backend files but they were never committed
5. Git reset removed the staged files, leaving backend on disk but broken

---

## Recovery Options

### Option A: Fix SSL Certificates (Recommended) ⭐

**Pros:**
- Fastest recovery
- Keeps all existing code and configuration
- Preserves ChromaDB data (if any documents ingested)

**Steps:**

1. **Reinstall certifi package:**
   ```bash
   cd backend
   venv/Scripts/python -m pip install --force-reinstall certifi
   ```

2. **Verify certificate bundle:**
   ```bash
   venv/Scripts/python -c "import certifi; print(certifi.where())"
   ```

3. **Test backend startup:**
   ```bash
   venv/Scripts/python main.py
   ```

4. **If network issues persist**, set environment variable to use system certificates:
   ```bash
   set REQUESTS_CA_BUNDLE=<path-to-system-ca-bundle>
   # Or disable SSL verification (NOT recommended for production)
   set PYTHONHTTPSVERIFY=0
   ```

### Option B: Recreate Virtual Environment

**Pros:**
- Clean slate with all packages fresh
- Eliminates venv corruption issues

**Steps:**

1. **Delete existing venv:**
   ```bash
   cd backend
   rm -rf venv/
   ```

2. **Create new venv:**
   ```bash
   python -m venv venv
   ```

3. **Install dependencies:**
   ```bash
   venv/Scripts/pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   venv/Scripts/python main.py
   ```

### Option C: Commit Backend to Git (Prevent Future Loss)

**After fixing the backend, commit it properly:**

1. **Update .gitignore** (already done in commit 191253d9):
   - ✅ `backend/venv/` - Virtual environment
   - ✅ `backend/chroma_db/` - Vector database
   - ✅ `backend/.env` - API keys
   - ✅ `backend/uploads/` - Uploaded files
   - ✅ `__pycache__/` - Python cache
   - ✅ `*.py[cod]` - Compiled Python files

2. **Stage and commit backend code:**
   ```bash
   git add backend/*.py backend/app/ backend/requirements.txt
   git commit -m "feat: add Mili AI Assistant backend with RAG support

   - FastAPI backend with ChromaDB vector storage
   - RAG-powered chat using Claude API
   - PDF document ingestion and processing
   - Local embeddings with SentenceTransformers
   "
   ```

3. **Create proper backup:**
   ```bash
   git push origin clean-main
   ```

---

## Configuration Files

### backend/.env
```env
ANTHROPIC_API_KEY=sk-PftIkzWDMSamtmXICNh7HT45NXZ2nILbhMZ18K8CTXzJ7Fsn
ANTHROPIC_BASE_URL=https://api.vectorengine.ai
LLM_MODEL=claude-3-7-sonnet-20250219
DATABASE_PATH=./chroma_db
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760
CORS_ORIGINS=["http://localhost:3000"]
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

⚠️ **Security Warning:** The API key is exposed in plaintext. This file should be in .gitignore (it is) and never committed.

### Missing Configuration
The .env file references a custom Anthropic endpoint (`api.vectorengine.ai`). Ensure:
1. This endpoint is accessible and valid
2. The API key has not expired
3. The model `claude-3-7-sonnet-20250219` is available

---

## Testing Recovery

### After applying fixes, test with:

1. **Start backend:**
   ```bash
   cd backend
   venv/Scripts/python main.py
   ```

2. **Expected output:**
   ```
   Mili AI Assistant starting up...
   Embedding model: all-MiniLM-L6-v2
   Database path: ./chroma_db
   LLM base URL: https://api.vectorengine.ai
   INFO:     Started server process [XXXX]
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

3. **Test health endpoint:**
   ```bash
   curl http://localhost:8000/api/health
   ```

4. **Test chat endpoint:**
   ```bash
   curl -X POST http://localhost:8000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "Hello Mili!"}'
   ```

### Using the provided test script:
```bash
cd backend
venv/Scripts/python test_api.py
```

---

## Recommendations

### Immediate Actions
1. ✅ **Fix SSL certificates** (Option A) - Quickest path to working backend
2. ⚠️ **Test API connectivity** to `api.vectorengine.ai` - Verify custom endpoint works
3. 📝 **Document the custom Anthropic endpoint** - Is this a proxy or paid service?

### Preventing Future Data Loss
1. ✅ **Commit backend code** to git (excluding venv, chroma_db, .env, uploads)
2. ✅ **Create backup script** for ChromaDB data
3. ✅ **Document setup process** in README
4. ✅ **Add backend startup script** to npm scripts in package.json

### Long-term Improvements
1. **Dockerize the backend** - Eliminates venv issues and provides reproducible builds
2. **Use .env.example** - Template for required environment variables
3. **Add health checks** - Monitor API availability and ChromaDB status
4. **Implement proper error handling** - Graceful fallbacks when downloads fail
5. **Consider cloud vector database** - Pinecone, Weaviate for better persistence

---

## Dependencies Analysis

### Installed Packages (Selected)
- `fastapi` 0.127.0 - Web framework
- `uvicorn` - ASGI server
- `langchain` 0.1.0+ - LLM orchestration
- `langchain-anthropic` - Claude integration
- `chromadb` 1.3.7 - Vector database
- `sentence-transformers` - Local embeddings
- `anthropic` 0.75.0 - Claude SDK
- `torch` 2.1.0+ - ML backend for embeddings
- `transformers` 4.35.0+ - HuggingFace models

### Missing or Corrupted
- `certifi` - SSL certificate bundle (corrupted)
- Potentially: HuggingFace model cache (requires network download)

---

## Conclusion

The backend is **90% functional** but blocked by SSL certificate issues. The fix is straightforward (reinstall certifi or recreate venv). However, the backend was never properly committed to git, which is why it survived the git reset but is now in a broken state.

**Recommended Action Plan:**
1. Fix SSL certificates (Option A or B)
2. Test backend startup and API connectivity
3. Ingest sample documents to test RAG functionality
4. **Commit backend code to git** to prevent future loss
5. Document setup and deployment process

---

## File Locations

**Backend Root:** `C:\Users\Tangzihan Xia\OneDrive\Desktop\Kiroku Notes\Openfolio\backend\`

**Key Files:**
- [backend/main.py](backend/main.py) - Application entry point
- [backend/requirements.txt](backend/requirements.txt) - Dependencies
- [backend/app/core/config.py](backend/app/core/config.py) - Configuration
- [backend/app/services/rag_service.py](backend/app/services/rag_service.py) - Core RAG logic

**Git Backup Branch:** `backup-broken-state` (does not contain backend files)

**Target Commit:** `706ffc32` (Mili V1.0 Integrated - before backend existed)
