from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

from .config import AI_API_KEY, AI_BASE_URL, AI_MODEL

app = FastAPI(title="MI-IA", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


@app.get("/api/health")
async def health():
    return {"status": "ok", "model_configured": bool(AI_API_KEY and AI_MODEL)}


@app.post("/api/chat")
async def chat(request: ChatRequest):
    if not AI_API_KEY or not AI_MODEL:
        raise HTTPException(
            status_code=503,
            detail="AI provider is not configured. Set AI_API_KEY and AI_MODEL in .env.",
        )

    messages = [
        {
            "role": "system",
            "content": "You are MI-IA, a helpful, honest and concise personal AI assistant.",
        },
        *request.history,
        {"role": "user", "content": request.message},
    ]

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": AI_MODEL,
        "messages": messages,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{AI_BASE_URL.rstrip('/')}/chat/completions",
            headers=headers,
            json=payload,
        )

    if response.is_error:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text,
        )

    data = response.json()
    answer = data["choices"][0]["message"]["content"]

    return {"response": answer}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
