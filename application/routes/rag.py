from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import Depends

from application.rag.retriever import retrieve_answer
from application.auth.jwt import verify_token

from fastapi.security import HTTPBearer

security = HTTPBearer() ##authorization header in jwt token

router = APIRouter()

class QueryRequest(BaseModel):
    query: str


def get_user(token: str):
    try:
        return verify_token(token)
    
    except Exception as e:

        print(e)


@router.post("/query")
def ask_questions(data: QueryRequest, credentials=Depends(security)):
    try:
        token = credentials.credentials
        user = get_user(token)

        answer = retrieve_answer(
            query=data.query,
            department=user["department"]
        )

        return {
            "answer": answer,
            "department": user["department"]
        }

    except Exception as e:
        print("ERROR:", repr(e))
        return {"error": str(e)}
    

    