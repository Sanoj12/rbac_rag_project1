Installation
1. Install uv
curl -Ls https://astral.sh/uv/install.sh | sh

or

pip install uv
2. Clone the repository
git clone https://github.com/your-username/project-name.git
cd project-name
3. Create virtual environment
uv venv

Activate it:

Linux / Mac

source .venv/bin/activate

Windows

.venv\Scripts\activate
4. Install dependencies

Using requirements file:

uv pip install -r requirements.txt


<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 6bb0447 (Update README.md)
Title:Role Based Access Control System(RBAC) RAG Chatbot

##A secure Role-Baesd Access Control(RBAC) Chatbot built using  Retrieval-Augmented Generation (RAG).The system autenticates users enforces role-based permissions,retreive authorized documents,and generate context-aware response using LLMs.


Features

-JWT Autentication
-Bcrypt Password Hashing
-SQLAlchemy ORM
-RBAC
-RAG
-Vector Search with Pinecone
-Docling for PDF and text parsing
-langchain
-REST APIs using FastAPI
-Dockerized Deployment
-CI/CD with GitHub Actions



## tech stack

1.Backend:
-Python
-FastAPI

2.AI/ML:
-Langchain
-Document Parsing-> Docling
-VectorDB -> Pinecone
-Embeddings -> Sentence Transformer
-LLM -> Ollama(llama)

3.Database
-Sqlite
-SQLAlchemy



4.DevOps

-Docker
-CI/CD Tool -> Github Actions


## User Authenication flow


User Login  ->   Verify Password using Bcrypt ->  Generate JWT Token ->   Return Token to user -> User sends JWT in api requestss -> server verifies jwt  -> Access granted/Access denied




### RBAC WORKFLOW



<<<<<<< HEAD
=======

# ** Role-Based Access Control (RBAC) RAG Chatbot**

A secure **Role-Based Access Control (RBAC)** chatbot built using **Retrieval-Augmented Generation (RAG)**. The system authenticates users, enforces role-based permissions, retrieves authorized documents, and generates context-aware responses using Large Language Models (LLMs).

## Features

* JWT Authentication
* Bcrypt Password Hashing
* SQLAlchemy ORM
* Role-Based Access Control (RBAC)
* Retrieval-Augmented Generation (RAG)
* Vector Search with Pinecone
* Docling for PDF and Text Parsing
* LangChain Integration
* REST APIs using FastAPI
* Dockerized Deployment
* CI/CD with GitHub Actions

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI

### AI/ML

* LangChain
* Document Parsing → Docling
* Vector Database → Pinecone
* Embeddings → Sentence Transformers
* LLM → Ollama (Llama)

### Database

* SQLite
* SQLAlchemy

### DevOps

* Docker
* GitHub Actions (CI/CD)

## 🔐 User Authentication Flow

```text
User Login
    │
    ▼
Verify Password (Bcrypt)
    │
    ▼
Generate JWT Token
    │
    ▼
Return Token to User
    │
    ▼
User Sends JWT in API Requests
    │
    ▼
Server Verifies JWT
    │
    ▼
Access Granted / Access Denied
```

## 🏢 RBAC Workflow

```text
>>>>>>> 73d8aaa533aa71306766d4623e25011a291b7dc9
=======
>>>>>>> 6bb0447 (Update README.md)
                    User Login
                         │
                         ▼
                JWT Authentication
                         │
                         ▼
<<<<<<< HEAD
<<<<<<< HEAD
                Extract User based on department
=======
          Extract User Department
>>>>>>> 73d8aaa533aa71306766d4623e25011a291b7dc9
=======
                Extract User based on department
>>>>>>> 6bb0447 (Update README.md)
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    Finance          Engineering         HR
        │                │                │
        ▼                ▼                ▼
Financial Docs    Technical Docs    Employee Docs

                         │
                         ▼
                     Marketing
                         │
                         ▼
                 Marketing Docs

                         │
                         ▼
              Query Pinecone Vector DB
                         │
                         ▼
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 6bb0447 (Update README.md)
              Filter Documents by department
                         │
                         ▼
              Send Context to LLM(Ollama)
                         │
                         ▼
                 Generate Response



## key

- Implemented secure JWT-based authentication and authorization.
<<<<<<< HEAD
=======
           Filter Documents by Department
                         │
                         ▼
             Send Context to LLM (Ollama)
                         │
                         ▼
                 Generate Response
```

## Key 

-Implemented secure JWT-based authentication and authorization.
>>>>>>> 73d8aaa533aa71306766d4623e25011a291b7dc9
=======
>>>>>>> 6bb0447 (Update README.md)
- Designed department-level document access using RBAC.
- Built a Retrieval-Augmented Generation (RAG) pipeline using LangChain and Pinecone.
- Integrated Docling for PDF document parsing and ingestion.
- Developed RESTful APIs using FastAPI and SQLAlchemy.
- Containerized the application using Docker.
- Automated build and deployment pipelines using GitHub Actions.

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 6bb0447 (Update README.md)



## run application


uvicorn application.main:app --reload 



streamlit run app.py
<<<<<<< HEAD
=======
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
>>>>>>> 73d8aaa533aa71306766d4623e25011a291b7dc9
=======
>>>>>>> 6bb0447 (Update README.md)
