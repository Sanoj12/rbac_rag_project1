from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from application.services.user import login

from application.auth.jwt import generate_jwt_token

router =APIRouter()

#pydantic 
class LoginRequest(BaseModel):
    email:str
    password:str



@router.post("/login")
def login_user(data:LoginRequest):

    try:

        user = login(data.email,data.password)
        print(user)
        print(user.department)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="invaild email or password"
            )

        token = generate_jwt_token(
            user.id,
            user.department
        )


        return{
            "token":token,
            "department":user.department
        }

    except Exception as e:
        print("ERROR:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )  
