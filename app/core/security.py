from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#SECRET_KEY in .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256" #HMAC with SHA-256.
ACCESS_TOKEN_EXPIRE_MINUTES = 60 #60mins expire time


#It uses bcrypt, a secure hashing algorithm.
#deprecated="auto" means old schemes are automatically marked as deprecated if no longer safe.
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
