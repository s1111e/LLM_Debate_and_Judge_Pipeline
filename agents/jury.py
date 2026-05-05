from collections import Counter

from api_basics import query_llm
from utils.answer_utils import extract_answer, extract_confidence
from utils.config_loader import load_config
from utils.prompt_loader import render_prompt


class JuryPanel:

    def __init__(self, judges=None, temperature=None, config=None):
        jury_config = (config or load_config())["jury"]
        self.judges = judges if judges is not None else jury_config["judges"]
        self.temperature = temperature if temperature is not None else jury_config["temperature"]

    def evaluate(self, question, transcript):
        decisions = []

        for judge_number in range(1, self.judges + 1):
            prompt = render_prompt(
                "jury_judge.txt",
                judge_number=judge_number,
                question=question,
                transcript=transcript
            )
            response, tokens = query_llm(prompt, temperature=self.temperature)
            answer = extract_answer(response)
            decisions.append({
                "judge": judge_number,
                "answer": answer,
                "confidence": extract_confidence(response),
                "raw_output": response,
                "tokens": tokens
            })

        valid_answers = [item["answer"] for item in decisions if item["answer"] in {"yes", "no"}]
        if valid_answers:
            majority = Counter(valid_answers).most_common(1)[0][0]
        else:
            majority = "unknown"

        disagreement = len(set(valid_answers)) > 1 if valid_answers else None

        return {
            "majority": majority,
            "disagreement": disagreement,
            "decisions": decisions
        }
