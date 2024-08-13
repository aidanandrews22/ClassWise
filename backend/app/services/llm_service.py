# app/services/llm_service.py
import httpx
from app.config import settings

async def getOpenAIResponse():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.LLM_API_URL,
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}]
            },
            headers={"Authorization": f"Bearer {settings.LLM_API_KEY}"}
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

async def get_llm_response(prompt: str) -> str:
    useOpenAI = False
    if useOpenAI:
        response = getOpenAIResponse()
    else:
        # Handle local llm
        print()

    return response