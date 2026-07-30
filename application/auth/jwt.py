import jwt
import datetime

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("JWT_SECRET_KEY")



#GENERATE JWT TOKEN

def generate_jwt_token(user_id,department):
    payload = {
        "user_id": user_id,
        "department": department,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }

    token = jwt.encode(payload,api_key,algorithm="HS256")
    print(token)
    return token


###vertifi jwt token
def verify_token(token):
    try:
        data = jwt.decode(token, api_key, algorithms="HS256")
        print(data)
        return data
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"