from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from .config import HOST, PORT
from .runtime import LocalRuntime

app=FastAPI(title="MI-IA Engine",version="0.2.0")
runtime=LocalRuntime()

class ChatRequest(BaseModel):
    model:str|None=None
    messages:list[dict]
    max_tokens:int|None=None
    temperature:float|None=None
    stream:bool=False

@app.get("/health")
def health():
    s=runtime.status()
    return {"status":"ok","loaded":s.loaded,"model_path":s.model_path,"device":s.device,"device_name":s.device_name}

@app.get("/v1/models")
def models():
    return {"object":"list","data":[{"id":"miia-local","object":"model","owned_by":"miia"}]}

@app.post("/v1/chat/completions")
def chat(request:ChatRequest):
    try:
        if request.stream:
            def events():
                for chunk in runtime.stream(request.messages,request.max_tokens or 512,request.temperature if request.temperature is not None else .7):
                    import json
                    yield "data: "+json.dumps({"choices":[{"delta":{"content":chunk}}]})+"\n\n"
                yield "data: [DONE]\n\n"
            return StreamingResponse(events(),media_type="text/event-stream")
        answer=runtime.generate(request.messages,request.max_tokens or 512,request.temperature if request.temperature is not None else .7)
    except Exception as exc:
        raise HTTPException(503,f"MI-IA Engine could not generate a response: {exc}") from exc
    return {"id":"miia-local-completion","object":"chat.completion","model":request.model or "miia-local","choices":[{"index":0,"message":{"role":"assistant","content":answer},"finish_reason":"stop"}]}

if __name__=="__main__":
 import uvicorn
 uvicorn.run("engine.server:app",host=HOST,port=PORT,reload=False)
