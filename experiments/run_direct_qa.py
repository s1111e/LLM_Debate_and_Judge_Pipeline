import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from api_basics import query_llm
from utils.answer_utils import extract_answer
from utils.config_loader import load_config

config = load_config()

# dataset path
data_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "strategyqa_100.json")
)

with open(data_path) as f:
    questions = json.load(f)

results = []

for item in questions:

    question = item["question"]
    gt = item["answer"]

    prompt = f"""
Answer the following question with YES or NO and provide short reasoning.

Question:
{question}
"""

    response, tokens = query_llm(prompt)

    pred = extract_answer(response)

    results.append({
        "question": question,
        "ground_truth": gt,
        "prediction": pred,
        "raw_output": response
    })


# -------- save results safely --------

log_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "logs", "direct_qa_results.json")
)

os.makedirs(os.path.dirname(log_path), exist_ok=True)

with open(log_path, "w") as f:
    json.dump(results, f, indent=2)

print("Direct QA experiment finished.")