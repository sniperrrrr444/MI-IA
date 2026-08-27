from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import httpx

from .config import AI_BASE_URL, AI_MODEL, HOST, PORT

app = FastAPI(title="MI-IA Local", version="0.2.0")

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
    try:
        async with httpx.AsyncClient(timeout=2) as client:
            response = await client.get(f"{AI_BASE_URL.rstrip('/')}/models")
            response.raise_for_status()
        return {"status": "ok", "local_engine": True, "model": AI_MODEL, "engine_url": AI_BASE_URL}
    except Exception:
        return {"status": "degraded", "local_engine": False, "model": AI_MODEL, "engine_url": AI_BASE_URL}


@app.post("/api/chat")
async def chat(request: ChatRequest):
    messages = [
        {
            "role": "system",
            "content": "You are MI-IA, a helpful, honest and concise personal AI assistant. You run locally on the user's device.",
        },
        *request.history,
        {"role": "user", "content": request.message},
    ]

    payload = {"model": AI_MODEL, "messages": messages, "stream": False}

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{AI_BASE_URL.rstrip('/')}/chat/completions",
                json=payload,
            )
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Local AI engine unavailable at {AI_BASE_URL}. Start the local engine and make sure model '{AI_MODEL}' is installed. ({exc})",
        ) from exc

    data = response.json()
    try:
        answer = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise HTTPException(status_code=502, detail="The local AI engine returned an unexpected response.") from exc

    return {"response": answer}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
