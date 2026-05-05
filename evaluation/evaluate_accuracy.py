import json
import math
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.answer_utils import normalize_answer


def get_prediction(item):
    for key in ("final_answer", "prediction", "majority", "jury_prediction", "verdict"):
        if key in item:
            answer = normalize_answer(item[key])
            if answer in {"yes", "no"}:
                return answer
    return "unknown"


def is_correct(item):
    return get_prediction(item) == normalize_answer(item.get("ground_truth"))


def compute_accuracy(results):
    if not results:
        return 0
    return sum(1 for item in results if is_correct(item)) / len(results)


def load_results(path):
    if not os.path.exists(path):
        return []

    with open(path, encoding="utf-8") as f:
        return json.load(f)


def paired_mcnemar(results_a, results_b):
    by_question_b = {item["question"]: item for item in results_b}
    b = 0
    c = 0

    for item_a in results_a:
        item_b = by_question_b.get(item_a["question"])
        if item_b is None:
            continue

        a_correct = is_correct(item_a)
        b_correct = is_correct(item_b)

        if a_correct and not b_correct:
            b += 1
        elif not a_correct and b_correct:
            c += 1

    if b + c == 0:
        return {"b": b, "c": c, "statistic": 0, "p_value": 1}

    statistic = ((abs(b - c) - 1) ** 2) / (b + c)
    p_value = math.erfc(math.sqrt(statistic / 2))
    return {"b": b, "c": c, "statistic": statistic, "p_value": p_value}


def print_accuracy_table(named_results):
    print("\nRESULT TABLE")
    print("| Method | N | Accuracy |")
    print("|------|---:|------:|")
    for name, results in named_results:
        print(f"| {name} | {len(results)} | {compute_accuracy(results):.3f} |")


def print_significance_table(named_results):
    debate_results = dict(named_results).get("Debate")
    if not debate_results:
        return

    print("\nPAIRED MCNEMAR TESTS VS DEBATE")
    print("| Comparison | Debate-only correct | Baseline-only correct | Chi-square | p-value |")
    print("|------|---:|---:|---:|---:|")

    for name, results in named_results:
        if name == "Debate" or not results:
            continue
        stats = paired_mcnemar(debate_results, results)
        print(
            f"| Debate vs {name} | {stats['b']} | {stats['c']} | "
            f"{stats['statistic']:.3f} | {stats['p_value']:.4f} |"
        )


def main():
    named_results = [
        ("Debate", load_results("logs/debate_results.json")),
        ("Direct QA", load_results("logs/direct_qa_results.json")),
        ("Self Consistency", load_results("logs/self_consistency_results.json")),
        ("Jury Panel", load_results("logs/jury_results.json"))
    ]

    named_results = [(name, results) for name, results in named_results if results]

    print("\n==============================")
    print("EXPERIMENT RESULTS")
    print("==============================")

    print_accuracy_table(named_results)
    print_significance_table(named_results)


if __name__ == "__main__":
    main()
