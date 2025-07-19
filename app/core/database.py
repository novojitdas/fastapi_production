from sqlalchemy import create_engine #create the database engine (i.e., connection to the DB).
from sqlalchemy.orm import sessionmaker, declarative_base #Creates a session factory to interact with the DB, Base class for model classes.
import os 
from dotenv import load_dotenv

load_dotenv() #read .env file and load the variables into os

DATABASE_URL = os.getenv("DATABASE_URL")  #Gets the DATABASE_URL from the .env file.

engine = create_engine(DATABASE_URL,echo=True) # Connects to your PostgreSQL database. echo=True logs all the SQL generated — useful for debugging.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# SessionLocal() will be used to interact with the DB in each request.
# autocommit=False: You control when data is committed.
# autoflush=False: No automatic flushing — gives you more contro

Base = declarative_base()
#Used as the base class for all your SQLAlchemy ORM models:
