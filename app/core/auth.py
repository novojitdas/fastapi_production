from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.user import User
from app.core.deps import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

def credentials_exception (message: str = "Invalid Token"):
    raise HTTPException(status_code=401, detail=message)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            credentials_exception()
    except JWTError:
         credentials_exception("Could not validate token")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        credentials_exception("User not found")
    return user

def require_role(*roles):
    def role_dependency(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403,detail="Access Denied")
        return current_user
    return role_dependency