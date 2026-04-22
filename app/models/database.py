from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime 
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import settings

engine= create_engine(settings.DATABASE_URL) # Connects to database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # This creates a session generator 

Base = declarative_base() # This is the base class for our models, it provides the necessary functionality to define tables and interact with the database.

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_name = Column(String, nullable=False)
    chunks_created = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.now)
    
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
def create_tables(): # Creates table in db if they don't exist
    Base.metadata.create_all(bind=engine)
    
def get_db(): # This is a dependency function that can be used in FastAPI routes to get a database session. It ensures that the session is properly closed after the request is processed.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
    
    