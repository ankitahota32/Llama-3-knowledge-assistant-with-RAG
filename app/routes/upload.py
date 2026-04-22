from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import shutil
import uuid
import os
from app.config import settings
from app.services.extractor import extract_text
from app.services.chunker import chunk_text
from app.services.embedder import embed_chunks
from app.services.retriever import save_to_index
from app.models.database import get_db, Document

router = APIRouter() # Creates a modular route group

ALLOWED_EXTENSIONS = {".pdf", ".txt"}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    ext = os.path.splitext(file.filename)[1].lower() # Extracts extension
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: '{ext}'. Only PDF and TXT allowed."
        )
        
    unique_name = f"{uuid.uuid4()}{ext}" #Generates unique filename and prevents overwriting
    save_path = os.path.join(settings.UPLOAD_DIR, unique_name) #Uses configurable upload directory
        
    with open(save_path, "wb") as buffer: # Save file to disk
       shutil.copyfileobj(file.file, buffer)
       
    try: 
        text = extract_text(save_path)
    except Exception as e: 
        raise HTTPException(status_code= 500, detail=f"Text extraction failed: {str(e)}")
    
    if not text: 
        raise HTTPException(status_code= 400, detail="No text could be extracted from this file")
    
    chunks = chunk_text(text)
    if not chunks:
        raise HTTPException(status_code= 400, detail="Document was too short to process")
    
    embeddings = embed_chunks(chunks)
    
    save_to_index(chunks, embeddings)
    
    doc = Document(
        filename=unique_name,
        original_name= file.filename,
        chunks_created = len(chunks)
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    return JSONResponse(content={
        "message": "File uploaded and processed successfully",
        "filename": file.filename,
        "chunks_created": len(chunks),
        "document_id": doc.id
    })
        