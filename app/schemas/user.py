from pydantic import BaseModel, EmailStr #Pydantic models - used  for request validation and response shaping.
# BaseModel -> coreClass of pydantic used for define data models with type validation.
# EmailStr -> special type validates email format.

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    username: str
    email: EmailStr