# app/routes/chat.py
from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.services.llm_service import get_llm_response

router = APIRouter()

@router.post("/generate", response_model=ChatResponse)
async def generate_chat_response(request: ChatRequest):
    try:
        response = await get_llm_response(request.prompt)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))