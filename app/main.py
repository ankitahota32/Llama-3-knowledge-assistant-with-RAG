from fastapi import FastAPI
from app.routes import upload, chat 
from app.models.database import create_tables
''' upload → contains upload-related API endpoints
chat → contains chat-related API endpoints '''


# Creating the app object and setting metadata for API documentation
app = FastAPI(
    title="RAG Knowledge Assistant",
    description="A Retrieval-Augmented Generation (RAG) assistant for knowledge management.",
    version="1.0.0"
    )

@app.on_event("startup")
def startup():
    create_tables() # This function is called when the application starts up, it creates the necessary tables in the database if they don't already exist.
    print("Database tables created succesfully")

app.include_router(upload.router, prefix="/api", tags=["Upload"]) # Registering the upload router with the app, prefixing all routes with /api and tagging them as "Upload"
app.include_router(chat.router, prefix="/api", tags=["Chat"]) # Registering the chat router with the app, prefixing all routes with /api and tagging them as "Chat"

@app.get("/")
def root():
    return {"status": "running", "message": "RAG Knowledge Assistant is up and running!"}