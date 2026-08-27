from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime, timezone
import json, re, httpx

from .config import AI_BASE_URL, AI_MODEL, HOST, PORT

DATA_DIR=Path(__file__).resolve().parent.parent/"data"
MEMORY_FILE=DATA_DIR/"memory.json"
TRAINING_FILE=DATA_DIR/"training.jsonl"
CONVERSATION_FILE=DATA_DIR/"conversations.jsonl"
DATA_DIR.mkdir(exist_ok=True)
for f in (MEMORY_FILE,TRAINING_FILE,CONVERSATION_FILE):
    if not f.exists(): f.touch()

app=FastAPI(title="MI-IA Local",version="0.4.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

class ChatRequest(BaseModel):
    message:str
    history:list[dict]=[]
    use_memory:bool=True
    learn_from_conversation:bool=True

class MemoryRequest(BaseModel):
    text:str

class TrainingExample(BaseModel):
    instruction:str
    response:str

def read_memory():
    try:return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except:return []

def save_memory(items): MEMORY_FILE.write_text(json.dumps(items[-500:],ensure_ascii=False,indent=2),encoding="utf-8")

def relevant_memory(query):
    items=read_memory(); terms=set(re.findall(r"[a-zA-ZÀ-ÿ0-9]{4,}",query.lower()))
    return sorted(items,key=lambda x:sum(t in x["text"].lower() for t in terms),reverse=True)[:8]

def remember_conversation(message,answer):
    now=datetime.now(timezone.utc).isoformat()
    with CONVERSATION_FILE.open("a",encoding="utf-8") as f:
        f.write(json.dumps({"timestamp":now,"user":message,"assistant":answer},ensure_ascii=False)+"\n")
    # Conversation-derived training data is local and can be used by the explicit trainer later.
    with TRAINING_FILE.open("a",encoding="utf-8") as f:
        f.write(json.dumps({"instruction":message,"response":answer,"source":"conversation","timestamp":now},ensure_ascii=False)+"\n")

def system_prompt(query):
    mem=relevant_memory(query)
    text="\n".join("- "+m["text"] for m in mem) or "- No relevant memories."
    return ("You are MI-IA, a capable local personal AI. Be honest about what you know. "
            "Use the local memory below when relevant. Never claim that saving a conversation "
            "changed neural weights; conversation learning is stored locally as training data "
            "until an explicit training job updates a model checkpoint.\n\nLOCAL MEMORY:\n"+text)

@app.get("/api/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=2) as c:
            r=await c.get(f"{AI_BASE_URL.rstrip('/')}/models");r.raise_for_status()
        return {"status":"ok","local_engine":True,"model":AI_MODEL}
    except:return {"status":"degraded","local_engine":False,"model":AI_MODEL}

@app.get("/api/memory")
async def get_memory(): return {"memory":read_memory()}

@app.post("/api/memory")
async def add_memory(req:MemoryRequest):
    t=req.text.strip()
    if not t: raise HTTPException(400,"Memory cannot be empty.")
    items=read_memory();items.append({"text":t,"timestamp":datetime.now(timezone.utc).isoformat()});save_memory(items)
    return {"ok":True,"memory_count":len(items)}

@app.delete("/api/memory")
async def clear_memory(): save_memory([]);return {"ok":True}

@app.get("/api/learning/status")
async def learning_status():
    conv=sum(1 for _ in CONVERSATION_FILE.open(encoding="utf-8"))
    train=sum(1 for _ in TRAINING_FILE.open(encoding="utf-8"))
    return {"conversation_records":conv,"training_examples":train,"local_only":True}

@app.delete("/api/learning")
async def clear_learning():
    CONVERSATION_FILE.write_text("",encoding="utf-8");TRAINING_FILE.write_text("",encoding="utf-8")
    return {"ok":True}

@app.post("/api/train")
async def train(ex:TrainingExample):
    if not ex.instruction.strip() or not ex.response.strip(): raise HTTPException(400,"Both fields are required.")
    with TRAINING_FILE.open("a",encoding="utf-8") as f:f.write(json.dumps({"instruction":ex.instruction.strip(),"response":ex.response.strip(),"source":"manual"},ensure_ascii=False)+"\n")
    return {"ok":True}

@app.post("/api/chat")
async def chat(req:ChatRequest):
    messages=[{"role":"system","content":system_prompt(req.message)},*req.history,{"role":"user","content":req.message}]
    try:
        async with httpx.AsyncClient(timeout=180) as c:
            r=await c.post(f"{AI_BASE_URL.rstrip('/')}/chat/completions",json={"model":AI_MODEL,"messages":messages,"stream":False})
            r.raise_for_status()
        answer=r.json()["choices"][0]["message"]["content"]
    except Exception as exc: raise HTTPException(503,"MI-IA Engine is unavailable.") from exc
    if req.learn_from_conversation: remember_conversation(req.message,answer)
    return {"response":answer,"learned_locally":req.learn_from_conversation}

if __name__=="__main__":
 import uvicorn
 uvicorn.run("backend.main:app",host=HOST,port=PORT,reload=True)
