"""
debater.py

Defines Debater agents for the debate system.
Each debater calls the LLM using the query_llm function.
"""

from api_basics import query_llm


class Debater:

    def __init__(self, role):
        """
        role: 'A' or 'B'
        """
        self.role = role


    def generate_initial_answer(self, question):
        """
        Generate the initial position of the debater
        """

        if self.role == "A":
            stance = "YES"
        else:
            stance = "NO"

        prompt = f"""
You are Debater {self.role}.

Question:
{question}

Your role:
Argue that the answer is {stance}.

Provide:
1. Answer
2. Reasoning

IMPORTANT:
Do not include internal thinking.
Do not output <think> tags.
Write only the final answer and reasoning.
"""

        response, tokens = query_llm(prompt)

        if not response:
            response = "No argument generated."

        return response


    def generate_argument(self, question, transcript, round_number=1):

        if self.role == "A":
            role_instruction = "Defend the answer YES and respond to Debater B."
        else:
            role_instruction = "Attack Debater A's reasoning and defend the answer NO."

        prompt = f"""
        You are Debater {self.role} in a formal debate.

        Question:
        {question}

        This is round {round_number} of the debate.

        Debate transcript so far:
        {transcript}

        Your task:
        {role_instruction}

        Rules:
        - Respond to the other debater's latest argument.
        - Do NOT repeat your previous arguments.
        - Provide NEW reasoning or evidence.
        - Keep your answer under 120 words.
        - Do NOT include <think> tags or internal reasoning.

        Write only the final argument.
        """

        response, tokens = query_llm(prompt)

        if not response or not response.strip():
            response = "No argument generated."

        return response