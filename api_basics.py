"""
api_basics.py
CS6263 — Assignment

OpenAI-compatible API client for LLM querying.
Includes retry logic and configuration-based parameters.
"""

import time
import sys
import re
import os

from openai import OpenAI
from openai import APIConnectionError, RateLimitError, APIStatusError

from utils.config_loader import load_config

# Load config file
config = load_config()

api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not set")

client = OpenAI(
    base_url=config["api"]["base_url"],
    api_key=os.getenv("OPENAI_API_KEY")
)


def query_llm(prompt, temperature=None, max_tokens=None, max_retries=3, remove_think=True):
    """
    Sends a prompt to the LLM and returns the response text and token usage.

    Parameters:
        prompt (str): The input prompt.
        temperature (float): Sampling temperature (optional override).
        max_tokens (int): Maximum tokens (optional override).
        max_retries (int): Retry attempts for transient errors.
        remove_think (bool): Remove <think> blocks if present.

    Returns:
        tuple:
            str -> Model response text
            int -> Token usage
    """

    # Use config defaults if not provided
    if temperature is None:
        temperature = config["model"]["temperature"]

    if max_tokens is None:
        max_tokens = config["model"]["max_tokens"]

    model_name = config["model"]["name"]


    for attempt in range(max_retries):

        try:

            response = client.chat.completions.create(

                model=model_name,

                messages=[
                    {"role": "system", "content": "You are an AI debater. Always produce a clear answer and reasoning."},
                    {"role": "user", "content": prompt}
                ],

                temperature=temperature,
                max_tokens=max_tokens
            )


            # Extract response text
            choice = response.choices[0]

            text = None

            if hasattr(choice, "message") and choice.message:
                text = choice.message.content

            if text is None and hasattr(choice, "text"):
                text = choice.text

            if text is None:
                text = ""

            text = str(text)

            print("MODEL RAW OUTPUT:", text)


            # Token usage
            tokens_used = response.usage.total_tokens if hasattr(response, "usage") else 0


            # Remove <think> blocks if present
            if remove_think and text:
                text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
                text = text.strip()


            if not text.strip():
                text = "No argument generated."

            return text, tokens_used


        except RateLimitError:
            wait_time = 2 ** attempt
            print(f"[RateLimitError] Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

        except APIConnectionError:
            wait_time = 2 ** attempt
            print(f"[ConnectionError] Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

        except APIStatusError as e:
            print(f"[APIStatusError] Status code: {e.status_code}")
            break

        except Exception as e:
            print(f"[Unexpected Error] {e}")
            break


    return "Request failed after retries.", 0



def main():

    prompts = [
        "What is the capital of France?",
        "Explain recursion in simple terms.",
        "Summarize the importance of LLM in 2 sentences."
    ]

    for i, p in enumerate(prompts, 1):

        print(f"\n--- Prompt {i} ---")
        print("Input:", p)

        result = query_llm(p, temperature=0.2, max_tokens=200)

        print("Output:")
        print(result)



if __name__ == "__main__":
    main()