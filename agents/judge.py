"""
judge.py

LLM judge that evaluates debate transcripts.
"""

from api_basics import query_llm


class Judge:

    def evaluate(self, question, transcript):


        prompt = f"""
        You are a neutral judge evaluating a debate.

        Question:
        {question}

        Debate transcript:
        {transcript}

        Analyze both sides carefully.

        Provide:

        1. Analysis of both debaters
        2. Strongest argument from each side
        3. Weakest argument from each side
        4. Final verdict (YES or NO)
        5. Confidence score (1-5)

        Do not include <think> tags.
        Keep the response concise.
        """

        response, tokens = query_llm(prompt)

        return response