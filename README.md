# RAG Knowledge Assistant

A production-style AI backend that lets you upload documents and ask questions about them using Retrieval Augmented Generation (RAG).

## What it does
- Upload PDFs or text files via REST API
- Automatically extracts, chunks, and embeds document text
- Ask natural language questions — answers come only from your documents
- Maintains conversation history across sessions
- Built entirely with open-source tools, runs 100% locally

## Tech Stack
- **FastAPI** — REST API framework
- **Llama 3** (via Ollama) — local open-source LLM
- **FAISS** — vector similarity search
- **Sentence Transformers** — text embeddings (all-MiniLM-L6-v2)
- **PostgreSQL + SQLAlchemy** — chat history and document metadata
- **PyMuPDF** — PDF text extraction

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload` | Upload a PDF or TXT file |
| POST | `/api/chat` | Ask a question about uploaded docs |
| GET | `/api/history/{session_id}` | Get conversation history |

## Local Setup

**Prerequisites:** Python 3.10+, PostgreSQL, Ollama

```bash
# Clone the repo
git clone https://github.com/yourusername/rag-assistant
cd rag-assistant

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Pull the LLM
ollama pull llama3.2:1b
ollama serve

# Run the server
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for the interactive API documentation.
