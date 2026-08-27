### RBAC RAG Chatbot

A full-stack, department-based Question & Answer chatbot built using Next.js, React, TypeScript, FastAPI, Python, JWT Authentication, and RAG.

The project uses Role-Based Access Control (RBAC) and department-based document filtering to ensure users can only access documents authorized for their department.


## Application Workflow

```text
                         RBAC RAG CHATBOT
                                │
                ┌───────────────┴───────────────┐
                │                               │
                ▼                               ▼
           FRONTEND                         BACKEND
        Next.js / React                  FastAPI / Python
                │                               │
                │          REST API             │
                └───────────────►◄──────────────┘
                                                │
                                                ▼
                                      JWT Authentication
                                                │
                                                ▼
                                      RBAC Authorization
                                                │
                                                ▼
                                      Department Filtering
                                                │
                                                ▼
                                           RAG Pipeline
                                                │
                            ┌───────────────────┴──────────────────┐
                            │                                      │
                            ▼                                      ▼
                       Pinecone                                  BM25
                    Semantic Search                         Keyword Search
                            │                                      │
                            └───────────────────┬──────────────────┘
                                                ▼
                                           Re-Ranking
                                                │
                                                ▼
                                           LLM / Groq
                                                │
                                                ▼
                                           Final Answer
                                                │
                                                ▼
                                            Frontend



```

### Frontend

The frontend is built with Next.js, React, and TypeScript.

For frontend setup, authentication flow, chat page, admin page, API integration, and frontend architecture

see:

Backend
The backend is built with Python and FastAPI.

For backend setup, JWT authentication, RBAC, department authorization, RAG pipeline, Pinecone, BM25, re-ranking, Langfuse, and API documentation, see:

👉 Backend README

🚀 Quick Start
1. Clone Repository
git clone https://github.com/Sanoj12/rbac-rag-chatbot1.git

cd rbac-rag-chatbot1

2. Start Application
Follow the instructions in the:

application/readme.md

3. Start Frontend
Follow the instructions in the:

frontend/README.md

Once both applications are running:

Frontend → http://localhost:3000
Application  → http://localhost:8000
Swagger  → http://localhost:8000/docs

🔐 Department-Based Access
Documents are filtered based on the authenticated user's department.

Engineering User
       ↓
Engineering Department
       ↓
Engineering Documents

Finance User
       ↓
Finance Department
       ↓
Finance Documents

This ensures that users retrieve information only from documents they are authorized to access.

👤 Author
Sanoj C SAM

Learning and portfolio project.

⭐ Project
If you find this project useful or interesting, consider giving the repository a ⭐.

