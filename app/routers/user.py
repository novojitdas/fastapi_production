from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.core.deps import get_db
import hashlib

router = APIRouter(
    prefix="/users", # All routes prefixed with /users
    tags=["Users"] # Adds this group to your FastAPI Swagger UI docs
)

# Dummy user storage
users_db = []

@router.post("/", response_model=UserOut) # POST route at /users/.
def create_user(user: UserCreate, db: Session = Depends(get_db)): # Automatically validates the incoming JSON body using the UserCreate schema.
    db_user = db.query(User).filter(User.email == user.email).first()
    if (db_user):
        raise HTTPException(status_code=400,detail="Email already registered")
    
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashlib.sha256(user.password.encode()).hexdigest()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.schemas.user import UserCreate, UserOut
# from app.models.user import User
# from app.core.deps import get_db
# import hashlib

# router = APIRouter(
#     prefix="/users", # All routes prefixed with /users
#     tags=["Users"] # Adds this group to your FastAPI Swagger UI docs
# )

# # Dummy user storage
# users_db = []

# @router.post("/", response_model=UserOut) # POST route at /users/.
# def create_user(user: UserCreate): # Automatically validates the incoming JSON body using the UserCreate schema.
#     users_db.append(user) # Add user into dummy db
#     return user # Returns user object following UserOut Validation
