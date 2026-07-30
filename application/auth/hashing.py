##hashing password -using bcrypt
import bcrypt

##string - bytes
def hashing_password(password:str):
    return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode()


##bytes -string
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())