import sys
import os

# allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from debate.debate_orchestrator import DebateOrchestrator
from utils.answer_utils import extract_answer


# =========================
# LOAD DATASET
# =========================

data_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "strategyqa_100.json")
)

with open(data_path) as f:
    questions = json.load(f)


# =========================
# INITIALIZE DEBATE SYSTEM
# =========================

debate = DebateOrchestrator()

results = []


# =========================
# RUN EXPERIMENT
# =========================

for i, item in enumerate(questions):

    question = item["question"]
    gt = item["answer"]

    print("\n==============================")
    print(f"QUESTION {i+1}: {question}")

    transcript, judge_result = debate.run_debate(question)

    # extract YES / NO prediction from judge output
    pred = extract_answer(str(judge_result))

    # fallback if extraction fails
    if pred is None:
        pred = "unknown"

    results.append({
        "question": question,
        "ground_truth": gt,
        "prediction": pred,
        "judge_output": str(judge_result)
    })


# =========================
# SAVE RESULTS
# =========================

logs_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "logs")
)

os.makedirs(logs_dir, exist_ok=True)

save_path = os.path.join(logs_dir, "debate_results.json")

with open(save_path, "w") as f:
    json.dump(results, f, indent=2)


print("\nDebate experiment finished.")
print("Results saved to:", save_path)