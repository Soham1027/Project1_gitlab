from datetime import timedelta,datetime, timezone
from typing import Annotated
import jwt
from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "9c435539b8c08a31ce1c93bf797abcb1c5c3993824be18568b7b5aba40456c04"   
JWT_REFESH_SECRET_KEY="439340ce06dca59e096161c2ca1f45f7d64ec962d6fd78dd082686cbc91c36b9"
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def create_jwt_token(data:dict,expire_delta:timedelta | None= None):
    
    to_encode = data.copy()
    if expire_delta:
        expire=datetime.now(timezone.utc)+expire_delta
    else:
        expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return(encoded_jwt)
    

def create_reset_token(email: str) -> str:
    to_encode = {"sub": email,"exp": datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)}
    
    return jwt.encode(to_encode, JWT_REFESH_SECRET_KEY, algorithm=ALGORITHM)


def create_reset_token_by_id(id: int) -> str:
    to_encode = {"sub": id, "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

def decode_email_token(token:str):
    payload = jwt.decode(token, JWT_REFESH_SECRET_KEY, algorithms=ALGORITHM)  # type: ignore
    for i in payload:
        if i=="sub":
            print("payload",payload[i])
            return payload[i]
        else:
            return None
        