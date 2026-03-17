import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from api_basics import query_llm
from utils.answer_utils import extract_answer
from utils.config_loader import load_config
from collections import Counter

config = load_config()

N = config["self_consistency"]["samples"]

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

    answers = []

    for i in range(N):

        prompt = f"""
Answer the following question with YES or NO.

Question:
{question}
"""

        response, tokens = query_llm(prompt, temperature=0.7)

        ans = extract_answer(response)

        answers.append(ans)

    majority = Counter(answers).most_common(1)[0][0]

    results.append({
        "question": question,
        "ground_truth": gt,
        "answers": answers,
        "majority": majority
    })

# =========================
# SAVE RESULTS
# =========================

logs_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "logs")
)

os.makedirs(logs_dir, exist_ok=True)

save_path = os.path.join(logs_dir, "self_consistency_results.json")

with open(save_path, "w") as f:
    json.dump(results, f, indent=2)


print("\n Self-consistency  experiment finished.")
print("Results saved to:", save_path)