"""Explicit LoRA fine-tuning for MI-IA Brain data.

Usage: python -m engine.lora_train --model /path/model --data data/training.jsonl --output models/miia-lora
"""
import argparse, json
from pathlib import Path


def load_rows(path):
    rows=[]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        try:
            x=json.loads(line)
            if x.get("instruction") and x.get("response"):
                rows.append(x)
        except json.JSONDecodeError:
            continue
    return rows


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--model",required=True)
    p.add_argument("--data",default="data/training.jsonl")
    p.add_argument("--output",default="models/miia-lora")
    p.add_argument("--epochs",type=float,default=1.0)
    p.add_argument("--lr",type=float,default=2e-4)
    p.add_argument("--batch-size",type=int,default=1)
    args=p.parse_args()

    from datasets import Dataset
    from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
    from peft import LoraConfig
    from trl import SFTTrainer

    rows=load_rows(args.data)
    if not rows: raise SystemExit("No training examples found.")
    dataset=Dataset.from_list([{"text":f"### Instruction:\n{x['instruction']}\n\n### Response:\n{x['response']}"} for x in rows])
    tokenizer=AutoTokenizer.from_pretrained(args.model,local_files_only=True)
    if tokenizer.pad_token is None: tokenizer.pad_token=tokenizer.eos_token
    model=AutoModelForCausalLM.from_pretrained(args.model,local_files_only=True)
    lora=LoraConfig(r=16,lora_alpha=32,lora_dropout=0.05,bias="none",task_type="CAUSAL_LM",target_modules="all-linear")
    training=TrainingArguments(output_dir=args.output,num_train_epochs=args.epochs,learning_rate=args.lr,per_device_train_batch_size=args.batch_size,gradient_accumulation_steps=8,logging_steps=5,save_strategy="epoch",report_to="none")
    trainer=SFTTrainer(model=model,tokenizer=tokenizer,train_dataset=dataset,dataset_text_field="text",peft_config=lora,args=training,max_seq_length=1024)
    trainer.train()
    trainer.save_model(args.output)
    tokenizer.save_pretrained(args.output)
    print(f"Saved LoRA adapter to {args.output}")

if __name__=="__main__": main()
