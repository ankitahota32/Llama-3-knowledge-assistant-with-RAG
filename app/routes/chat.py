from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import httpx
import json
import uuid
from app.models.database import get_db, Message
from app.services.embedder import embed_query
from app.services.retriever import search_index
from app.config import settings

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    session_id: str = None
    
@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    session_id = request.session_id or str(uuid.uuid4())
    
    query_embedding = embed_query(request.question)
    
    relevant_chunks = search_index(query_embedding, k = 4)
    
    if not relevant_chunks:
        raise HTTPException(
            status_code=404,
            detail= "No documnets found. Please upload a document first"
        )
        
    history = db.query(Message).filter(
       Message.session_id == session_id
    ).order_by(Message.created_at.desc()).limit(6).all()
    history = list(reversed(history))
    
    history_text = ""
    if history:
        history_text = "\n".join(
            f"{m.role.upper()}: {m.content}" for m in history
            
        )
        
    context = "\n\n".join(relevant_chunks)
    
    prompt = f"""You are a helpful assistant that answers questions strictly based on the provided document context.
    If the answer is not in the context, say "I don't have enough information in the uploaded documents to answer that." Do not make up answers.
    
DOCUMENT CONTEXT: 
{context}
 
CONVERSATION HISTORY:
{history_text if history_text else "No previous conversation."}

USER_QUESTION: {request.question}

ANSWER:"""

    user_message = Message(
        session_id=session_id,
        role="user",
        content=request.question
    )
    db.add(user_message)
    db.commit()
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                }
            )
            result = response.json()
            answer = result.get("response", "No response from model.")
            
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            details="Cannot connect to Ollama. Make sure it is running with: ollama serve"
        )
        
    assistant_message = Message(
        session_id = session_id,
        role="assistant",
        content = answer
    )
    db.add(assistant_message)
    db.commit()
    
    return {
        "session_id": session_id,
        "question": request.question,
        "answer": answer,
        "chunks_used": len(relevant_chunks)
    }
    
@router.get("/history/{session_id}")
def get_history(session_id: str, db: Session = Depends(get_db)):
     messages = db.query(Message).filter(
         Message.session_id == session_id
     ).order_by(Message.created_at.asc()).all()
     
     if not messages:
            raise HTTPException(status_code=404, detail="No history found for this session.")
        
     return {
            "session_id": session_id,
            "messages": [
                {
                    "role": m.role,
                    "content": m.content,
                    "created_at": m.created_at
                }
                for m in messages
            ]
        }