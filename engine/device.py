import torch

def detect_device():
    if torch.cuda.is_available():
        return {"type":"cuda","name":torch.cuda.get_device_name(0)}
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return {"type":"mps","name":"Apple Metal"}
    return {"type":"cpu","name":"CPU"}

def recommended_dtype(device_type):
    return torch.float16 if device_type in {"cuda","mps"} else torch.float32
