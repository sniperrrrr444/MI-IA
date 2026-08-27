from dataclasses import dataclass
from typing import Iterator
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .config import MODEL_PATH, MAX_NEW_TOKENS, TEMPERATURE

@dataclass
class RuntimeStatus:
    loaded: bool
    model_path: str
    device: str

class LocalRuntime:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def status(self) -> RuntimeStatus:
        return RuntimeStatus(bool(self.model), MODEL_PATH, self.device)

    def load(self) -> RuntimeStatus:
        if not MODEL_PATH:
            raise RuntimeError("MIIA_MODEL_PATH is not configured.")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
        dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            local_files_only=True,
            torch_dtype=dtype,
        )
        self.model.to(self.device)
        self.model.eval()
        return self.status()

    def generate(self, messages: list[dict], max_new_tokens: int = MAX_NEW_TOKENS,
                 temperature: float = TEMPERATURE) -> str:
        if self.model is None:
            self.load()

        prompt = self._format_messages(messages)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.inference_mode():
            output = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=temperature > 0,
                temperature=max(temperature, 1e-5),
                pad_token_id=self.tokenizer.eos_token_id,
            )

        generated = output[0][inputs["input_ids"].shape[-1]:]
        return self.tokenizer.decode(generated, skip_special_tokens=True).strip()

    def _format_messages(self, messages: list[dict]) -> str:
        if hasattr(self.tokenizer, "apply_chat_template"):
            try:
                return self.tokenizer.apply_chat_template(
                    messages, tokenize=False, add_generation_prompt=True
                )
            except Exception:
                pass
        return "\n".join(
            f"{m.get('role','user').upper()}: {m.get('content','')}" for m in messages
        ) + "\nASSISTANT:"
