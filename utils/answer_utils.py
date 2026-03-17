def extract_answer(text):
    """
    Extract YES or NO from LLM output.
    """

    if not text:
        return "unknown"

    text = text.lower()

    if "yes" in text:
        return "yes"

    if "no" in text:
        return "no"

    return "unknown"