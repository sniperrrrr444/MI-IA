"""Offline evaluation helpers for comparing model checkpoints."""
import json
from pathlib import Path


def load_eval_set(path="data/eval.jsonl"):
    p=Path(path)
    if not p.exists(): return []
    rows=[]
    for line in p.read_text(encoding="utf-8").splitlines():
        try: rows.append(json.loads(line))
        except json.JSONDecodeError: pass
    return rows


def exact_match(expected, actual):
    return expected.strip().casefold()==actual.strip().casefold()


def score(expected, actual):
    """Simple deterministic baseline score; semantic evaluation can be added later."""
    return 1.0 if exact_match(expected, actual) else 0.0
