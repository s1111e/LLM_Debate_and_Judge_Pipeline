"""
debater.py

Defines Debater agents for the debate system.
Each debater calls the LLM using the query_llm function.
"""

from api_basics import query_llm
from utils.answer_utils import normalize_answer
from utils.prompt_loader import render_prompt


class Debater:

    def __init__(self, role):
        """
        role: 'A' or 'B'
        """
        self.role = role
        self.template_name = "debaterA.txt" if role == "A" else "debaterB.txt"


    def generate_initial_answer(self, question):
        """
        Generate an independent initial position before seeing the opponent.
        """

        task = (
            "Independently choose the answer you believe is correct. "
            "Do not assume the other debater's position."
        )

        prompt = render_prompt(
            self.template_name,
            question=question,
            transcript="No previous debate transcript.",
            round_number="initial",
            position="Choose YES or NO independently.",
            task=task
        )

        response, tokens = query_llm(prompt)

        if not response:
            response = "No argument generated."

        return response


    def generate_argument(self, question, transcript, round_number=1, position="unknown"):
        answer = normalize_answer(position)
        position_text = answer.upper() if answer in {"yes", "no"} else "the answer you defended initially"

        if self.role == "A":
            task = "Defend your position and address Debater B's strongest previous objection."
        else:
            task = "Challenge Debater A's latest argument and defend your own position."

        prompt = render_prompt(
            self.template_name,
            question=question,
            transcript=transcript,
            round_number=round_number,
            position=position_text,
            task=task
        )

        response, tokens = query_llm(prompt)

        if not response or not response.strip():
            response = "No argument generated."

        return response
