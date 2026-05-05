import json
import re


VALID_ANSWERS = {"yes", "no"}


def normalize_answer(value):
    if value is True:
        return "yes"
    if value is False:
        return "no"
    if value is None:
        return "unknown"

    text = str(value).strip().lower()
    if text in VALID_ANSWERS:
        return text
    if text in {"true", "1"}:
        return "yes"
    if text in {"false", "0"}:
        return "no"
    return "unknown"


def _extract_from_json(text):
    try:
        payload = json.loads(text)
    except Exception:
        return "unknown"

    for key in ("final_answer", "finalAnswer", "answer", "verdict", "prediction"):
        if key in payload:
            answer = normalize_answer(payload[key])
            if answer in VALID_ANSWERS:
                return answer

    return "unknown"


def extract_answer(text):
    """
    Extract a normalized yes/no answer from model output.
    """

    if not text:
        return "unknown"

    raw = str(text).strip()

    json_answer = _extract_from_json(raw)
    if json_answer in VALID_ANSWERS:
        return json_answer

    patterns = [
        r"final\s+answer\s*[:\-]?\s*\**\s*(yes|no)\b",
        r"verdict\s*[:\-]?\s*\**\s*(yes|no)\b",
        r"answer\s*[:\-]?\s*\**\s*(yes|no)\b",
        r"\b(yes|no)\b\s*[–-]\s*",
    ]

    lowered = raw.lower()
    for pattern in patterns:
        match = re.search(pattern, lowered, flags=re.IGNORECASE)
        if match:
            return normalize_answer(match.group(1))

    matches = re.findall(r"\b(yes|no)\b", lowered, flags=re.IGNORECASE)
    if len(set(matches)) == 1 and matches:
        return normalize_answer(matches[0])

    return "unknown"


def extract_confidence(text):
    if not text:
        return None

    match = re.search(r"confidence\s*[:\-]?\s*(?:score\s*)?\**\s*([1-5])", str(text), re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def opposite_answer(answer):
    normalized = normalize_answer(answer)
    if normalized == "yes":
        return "no"
    if normalized == "no":
        return "yes"
    return "unknown"
