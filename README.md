
Title:   RBAC RAG Chatbot

##A secure Role-Baesd Access Control(RBAC) Chatbot built using  Retrieval-Augmented Generation (RAG).The system autenticates users enforces role-based permissions,retreive authorized documents,and generate context-aware response using LLMs.

Overview

This project combines RAG + RBAC to create a secure AI-powered question-answering system

The application:
 
 1.Authenticates the user with JWT
 2.identifies the users department
 3.Load documents and Converts documents into smaller chunks.
 4.Generates embedding for document chunks
 5.Stores embeddings in pinecone
 6.Retrieves relevant documents using semantic search.
 7.Performs keyword search using BM25.
 8.Combines semantic search + keyword search and reranking retrieved documents.
 9.Sends relevant context to the LLM.
 10.Generates an answer based only on the retrieved documents.

## 🔐 User Authentication Flow

```text
User Login
    │
    ▼
Verify Email & Password (Bcrypt)
    │
    ▼
Generate JWT Token
    │
    ▼
Return Token to User
    │
    ▼
User Sends JWT with API Requests
    │
    ▼
Server Verifies JWT token
    │
    ▼
Access Granted / Access Denied
```

## 🏢 RBAC Workflow

User Login(Email & Password)
    ↓
JWT Authentication
    ↓
Identify User & Department
    ↓
Department-Based Access
    ↓
├── Finance → Finance Documents
├── HR → HR Documents
├── Marketing → Marketing Documents
├── Engineering → Engineering Documents
└── General → General Documents
    ↓
User Query
    ↓
Query Embedding
    ↓
Pinecone Vector Database Semantic Search(department filtering)
    ↓
BM25 Keyword Search
    ↓
Combine semantic search + keyword search
    ↓
Re-Ranking
    ↓
Remove Duplicates
    ↓
Top Relevant Documents
    ↓
send Relevant Context
    ↓
Groq LLM
    ↓
Generate Response
    ↓
Display Response to User(Streamlit)
                    

Features
  1. JWT authentication
  2. Role-Based Access Control
  3. Department-based document filtering
  4. PDF and Markdown document processing
  5. Document chunking
  6. Text embeddings
  7. Semantic search
  8. BM25 keyword search
  9.Document reranking
 10.LLM-based answer generation
 11.Retrieval-Augmented Generation
 12.Langfuse observability
 13.Docker support
 14.GitHub Actions CI/CD


 Techologies Used       

| Category                 | Technology                        |
| ------------------------ | --------------------------------- |
| **Programming Language** | Python                            |
| **Backend**              | FastAPI                           |
| **Frontend**             | Streamlit                         |
| **Authentication**       | JWT                               |
| **Password Hashing**     | Bcrypt                            |
| **Database**             | SQLite                            |
| **ORM**                  | SQLAlchemy                        |
| **Vector Database**      | Pinecone                          |
| **Embeddings**           | Sentence Transformers             |
| **Semantic Search**      | Pinecone Vector Search            |
| **Keyword Search**       | BM25                              |
| **Hybrid Retrieval**     | Pinecone + BM25                   |
| **Re-Ranking**           | Cross-Encoder                     |
| **LLM**                  | Groq                              |
| **Document Processing**  | Docling                           |
| **Text Chunking**        | RecursiveCharacterTextSplitter    |
| **Observability**        | Langfuse                          |
| **Containerization**     | Docker                            |
| **Version Control**      | Git / GitHub                      |




Installation

1. Clone the repository
git clone https://github.com/Sanoj12/rbac-rag-chatbot1.git

cd rbac-rag-chatbot1

2. Create virtual environment
uv venv

3. Activate environment

Windows:
.venv\Scripts\activate

4. Install dependencies
uv pip install -r requirements.txt


Environment Variables

Create a .env file:

PINECONE_API_KEY=
GROQ_API_KEY=
JWT_SECRET_KEY
LANGFUSE_SECRET_KEY=y
LANGFUSE_PUBLIC_KEY=
LANGFUSE_HOST=

Never upload .env or API keys to GitHub.

Add this to .gitignore:

.env
.venv/
__pycache__/
*.pyc



##  Run Application

- Start FastAPI Server

```bash
uvicorn application.main:app --reload
```

-Start Streamlit UI
streamlit run app.py
```bash
streamlit run app.py
```
