# LLM Debate and Judge Pipeline

This repository implements a multi-agent LLM debate system for StrategyQA-style yes/no reasoning questions. Two debaters produce independent initial answers, debate for multiple rounds when they disagree, and a judge selects the final verdict.

Project webpage / UI:
https://s1111e.github.io/LLM_Debate_and_Judge_Pipeline/

Full report:
[REPORT.md](./REPORT.md)

## Current Results

Computed from the checked-in logs with `python evaluation/evaluate_accuracy.py`:

| Method | Accuracy |
|------|------:|
| Debate | 0.700 |
| Direct QA | 0.680 |
| Self Consistency | 0.710 |
| Jury Panel | 0.660 |

## Setup

```bash
conda activate NLP_HW
pip install -r requirements.txt
```

Set your API profile before running LLM experiments. The code reads `UTSA_API_KEY`, `UTSA_BASE_URL`, and `UTSA_MODEL`; it also supports OpenAI-compatible `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `OPENAI_MODEL`.

```bash
$env:UTSA_API_KEY="YOUR_KEY"
$env:UTSA_BASE_URL="http://149.165.171.140:8888/v1"
$env:UTSA_MODEL="Qwen/Qwen3-8B"
```

If you want the key stored on the conda environment, use:

```bash
conda env config vars set UTSA_API_KEY="YOUR_KEY" -n NLP_HW
conda env config vars set UTSA_BASE_URL="http://149.165.171.140:8888/v1" -n NLP_HW
conda env config vars set UTSA_MODEL="Qwen/Qwen3-8B" -n NLP_HW
conda activate NLP_HW
```

Model endpoint, model name, temperature, debate rounds, self-consistency samples, and jury settings are configured in `config/config.yaml`.

Suggested smoke-test profile: start with Qwen3-8B or Llama 3.1 8B for quick checks, then switch to the larger VPN-only endpoints for final runs if they are reachable.

Available model profiles:

| Profile | `UTSA_BASE_URL` | `UTSA_MODEL` |
|------|------|------|
| Llama 3.1 8B | `http://149.165.173.247:8888/v1` | `meta-llama/Llama-3.1-8B-Instruct` |
| Qwen3 8B | `http://149.165.171.140:8888/v1` | `Qwen/Qwen3-8B` |
| GPT OSS 20B | `http://10.100.1.212:8888/v1` | `openai/gpt-oss-20b` |
| Llama 3.3 70B | `http://10.246.100.230/v1` | `llama-3.3-70b-instruct-awq` |
| Qwen3.5 27B | `http://10.100.1.213:8888/v1` | `Qwen/Qwen3.5-27B` |

## Run

Single debate:

```bash
python run_debate.py --question "Did the Roman Empire overlap with the Mayan civilization?"
```

LLM API smoke test:

```bash
python api_demo.py
```

Main experiments, including the bonus jury panel used in the reported table:

```bash
python experiments/run_debate_experiment.py
python experiments/run_direct_qa.py
python experiments/run_self_consistency.py
python experiments/run_jury.py
python evaluation/evaluate_accuracy.py
```

Local web UI:

```bash
export UTSA_API_KEY="YOUR_KEY"
export UTSA_BASE_URL="http://149.165.171.140:8888/v1"
export UTSA_MODEL="Qwen/Qwen3-8B"
python app.py
```

Then open `http://127.0.0.1:5000`.

The UI has two modes:

- `Show Saved`: loads a saved transcript from `logs/debate_logs.json`.
- `Live Run`: runs the full LLM debate pipeline through Flask. Start `python app.py` from the same terminal where the `UTSA_*` variables are set.

## Repository Structure

```text
agents/          Debater, judge, and optional jury panel agents
debate/          Debate orchestration and logging
experiments/     Debate, Direct QA, Self-Consistency, and Jury runners
evaluation/      Accuracy and paired McNemar evaluation
prompts/         Editable prompt templates
config/          Model and experiment hyperparameters
data/            StrategyQA 100-question subset
logs/            JSON experiment outputs and debate transcripts
```

## Notes

The latest saved run shows a much stronger debate pipeline than the earlier version. Debate is slightly below self-consistency, above Direct QA and the jury panel, and the paired McNemar tests do not show a statistically significant gap at the 0.05 level.
