from sqlalchemy import Column, Integer, String,Enum
from app.core.database import Base
import enum

class Role(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    customer = "customer"

class User(Base): 
    __tablename__ = "users" #Creates a User model mapped to the "users" table in the database.

    id = Column(Integer, primary_key=True, index=True) #Tells the database to create an index on this column. Improves search performance for queries using this field.
    username = Column(String, unique=True, nullable=False) #nullable false means value required in this columnn
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String,nullable=False)
    role = Column(Enum(Role), default=Role.customer)
    refresh_token = Column(String, nullable=True)