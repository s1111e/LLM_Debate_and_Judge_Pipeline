import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.jury import JuryPanel
from debate.debate_orchestrator import DebateOrchestrator
from utils.config_loader import load_config


config = load_config()

data_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "strategyqa_100.json")
)

with open(data_path, encoding="utf-8") as f:
    questions = json.load(f)

debate = DebateOrchestrator(config=config)
jury_config = config.get("jury", {})
jury = JuryPanel(
    judges=jury_config["judges"],
    temperature=jury_config["temperature"],
    config=config
)

results = []

for i, item in enumerate(questions):
    question = item["question"]
    gt = item["answer"]

    print("\n==============================")
    print(f"QUESTION {i + 1}: {question}")

    transcript, debate_log = debate.run_debate(question, ground_truth=gt, save_log=False)
    transcript_text = json.dumps({
        "initial_positions": debate_log["initial_positions"],
        "rounds": debate_log["rounds"],
        "single_judge": debate_log["judge_result"]
    }, indent=2)

    jury_result = jury.evaluate(question, transcript_text)

    results.append({
        "question": question,
        "ground_truth": gt,
        "final_answer": jury_result["majority"],
        "single_judge_prediction": debate_log["prediction"],
        "single_judge_final_answer": debate_log["final_answer"],
        "single_judge_confidence": debate_log.get("confidence"),
        "initial_positions": debate_log["initial_positions"],
        "rounds": debate_log["rounds"],
        "single_judge_output": debate_log["judge_result"],
        "jury_prediction": jury_result["majority"],
        "jury_disagreement": jury_result["disagreement"],
        "jury_decisions": jury_result["decisions"]
    })

logs_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "logs")
)
os.makedirs(logs_dir, exist_ok=True)

save_path = os.path.join(logs_dir, "jury_results.json")

with open(save_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\nJury experiment finished.")
print("Results saved to:", save_path)
