from fastapi import APIRouter
from pydantic import BaseModel

from application.services.user import add_user as create_user
 

router =APIRouter()

class CreateUser(BaseModel):
    name:str
    email:str
    password:str
    department:str

@router.post("/add-user")
def add_user(data:CreateUser):
    try:

        return create_user(
            name=data.name,
            email=data.email,
            password=data.password,
            department = data.department
        )
       
    

    except Exception as e:
        print(e)