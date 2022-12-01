from passlib.context import CryptContext
from jose import jwt

from datetime import datetime, timedelta

JWT_SECRET = "markus"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(user):
    try:
        claims = {
            "sub": user.username,
            "lastname": user.lastname,
            
            "email": user.email,
            "password": user.password,
            "tax": user.tax,
            "phone": user.phone,
            
            
            "Role": user.role,
            "Place": user.place,
            
            "active": user.is_active,
            "exp": datetime.utcnow() + timedelta(minutes=120),
        }
        return jwt.encode(claims=claims, key=JWT_SECRET, algorithm=ALGORITHM)
    except Exception as ex:
        print(str(ex))
        raise ex

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_token(token):
    try:
        payload = jwt.decode(token, key=JWT_SECRET)
        return payload
    except:
        raise Exception("Ошибка")