from pydantic_settings import BaseSettings
from pathlib import Path # Used to create directories if they don't exist

class Settings(BaseSettings): #Tells python these variables should come from env file
    DATABASE_URL: str
    UPLOAD_DIR: str = "./uploads"
    VECTOR_STORE_PATH: str = "./vector_store"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:1b"
    
    class Config: #Tells pydantic to look for these variables in the .env file
        env_file = ".env" 
        
settings = Settings()

Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)
Path(settings.VECTOR_STORE_PATH).mkdir(exist_ok=True)
    