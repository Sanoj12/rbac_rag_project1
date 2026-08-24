from fastapi import FastAPI
from routes import auth,rag,admin
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
    "https://rbac-rag.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router,prefix="/admin")
app.include_router(auth.router,prefix="/auth")
app.include_router(rag.router,prefix="/rag")

@app.get("/")
def home():
    return {"message": "RBAC RAG API running"}