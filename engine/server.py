from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .config import HOST, PORT
from .runtime import LocalRuntime

app = FastAPI(title="MI-IA Engine", version="0.1.0")
runtime = LocalRuntime()

class ChatRequest(BaseModel):
    model: str | None = None
    messages: list[dict]
    max_tokens: int | None = None
    temperature: float | None = None

@app.get("/health")
def health():
    status = runtime.status()
    return {
        "status": "ok",
        "loaded": status.loaded,
        "model_path": status.model_path,
        "device": status.device,
    }

@app.get("/v1/models")
def models():
    return {"object":"list","data":[{"id":"miia-local","object":"model","owned_by":"miia"}]}

@app.post("/v1/chat/completions")
def chat(request: ChatRequest):
    try:
        answer = runtime.generate(
            request.messages,
            max_new_tokens=request.max_tokens or 512,
            temperature=request.temperature if request.temperature is not None else 0.7,
        )
    except Exception as exc:
        raise HTTPException(503, f"MI-IA Engine could not generate a response: {exc}") from exc

    return {
        "id": "miia-local-completion",
        "object": "chat.completion",
        "model": request.model or "miia-local",
        "choices": [{"index":0,"message":{"role":"assistant","content":answer},"finish_reason":"stop"}],
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("engine.server:app", host=HOST, port=PORT, reload=False)
