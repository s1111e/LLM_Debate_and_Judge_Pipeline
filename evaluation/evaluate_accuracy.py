import json
import os


def compute_accuracy(results):

    correct = 0
    total = 0

    for item in results:

        gt = item["ground_truth"]

        # convert ground truth to yes/no
        if gt is True:
            gt = "yes"
        elif gt is False:
            gt = "no"
        else:
            gt = str(gt).lower()

        pred = item.get("prediction", item.get("majority", "unknown"))
        pred = str(pred).lower()

        if pred == gt:
            correct += 1

        total += 1

    return correct / total if total > 0 else 0

def load_results(path):

    if not os.path.exists(path):
        print("File not found:", path)
        return []

    with open(path) as f:
        return json.load(f)


# =============================
# Load experiment outputs
# =============================

debate_results = load_results("logs/debate_results.json")
direct_results = load_results("logs/direct_qa_results.json")
self_results = load_results("logs/self_consistency_results.json")


# =============================
# Compute accuracies
# =============================

debate_acc = compute_accuracy(debate_results)
direct_acc = compute_accuracy(direct_results)
self_acc = compute_accuracy(self_results)


# =============================
# Print results table
# =============================

print("\n==============================")
print("EXPERIMENT RESULTS")
print("==============================")

print(f"Debate Accuracy: {debate_acc:.3f}")
print(f"Direct QA Accuracy: {direct_acc:.3f}")
print(f"Self Consistency Accuracy: {self_acc:.3f}")

print("\nRESULT TABLE")

print("| Method | Accuracy |")
print("|------|------|")
print(f"| Debate | {debate_acc:.3f} |")
print(f"| Direct QA | {direct_acc:.3f} |")
print(f"| Self Consistency | {self_acc:.3f} |")