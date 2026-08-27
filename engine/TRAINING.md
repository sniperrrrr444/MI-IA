# MI-IA training pipeline

Brain examples are stored locally and can become a real fine-tuning dataset.

```
Brain → training.jsonl → validation → tokenization → fine-tuning → checkpoint → Engine
```

Adding an example does not silently modify model weights. Training will be an explicit operation with checkpoints.
