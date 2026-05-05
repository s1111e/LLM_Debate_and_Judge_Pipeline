"""
debate_orchestrator.py

Controls the multi-agent debate process.
"""

import json
import os

from agents.debater import Debater
from agents.judge import Judge
from utils.answer_utils import extract_answer, extract_confidence, opposite_answer
from utils.config_loader import load_config


class DebateOrchestrator:

    def __init__(self, rounds=None, config=None):
        self.config = config or load_config()
        debate_config = self.config["debate"]

        self.rounds = rounds if rounds is not None else debate_config["rounds"]
        self.adaptive_stopping = debate_config["adaptive_stopping"]
        self.convergence_rounds = debate_config["convergence_rounds"]
        self.log_path = debate_config["log_path"]

        self.debaterA = Debater("A")
        self.debaterB = Debater("B")
        self.judge = Judge()

    def _format_transcript(self, log_data, current_round_a=None):
        transcript_view = {
            "initial_positions": log_data["initial_positions"],
            "rounds": log_data["rounds"]
        }

        if current_round_a is not None:
            transcript_view["current_round_debater_a"] = current_round_a

        if log_data.get("consensus"):
            transcript_view["consensus"] = log_data["consensus"]

        return json.dumps(transcript_view, indent=2)

    def _build_legacy_transcript(self, log_data):
        transcript = [{
            "round": "initial",
            "A": log_data["initial_positions"]["A"]["text"],
            "B": log_data["initial_positions"]["B"]["text"]
        }]

        for round_data in log_data["rounds"]:
            transcript.append({
                "round": round_data["round"],
                "A": round_data["A"]["argument"],
                "B": round_data["B"]["argument"]
            })

        return transcript

    def _fallback_verdict(self, log_data):
        if log_data.get("consensus") in {"yes", "no"}:
            return log_data["consensus"], "consensus"

        if log_data["rounds"]:
            final_round = log_data["rounds"][-1]
            answer_a = final_round["A"].get("answer")
            answer_b = final_round["B"].get("answer")
            if answer_a in {"yes", "no"} and answer_a == answer_b:
                return answer_a, "final_round_convergence"

        return "unknown", None

    def _save_log(self, log_data):
        log_file = self.log_path
        os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)

        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(log_data)

        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)

    def run_debate(self, question, ground_truth=None, save_log=True):
        print("\n=== QUESTION ===")
        print(question)

        print("\n=== INITIAL ANSWERS ===")
        initial_A = self.debaterA.generate_initial_answer(question)
        initial_B = self.debaterB.generate_initial_answer(question)

        answer_A = extract_answer(initial_A)
        answer_B = extract_answer(initial_B)

        print("\nDebater A:")
        print(initial_A)
        print("\nDebater B:")
        print(initial_B)

        log_data = {
            "question": question,
            "ground_truth": ground_truth,
            "initial_positions": {
                "A": {"text": initial_A, "answer": answer_A},
                "B": {"text": initial_B, "answer": answer_B}
            },
            "rounds": [],
            "consensus": None,
            "stopped_early": False,
            "stop_reason": None
        }

        if answer_A in {"yes", "no"} and answer_A == answer_B:
            log_data["consensus"] = answer_A
            log_data["stopped_early"] = True
            log_data["stop_reason"] = "initial_consensus"
            print("\nInitial consensus detected. Skipping debate rounds.")
        else:
            position_A = answer_A if answer_A in {"yes", "no"} else "yes"
            position_B = answer_B if answer_B in {"yes", "no"} else opposite_answer(position_A)
            if position_B not in {"yes", "no"}:
                position_B = "no"

            previous_converged_answer = None
            consecutive_convergence = 0

            for round_number in range(1, self.rounds + 1):
                print(f"\n=== ROUND {round_number} ===")

                transcript_before_a = self._format_transcript(log_data)
                argument_A = self.debaterA.generate_argument(
                    question,
                    transcript_before_a,
                    round_number=round_number,
                    position=position_A
                )

                answer_A_round = extract_answer(argument_A)
                if answer_A_round not in {"yes", "no"}:
                    answer_A_round = position_A

                transcript_for_b = self._format_transcript(
                    log_data,
                    current_round_a={
                        "round": round_number,
                        "argument": argument_A,
                        "answer": answer_A_round
                    }
                )
                argument_B = self.debaterB.generate_argument(
                    question,
                    transcript_for_b,
                    round_number=round_number,
                    position=position_B
                )

                answer_B_round = extract_answer(argument_B)
                if answer_B_round not in {"yes", "no"}:
                    answer_B_round = position_B

                print("\nDebater A:")
                print(argument_A)
                print("\nDebater B:")
                print(argument_B)

                log_data["rounds"].append({
                    "round": round_number,
                    "A": {"argument": argument_A, "answer": answer_A_round},
                    "B": {"argument": argument_B, "answer": answer_B_round}
                })

                if answer_A_round == answer_B_round:
                    if previous_converged_answer == answer_A_round:
                        consecutive_convergence += 1
                    else:
                        consecutive_convergence = 1
                    previous_converged_answer = answer_A_round
                else:
                    consecutive_convergence = 0
                    previous_converged_answer = None

                if self.adaptive_stopping and consecutive_convergence >= self.convergence_rounds:
                    log_data["stopped_early"] = True
                    log_data["stop_reason"] = "round_convergence"
                    print("\nDebate converged early. Stopping debate.")
                    break

        print("\n=== JUDGE DECISION ===")
        judge_transcript = self._format_transcript(log_data)

        try:
            judge_result = self.judge.evaluate(question, judge_transcript)
        except Exception as e:
            print("Judge failed:", e)
            judge_result = "Judge evaluation failed."

        verdict = extract_answer(judge_result)
        confidence = extract_confidence(judge_result)
        fallback_source = None
        if verdict not in {"yes", "no"}:
            verdict, fallback_source = self._fallback_verdict(log_data)

        log_data["judge_reasoning"] = judge_result
        log_data["judge_result"] = judge_result
        log_data["verdict"] = verdict
        log_data["prediction"] = verdict
        log_data["final_answer"] = verdict
        log_data["confidence"] = confidence
        log_data["fallback_source"] = fallback_source
        log_data["transcript"] = self._build_legacy_transcript(log_data)

        print(judge_result)

        if save_log:
            self._save_log(log_data)
            print(f"\nDebate saved to {self.log_path}")

        return log_data["transcript"], log_data
