import torch
from engine.sampler import sample_next

def test_sample_next_returns_valid_token():
    token = sample_next(torch.tensor([0.1, 0.2, 0.3]), temperature=1.0, top_k=3)
    assert token in (0, 1, 2)
