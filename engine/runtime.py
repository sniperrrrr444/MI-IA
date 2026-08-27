from dataclasses import dataclass
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from .config import MODEL_PATH, MAX_NEW_TOKENS, TEMPERATURE
from .device import detect_device, recommended_dtype
from .cache import KVCache

@dataclass
class RuntimeStatus:
    loaded: bool
    model_path: str
    device: str
    device_name: str

class LocalRuntime:
    def __init__(self):
        d=detect_device()
        self.device=d["type"]; self.device_name=d["name"]
        self.tokenizer=None; self.model=None; self.kv_cache=KVCache()

    def status(self):
        return RuntimeStatus(bool(self.model),MODEL_PATH,self.device,self.device_name)

    def load(self):
        if not MODEL_PATH: raise RuntimeError("MIIA_MODEL_PATH is not configured.")
        self.tokenizer=AutoTokenizer.from_pretrained(MODEL_PATH,local_files_only=True)
        self.model=AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,local_files_only=True,
            torch_dtype=recommended_dtype(self.device)
        ).to(self.device)
        self.model.eval()
        return self.status()

    def _format(self,messages):
        if hasattr(self.tokenizer,"apply_chat_template"):
            try: return self.tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
            except Exception: pass
        return "\n".join(f"{m.get('role','user').upper()}: {m.get('content','')}" for m in messages)+"\nASSISTANT:"

    def generate(self,messages,max_new_tokens=MAX_NEW_TOKENS,temperature=TEMPERATURE):
        if self.model is None: self.load()
        inputs=self.tokenizer(self._format(messages),return_tensors="pt").to(self.device)
        with torch.inference_mode():
            output=self.model.generate(
                **inputs,max_new_tokens=max_new_tokens,
                do_sample=temperature>0,temperature=max(temperature,1e-5),
                top_k=40,use_cache=True,pad_token_id=self.tokenizer.eos_token_id
            )
        generated=output[0][inputs["input_ids"].shape[-1]:]
        self.kv_cache.set(True)
        return self.tokenizer.decode(generated,skip_special_tokens=True).strip()

    def stream(self,messages,max_new_tokens=MAX_NEW_TOKENS,temperature=TEMPERATURE):
        answer=self.generate(messages,max_new_tokens,temperature)
        for chunk in answer.split():
            yield chunk+" "
