### RBAC RAG Chatbot - Backend

A department-based document Question & Answer Chatbot built using Python,Fastapi,JWT Authenication, and RAG.


The Backend provides authenication, role-based access control,department-based filtering,user management, and rag question answering for the frontened application.


## Project Overview

This project is a Role-Based Access Control (RBAC) backend where document access is based on the user's department.

for example:

```text

Engineering User
       ↓
Engineering Department
       ↓
Engineering Documents

```

The main responsibilities of the backend are:

- User authenication
- Jwt token generation
- User authorization
- Role-Based access control
- Department-based document filtering
- RAG question answering
- User management
- APi request validation


#### Features

  1. User Login
  2. JWT Authentication
  3. Password Verification
  4. Role-Based access control
  5. Document-based Authorization
  6. Admin User Management
  7. Add New Users
  8. Department assignment
  9. RAG Question and Answer
 10. Document retrieval
 11. Request Validation
 12. Error handling 
 13. Langfuse observability
 14. Docker support
 15. GitHub Actions CI/CD
 16. FASTAPI Swagger Documentation



 ####Technologies Used

      

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
 


##Workflow

Login API

POST /auth/login


```text

Client
  ↓
POST /auth/login
  ↓
FastAPI Router
  ↓
LoginRequest Validation
  ↓
services.user.login()
  ↓
Validate Email + Password
  ↓
User Found?
  ┌────────────────────┴────────────────────┐
  │                                         │
 NO                                        YES
  ↓                                         ↓
Return 401                             Generate JWT
  ↓                                         ↓
Invalid Credentials                  Return Token
                                            +
                                       User Information



```

##Backend Components

```text
backend/
│
├── routes/
│   └── auth.py
│       └── POST /auth/login
│
├── services/
│   └── user.py
│       └── login()
│
└── auth/
    └── jwt.py
        └── generate_jwt_token()


```

####2. Admin Add User API


POST /admin/add-user

```text
                    LOGIN
                      ↓
              POST /auth/login
                      ↓
            Validate Credentials
                      ↓
             Generate JWT Token
                      ↓
              Return JWT + User
                      ↓
              Admin Dashboard
                      ↓
             POST /admin/add-user
                      ↓
              Verify JWT Token
                      ↓
              Get Logged-in User
                      ↓
                Check Role
                      ↓
             role == "admin"?
                /          \
              NO            YES
              ↓              ↓
           403          Get Department
                             ↓
                    Check Permission
                             ↓
                    Create New User
                             ↓
                    Hash Password
                             ↓
                    Save Database
                             ↓
                    Success Response


```
Backend Components

```text
backend/
│
├── routes/
│   ├── auth.py
│   │   └── POST /auth/login
│   │
│   └── admin.py
│       └── POST /admin/add-user
│
├── services/
│   ├── user.py
│   │   ├── login()
│   │   └── add_user()
│   │
│   └── admin.py
│       └── create_admin()
│
├── auth/
│   ├── jwt.py
│   │   ├── generate_jwt_token()
│   │   └── verify_token()
│   │
│   └── hashing.py
│       ├── hashing_password()
│       └── verify_password()
│
└── database/
    └── db.py
        └── User


```

### 3 .Question API
POST /rag/query

```text
             Client
              ↓
     retrieve_answer(query, department)
              ↓

      Start Langfuse Trace         
                             
             query                        
           department     
               ↓
        Create Embedding
               ↓
        Query Embedding
               ↓

        Pinecone Search        
          top_k = 5                    
        department filter            
               ↓
        Semantic Results
               │
               │
               ├──────────────────────┐
               │                      │
               ↓                      ↓
        Pinecone Results         BM25 Search
               │                      │
               │                 top_k = 5
               │                      │
               │                 Department
               │                   Filter
               │                      │
               │                      ↓
               │               Keyword Results
               │                      │
               └──────────┬───────────┘
                          ↓
                   Combine Results
                          ↓
                  Remove Duplicates
                          ↓
                   Combined Documents
                          ↓
                       Re-ranker
                          ↓
                     Top 3 Documents
                          ↓
                    Build LLM Prompt
                          ↓
                   Context + Question
                          ↓
                    LLM Generation
                          ↓
                   Final Answer
                          +
                       Sources
                          ↓
                     Langfuse Trace


```

Backend Components

application/
│
├── rag/
│   │
│   ├── embedding.py
│   │     └── create_embeddings()
│   │
│   ├── pinecone_store.py
│   │     └── init_index()
│   │
│   ├── bm25_search.py
│   │     ├── bm25_index()
│   │     ├── bm25_search()
│   │     
│   │
│   ├── reranking.py
│   │     └── reranker_documents()
│   │
│   ├── llm.py
│   │     └── generate_answer()
│   │
│   └── langfuse_config.py
│         └── langfuse
│
└── services/
      └── rag.py
            └── retrieve_answer()





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

## API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI

http://localhost:8000/docs