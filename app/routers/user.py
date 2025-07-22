from fastapi import APIRouter, Depends, HTTPException
from fastapi import Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut, UserLogin
from app.models.user import User
from app.core.deps import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.core.auth import get_current_user
import hashlib

router = APIRouter(
    prefix="/users", # All routes prefixed with /users
    tags=["Users"] # Adds this group to your FastAPI Swagger UI docs
)

# 1. /register POST
# 2. /login POST
# 3. /me GET for auth check


# 2. /register POST
@router.post("/register", response_model=UserOut, summary="Register a new user")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = hash_password(user.password)
    db_user = User(username=user.username,email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 3. /login POST
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

#this is for swagger testing
@router.post("/token", summary="OAuth2 login for Swagger UI")
def login_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


# 3. /me GET AUTH check

@router.get("/me", response_model=UserOut, summary="get current logged in user",tags=["Users"])
def get_me(current_user: User = Depends(get_current_user)):
    return current_user