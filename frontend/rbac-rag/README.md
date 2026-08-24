### RBAC RAG Chatbot -Frontend

A department-based document Question & Answer chatbot frontend built using Next.js and React.

The application allows users to log in,ask questions from authorized documents,and receive answers from the rag backend.

Admins can also add new users and assign them to departments.



## Project Overview

This project is a role-based on their department

For example:
 - Engineering users can access Engineering documents.
 - Finance users can access Finance documents.


frontend communicate with a Fastapi backend through REST apis.


## Features

-User Login
-JWT Authentication
-Protected Chat page
-User Information Display
-Admin Page
-Add new Users
-Department assignment
-RAG Question & Answer
-Chat History
-Loading State
-Error Handling
-Logout



###Techologies Used

- Next.js
- Typescript
- React

### Authenication

- JWT
- LocalStorage


###Pages

Login Page

app/login/page.tsx

The frontend sends the login request to the fastapi backend

1.Login workflow

User
 ↓
Login Page
 ↓
Enter Email + Password
 ↓
Click Login
 ↓
handleLogin()
 ↓
Validate Input
 ↓
POST /auth/login
 ↓
FastAPI
 ↓
Check Email + Password
 ↓
Valid?
 ├── NO
 │    ↓
 │  Return Error
 │    ↓
 │  Display Error
 │
 └── YES
      ↓
   Generate JWT
      ↓
   Return JWT + User Information
      ↓
   Store access_token(localStorage)
      ↓
   Store user information
      ↓
   Redirect
      ↓
   Chat / Admin Page


2.Chat Page

app/chat/page.tsx

The chat page allows authenticated users to ask questions.

Chat workflow

User
 ↓
Login
 ↓
JWT Token
 ↓
Chat Page
 ↓
Enter Question
 ↓
Click Send
 ↓
sendQuestion()
 ↓
Check Question
 ↓
Is Question Empty?
 ├── YES
 │    ↓
 │  Display Error
 │    ↓
 │  Stop
 │
 └── NO
      
      ↓
   Get JWT from localStorage
      ↓
   Does JWT Exist?
   ├── NO
   │    ↓
   │  Redirect to Login
   │
   └── YES
        ↓
      fetch()
        ↓
   POST /rag/query
        ↓
   Send JWT + Question
        ↓
      FastAPI
        ↓
    Verify JWT
        ↓
   Identify User
        ↓
   Get Department
        ↓
   Apply Department Filter
        ↓
   Retrieve Relevant Documents
        ↓
        RAG
        ↓
   Generate Answer
        ↓
   Return JSON Response
        ↓
   response.json()
        ↓
   Save Question + Answer
        ↓
   Chat History
        ↓
   Clear Question
  
        ↓
   Display Answer


3.Admin Page

to add new users and assign them to departments.

Admin
 ↓
Login Page
 ↓
Enter Email + Password
 ↓
Click Login
 ↓
POST /auth/login
 ↓
FastAPI
 ↓
Verify Admin
 ↓
Generate JWT
 ↓
Return Token
 ↓
Store Token
 ↓
Redirect to Admin Page
 ↓
Admin Page
 ↓
Enter User Details
 ↓
Name + Email + Password + Department
 ↓
Click Add User
 ↓
POST /admin/add-user
 ↓
Send JWT + User Details
 ↓
FastAPI
 ↓
Verify JWT
 ↓
Check Admin Permission
 ↓
Create User
 ↓
Save User in Database
 ↓
Return Response
 ↓
Display Success Message



API Endpointes:

1. POST  ->   /auth/login  -> login user

2. POST  -> /admin/add-user  -> Add new user

3. POST ->  /rag/query  -> ask rag question





## Installation

1. Clone Repository
git clone https://github.com/Sanoj12/rbac_rag_project1

2. Open Frontend
cd frontend/rbac-rag

3. Install Dependencies
npm install

4. Create .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000

5. Start Next.js
npm run dev

The frontend will normally run at:

http://localhost:3000


##Backend Requirement

The FastAPI backend must be running.

Example:

uvicorn main:app --reload

Backend:

http://localhost:8000

FastAPI Swagger UI:

http://localhost:8000/docs



##Learning

  -Nextjs App Router
  -React Components
  -JSX
  -Hooks(useState & useEffect)
  -LocalStorage
  -fetchAPI
  -form handling
  -Connecting Next.js with FastAPI


Author
Sanoj C SAM
Completed as a learning and portfolio project.