from application.database.db import Session
from application.database.db import User
import bcrypt

from application.auth.hashing import hashing_password,verify_password


session= Session()



###add user 

def add_user(name, email, password,department):
    try:
      
       hashed_password = hashing_password(password)
       user = User(
           name=name,
           email=email,
           password=hashed_password,
           department=department
       )

       session.add(user)
       session.commit()

       print("user added successfully")

    except Exception as e:

        print(e)



###login
def login(email,password):
    try:
        user = session.query(User).filter(User.email == email).first()
        
        if not user:
            print("user doesnt exists")

        if user and verify_password(password,user.password):
            return user
    
    except Exception as e:
        print(e)