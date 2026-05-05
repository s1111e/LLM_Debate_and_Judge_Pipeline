from pathlib import Path


PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts"


def load_prompt_template(filename):
    path = PROMPT_DIR / filename
    return path.read_text(encoding="utf-8")


def render_prompt(filename, **values):
    safe_values = {key: "" if value is None else value for key, value in values.items()}
    return load_prompt_template(filename).format(**safe_values)
