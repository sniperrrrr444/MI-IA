import torch

def sample_next(logits: torch.Tensor, temperature: float = 0.7, top_k: int = 40):
    logits = logits / max(temperature, 1e-5)
    if top_k and top_k < logits.shape[-1]:
        values, indices = torch.topk(logits, top_k)
        filtered = torch.full_like(logits, float("-inf"))
        filtered.scatter_(0, indices, values)
        logits = filtered
    return torch.multinomial(torch.softmax(logits, dim=-1), 1).item()
