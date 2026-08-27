from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import json
import re
import httpx

from .config import AI_BASE_URL, AI_MODEL, HOST, PORT

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MEMORY_FILE = DATA_DIR / "memory.json"
TRAINING_FILE = DATA_DIR / "training.jsonl"
DATA_DIR.mkdir(exist_ok=True)
if not MEMORY_FILE.exists(): MEMORY_FILE.write_text("[]", encoding="utf-8")
if not TRAINING_FILE.exists(): TRAINING_FILE.touch()

app = FastAPI(title="MI-IA Local", version="0.3.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []
    use_memory: bool = True

class MemoryRequest(BaseModel):
    text: str

class TrainingExample(BaseModel):
    instruction: str
    response: str

def read_memory():
    try: return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except Exception: return []

def save_memory(items):
    MEMORY_FILE.write_text(json.dumps(items[-500:], ensure_ascii=False, indent=2), encoding="utf-8")

def memory_context(query):
    items=read_memory()
    terms=set(re.findall(r"[a-zA-ZÀ-ÿ0-9]{4,}", query.lower()))
    ranked=sorted(items,key=lambda x: sum(t in x["text"].lower() for t in terms),reverse=True)
    return ranked[:8]

def build_system(query):
    memories=memory_context(query)
    memory_text="\n".join(f"- {m['text']}" for m in memories)
    return ("You are MI-IA, a capable, honest and concise personal AI assistant. "
            "You run locally on the user's device. Never claim to have learned or changed "
            "your neural weights unless an actual training process did so.\n\n"
            "Relevant local memory:\n"+(memory_text or "- No relevant memories."))

@app.get("/api/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=2) as client:
            r=await client.get(f"{AI_BASE_URL.rstrip('/')}/models"); r.raise_for_status()
        return {"status":"ok","local_engine":True,"model":AI_MODEL}
    except Exception:
        return {"status":"degraded","local_engine":False,"model":AI_MODEL}

@app.get("/api/memory")
async def get_memory(): return {"memory":read_memory()}

@app.post("/api/memory")
async def add_memory(request: MemoryRequest):
    text=request.text.strip()
    if not text: raise HTTPException(400,"Memory cannot be empty.")
    items=read_memory()
    items.append({"text":text})
    save_memory(items)
    return {"ok":True,"memory_count":len(items)}

@app.delete("/api/memory")
async def clear_memory():
    save_memory([])
    return {"ok":True}

@app.post("/api/train")
async def train(example: TrainingExample):
    # This is a local knowledge/training dataset, not silent weight modification.
    row={"instruction":example.instruction.strip(),"response":example.response.strip()}
    if not row["instruction"] or not row["response"]: raise HTTPException(400,"Both fields are required.")
    with TRAINING_FILE.open("a",encoding="utf-8") as f: f.write(json.dumps(row,ensure_ascii=False)+"\n")
    return {"ok":True,"message":"Training example saved locally.","training_examples":sum(1 for _ in TRAINING_FILE.open(encoding="utf-8"))}

@app.get("/api/training")
async def training_status():
    count=sum(1 for _ in TRAINING_FILE.open(encoding="utf-8"))
    return {"examples":count,"file":str(TRAINING_FILE)}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    system=build_system(request.message)
    messages=[{"role":"system","content":system},*request.history,{"role":"user","content":request.message}]
    payload={"model":AI_MODEL,"messages":messages,"stream":False}
    try:
        async with httpx.AsyncClient(timeout=180) as client:
            r=await client.post(f"{AI_BASE_URL.rstrip('/')}/chat/completions",json=payload); r.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(503,f"Local AI engine unavailable. Start the local engine and install '{AI_MODEL}'.") from exc
    try: answer=r.json()["choices"][0]["message"]["content"]
    except (KeyError,IndexError,TypeError) as exc: raise HTTPException(502,"Unexpected local AI response.") from exc
    return {"response":answer}

if __name__=="__main__":
    import uvicorn
    uvicorn.run("backend.main:app",host=HOST,port=PORT,reload=True)
