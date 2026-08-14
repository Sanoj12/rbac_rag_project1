from fastapi import FastAPI
from application.routes import auth,rag,admin

app = FastAPI()

app.include_router(admin.router,prefix="/admin")
app.include_router(auth.router,prefix="/auth")
app.include_router(rag.router,prefix="/rag")

@app.get("/")
def home():
    return {"message": "RBAC RAG API running"}