# Openfolio

Openfolio is an intelligent portfolio website for Tangzihan Xia, featuring a clean design with MDX-based content management and an AI-powered assistant called "Mili" powered by RAG (Retrieval-Augmented Generation).

## Features

### AI-Powered Assistant (Mili)
- **RAG-Enhanced Chat**: Ask questions about the portfolio and get intelligent answers
- **Vector Database**: Uses ChromaDB for semantic document search
- **Local Embeddings**: Free, local sentence transformers for embeddings (all-MiniLM-L6-v2)
- **Document Understanding**: Ingests PDF documents to provide context-aware responses

### Portfolio Features
- MDX-based content system for projects and blog posts
- About / CV page
- Responsive design optimized for all screen sizes
- Clean, timeless design without heavy animations
- Automatic open-graph and metadata generation
- Conditional section rendering based on content configuration

## Tech Stack

### Frontend
- **Next.js 16** - React framework
- **Once UI** - Component library
- **MDX** - Markdown + JSX for content
- **React 19** - UI library

### Backend
- **FastAPI** - Python web framework
- **ChromaDB** - Vector database for RAG
- **LangChain** - LLM orchestration
- **Anthropic Claude** - AI model
- **SentenceTransformers** - Local embeddings

## Getting Started

### Prerequisites
- Node.js v18.17+
- Python 3.12+
- pip (Python package manager)

### Frontend Setup

**1. Install dependencies**
```bash
npm install
```

**2. Run development server**
```bash
npm run dev
```

**3. Build for production**
```bash
npm run build
```

### Backend Setup (AI Assistant)

**1. Navigate to backend directory**
```bash
cd backend
```

**2. Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the backend directory:

```env
# Anthropic Claude Configuration
ANTHROPIC_API_KEY=your-api-key-here
ANTHROPIC_BASE_URL=https://api.anthropic.com
LLM_MODEL=claude-3-5-sonnet-20241022

# Database & Storage
DATABASE_PATH=./chroma_db
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000"]

# Embedding Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

**5. Start the backend server**
```bash
uvicorn main:app --reload --port 8000
```

**6. Ingest documents**

Place your PDF files in the `backend/documents/` directory, then:

```bash
# Via API
curl -X POST http://localhost:8000/api/ingest-directory

# Or via the provided test script
python test_api.py
```

### Content Management

**Edit config:**
```
src/resources/once-ui.config.js
```

**Edit content:**
```
src/resources/content.js
```

**Create blog posts / projects:**
```
Add a new .mdx file to src/app/blog/posts or src/app/work/projects
```

## Project Structure

```
Openfolio/
├── src/                    # Next.js frontend
│   ├── app/               # Pages and API routes
│   └── resources/         # Configuration and content
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes (chat, ingest, health)
│   │   ├── core/         # Configuration
│   │   ├── models/       # Data models
│   │   ├── services/     # RAG service
│   │   └── utils/        # Utilities
│   ├── chroma_db/        # Vector database storage
│   ├── documents/        # PDF documents for ingestion
│   └── main.py           # FastAPI app entry point
└── public/               # Static assets
```

## API Endpoints

### Health Check
```
GET /api/health
```
Returns system status including vector store statistics.

### Chat
```
POST /api/chat
```
Send queries to the AI assistant.

**Request:**
```json
{
  "message": "What are Tangzihan's skills?",
  "session_id": "user-session-123"
}
```

**Response:**
```json
{
  "answer": "Tangzihan has experience in...",
  "sources": [...],
  "document_count": 42,
  "mode": "rag"
}
```

### Document Ingestion
```
POST /api/ingest
Content-Type: multipart/form-data
```
Upload and ingest a single PDF file.

```
POST /api/ingest-directory
```
Ingest all PDFs from the configured documents directory.

## Features in Detail

### Once UI Components
- All tokens, components & features of [Once UI](https://once-ui.com)
- Endless customization through data attributes
- Responsive layout for all screen sizes

### SEO
- Automatic open-graph and X (Twitter) image generation with next/og
- Automatic schema and metadata generation

### Content Management
- Render sections conditionally based on content file
- Enable/disable pages for blog, work, gallery and about/CV
- Generate and display social links automatically
- Password protection support for URLs

### RAG Pipeline
- PDF document loading and chunking
- Semantic vector search with ChromaDB
- Context-aware responses using Claude
- Local embeddings (no API costs)

## Deployment

### Frontend (Vercel/Netlify)
The Next.js frontend can be deployed to Vercel, Netlify, or any Node.js hosting platform.

### Backend Options
1. **Vercel Serverless Functions** - Deploy FastAPI as serverless
2. **Render/Railway** - Deploy as a containerized service
3. **AWS/GCP/Azure** - Deploy to any cloud platform
4. **Self-hosted** - Run on your own server

### Production Considerations
- Use environment variables for sensitive data (API keys, database URLs)
- Consider migrating ChromaDB to Supabase/pgvector for cloud deployments
- Set up proper CORS origins for production domains
- Use a production-grade WSGI server like Gunicorn

## Acknowledgments

- Frontend built with [Once UI](https://once-ui.com) for [Next.js](https://nextjs.org)
- Original template: [Magic Portfolio](https://github.com/once-ui-system/magic-portfolio) by [Lorant One](https://www.threads.net/@lorant.one)
- AI backend powered by [Anthropic Claude](https://www.anthropic.com/claude)
- Vector search with [ChromaDB](https://www.trychroma.com/)

## License

Distributed under the CC BY-NC 4.0 License.
- Attribution is required.
- Commercial usage is not allowed.
- You can extend the license by purchasing a [Once UI Pro](https://once-ui.com/pricing) license.

See `LICENSE.txt` for more information.