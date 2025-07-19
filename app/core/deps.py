from app.core.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

# SessionLocal() creates a new SQLAlchemy database session (a connection + unit of work).
# yield db provides the session to whatever function needs it (e.g., a route handler).
# After the request finishes, the finally block closes the session, releasing the DB connection.