

###### RBAC RAG Chatbot — Frontend

A department-based document Question & Answer chatbot frontend built using Next.js, React, and TypeScript.

The application allows users to log in, ask questions from authorized documents, and receive answers from the RAG backend.

Admins can also add new users and assign them to departments.

📌 Project Overview

This project is a Role-Based Access Control (RBAC) application where document access is based on the user's department.

For example:

Engineering users can access Engineering documents.
Finance users can access Finance documents.

The frontend communicates with a FastAPI backend through REST APIs.

✨ Features
User Login
JWT Authentication
Protected Chat Page
User Information Display
Admin Page
Add New Users
Department Assignment
RAG Question & Answer
Chat History
Loading State
Error Handling
Logout


🛠️ Technologies Used
Frontend
Next.js
TypeScript
React
JSX
React Hooks
App Router
Authentication
JWT Authentication
LocalStorage
Backend Communication
REST APIs
Fetch API
FastAPI


File:

app/login/page.tsx


The login page allows users to authenticate using their email and password.

Login Workflow

```text
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
 ┌───────────────┴───────────────┐
 │                               │
NO                              YES
 ↓                               ↓
Return Error                 Generate JWT
 ↓                               ↓
Display Error             Return JWT + User Info
                                 ↓
                         Store access_token
                           in localStorage
                                 ↓
                         Store User Information
                                 ↓
                              Redirect
                                 ↓
                         Chat / Admin Page
```

💬 Chat Page

File:

app/chat/page.tsx


The chat page allows authenticated users to ask questions from documents they are authorized to access.


Chat Workflow

```text
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
 ┌───────┴───────┐
 │               │
YES              NO
 ↓               ↓
Display Error    Get JWT from
Stop             localStorage
                 ↓
           Does JWT Exist?
         ┌───────┴───────┐
         │               │
        NO              YES
         ↓               ↓
   Redirect Login      fetch()
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
                 Display Answer
```

👨‍💼 Admin Page

The Admin Page allows authorized administrators to add new users and assign them to departments.

Admin Workflow

```text
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
```

🔌 API Endpoints
Method	Endpoint	Description
POST	/auth/login	Login user
POST	/admin/add-user	Add a new user
POST	/rag/query	Ask a RAG question

🔐 Authentication

The application uses JWT authentication.

After a successful login, the FastAPI backend returns:

JWT access token
User information

The frontend stores the access token in:

localStorage


The JWT is then used when communicating with protected backend endpoints.


🏢 Department-Based Authorization

The application uses the user's department to control document access.

Example:

```text
Engineering User
       ↓
Engineering Department
       ↓
Engineering Documents
```

```text
Finance User
       ↓
Finance Department
       ↓
Finance Documents
```


⚙️ Installation

1. Clone Repository
git clone https://github.com/Sanoj12/rbac_rag_project1

2. Open Frontend
cd frontend/rbac-rag

3. Install Dependencies
npm install

4. Create Environment File

Create a .env.local file in the frontend project:

NEXT_PUBLIC_API_URL=http://localhost:8000

5. Start Next.js
npm run dev


The frontend will normally run at:

http://localhost:3000


Start the backend using:

uvicorn main:app --reload
The backend will normally run at:

http://localhost:8000


FastAPI Swagger UI:

http://localhost:8000/docs

🎯 Learning

This project helped me learn and practice:

Next.js App Router
React Components
JSX
TypeScript
React Hooks
useState
useEffect
LocalStorage
Fetch API
Form Handling
JWT Authentication
REST API Integration
Connecting Next.js with FastAPI

🚀 Future Improvements

Possible future improvements include:

Better UI/UX
Document upload functionality
Admin document management
User management dashboard

👤 Author

Sanoj C SAM

Completed as a learning and portfolio project.

⭐ Project

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.