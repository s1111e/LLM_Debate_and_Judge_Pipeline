from datasets import load_dataset
import json
import random

# load StrategyQA dataset
dataset = load_dataset("ChilleD/StrategyQA")

# StrategyQA questions
questions = dataset["train"]

# random 100 questions
sample = random.sample(list(questions), 100)

data = []

for item in sample:
    data.append({
        "question": item["question"],
        "answer": item["answer"]
    })

# save JSON
with open("data/strategyqa_100.json", "w") as f:
    json.dump(data, f, indent=2)

print("Saved 100 questions to data/strategyqa_100.json")