from pydantic import BaseModel, EmailStr #Pydantic models - used  for request validation and response shaping.
from enum import Enum
# BaseModel -> coreClass of pydantic used for define data models with type validation.
# EmailStr -> special type validates email format.

class Role(str,Enum):
    admin = "admin"
    manager = "manager"
    customer = "customer"

class UserCreate(BaseModel): # Public registration
    username: str
    email: EmailStr
    password: str

class UserCreateByAdmin(UserCreate):  # Admin creates any user
    role: Role

class UserOut(BaseModel):
    username: str
    email: EmailStr
    role: Role 

    class Config:
         from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str 
    token_type: str = "bearer"