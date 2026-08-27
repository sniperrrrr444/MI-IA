"""Explicit local fine-tuning pipeline for MI-IA Brain datasets."""
from pathlib import Path
import json


def load_examples(path: str):
    rows=[]
    p=Path(path)
    if not p.exists(): return rows
    for line in p.read_text(encoding="utf-8").splitlines():
        try:
            x=json.loads(line)
            if x.get("instruction") and x.get("response"): rows.append(x)
        except json.JSONDecodeError: pass
    return rows


def split_examples(rows, validation_ratio=0.1):
    cut=max(1, int(len(rows)*(1-validation_ratio))) if rows else 0
    return rows[:cut], rows[cut:]


def dataset_report(path: str):
    rows=load_examples(path)
    train, validation=split_examples(rows)
    return {"examples":len(rows),"train":len(train),"validation":len(validation)}


if __name__ == "__main__":
    import argparse
    parser=argparse.ArgumentParser(description="Inspect MI-IA local training data")
    parser.add_argument("dataset", nargs="?", default="data/training.jsonl")
    args=parser.parse_args()
    print(json.dumps(dataset_report(args.dataset), indent=2))
