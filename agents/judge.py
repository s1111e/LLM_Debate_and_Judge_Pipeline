"""
judge.py

LLM judge that evaluates debate transcripts.
"""

from api_basics import query_llm
from utils.prompt_loader import render_prompt


class Judge:

    def evaluate(self, question, transcript):

        prompt = render_prompt(
            "judge.txt",
            question=question,
            transcript=transcript
        )

        response, tokens = query_llm(prompt)

        return response
