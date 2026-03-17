"""
debate_orchestrator.py

Controls the multi-agent debate process.
"""

from agents.debater import Debater
from agents.judge import Judge
from utils.answer_utils import extract_answer

import json
import os


class DebateOrchestrator:

    def __init__(self, rounds=3):
        self.rounds = rounds

        self.debaterA = Debater("A")
        self.debaterB = Debater("B")
        self.judge = Judge()


    def run_debate(self, question):

        transcript = []

        print("\n=== QUESTION ===")
        print(question)

        # Phase 1 — Initial positions

        print("\n=== INITIAL ANSWERS ===")

        initial_A = self.debaterA.generate_initial_answer(question)
        initial_B = self.debaterB.generate_initial_answer(question)

        print("\nDebater A:")
        print(initial_A)

        print("\nDebater B:")
        print(initial_B)

        transcript.append({
            "round": "initial",
            "A": initial_A,
            "B": initial_B
        })

        # Phase 2 — Debate rounds

        prev_answer = None
        same_count = 0

        for r in range(self.rounds):

            print(f"\n=== ROUND {r+1} ===")

            current_transcript = ""

            for t in transcript:

                if t["round"] == "initial":
                    current_transcript += f"\nInitial Position\n"
                    current_transcript += f"Debater A: {t['A']}\n"
                    current_transcript += f"Debater B: {t['B']}\n"

                else:
                    current_transcript += f"\nRound {t['round']}\n"
                    current_transcript += f"Debater A: {t['A']}\n"
                    current_transcript += f"Debater B: {t['B']}\n"


            argument_A = self.debaterA.generate_argument(
                question,
                current_transcript,
                round_number=r+1
            )

            argument_B = self.debaterB.generate_argument(
                question,
                current_transcript,
                round_number=r+1
            )


            print("\nDebater A:")
            print(argument_A)

            print("\nDebater B:")
            print(argument_B)


            # -------- Extract YES/NO answers --------
            answer_A = extract_answer(argument_A)
            answer_B = extract_answer(argument_B)


            # -------- Adaptive stopping logic --------
            if answer_A == answer_B:

                if prev_answer == answer_A:
                    same_count += 1
                else:
                    same_count = 1

                prev_answer = answer_A

            else:
                same_count = 0


            # Stop debate early if agents converge
            transcript.append({
                "round": r+1,
                "A": argument_A,
                "B": argument_B
            })

            # Stop debate early if agents converge
            if same_count >= 2:
                print("\nDebate converged early. Stopping debate.")
                break

        # Phase 3 — Judge decision

        print("\n=== JUDGE DECISION ===")

        try:
            judge_result = self.judge.evaluate(question, transcript)
        except Exception as e:
            print("Judge failed:", e)
            judge_result = "Judge evaluation failed."

        print(judge_result)


        # ===== SAVE LOG =====

        log_data = {
            "question": question,
            "transcript": transcript,
            "judge_result": judge_result
        }

        os.makedirs("logs", exist_ok=True)

        log_file = "logs/debate_logs.json"

        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(log_data)

        with open(log_file, "w") as f:
            json.dump(logs, f, indent=2)

        print("\nDebate saved to logs/debate_logs.json")

        return transcript, judge_result