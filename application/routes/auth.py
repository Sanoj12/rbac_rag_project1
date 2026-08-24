from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from services.user import login

from auth.jwt import generate_jwt_token

router =APIRouter()

#pydantic 
class LoginRequest(BaseModel):
    email:str
    password:str


@router.post("/login")
def login_user(data: LoginRequest):

    try:

        # Call login function
        user = login(
            data.email,
            data.password
        )

        # User not found / wrong password
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        print("USER:", user)
        print("DEPARTMENT:", user.department)

        # Generate JWT
        token = generate_jwt_token(
            user.id,
            user.department
        )

        return {
            "access_token": token,
            "user": {
                "id": user.id,
                "email": user.email,
                "department": user.department
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        print("LOGIN API ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )