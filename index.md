# LLM Debate and Judge Pipeline

This page summarizes the StrategyQA debate project. The interactive UI is provided by `index.html`, and the complete written report is available in [REPORT.md](./REPORT.md).

## Results

| Method | N | Accuracy |
|------|---:|------:|
| Debate | 100 | 0.700 |
| Direct QA | 100 | 0.680 |
| Self Consistency | 100 | 0.710 |
| Jury Panel | 100 | 0.660 |

The revised debate pipeline is competitive with the baselines and outperforms Direct QA in this run. Self-consistency achieves the best accuracy, while the jury panel is a completed bonus experiment but does not improve over the single judge here. Paired McNemar tests do not show a statistically significant gap between debate and the other methods at the 0.05 level.

## System

The pipeline uses two debaters and one judge:

1. Debater A and Debater B answer independently.
2. Initial consensus skips debate rounds.
3. Disagreement triggers up to three debate rounds.
4. Debater B sees Debater A's current-round argument before responding.
5. The judge evaluates the full transcript and returns a final answer plus confidence.
6. The optional jury panel runs three independent judges and takes a majority vote.

## Experiments

- Dataset: 100 StrategyQA questions.
- Debate calls: 2 initial calls, up to 6 round calls, and 1 judge call.
- Direct QA: one model call per question.
- Self Consistency: 9 independent samples per question.
- Jury Panel: 3 independent judges over the debate transcript.

Jury note: the implemented panel uses 3 independent LLM judges and majority vote. It compares jury accuracy against the single-judge debate result, but it is not a full multi-turn VERDICT-style deliberation protocol where judges revise after seeing each other's critiques. In the final logs, internal panel disagreement occurred on 1/100 questions, so disagreement was too sparse to support a strong difficulty correlation.

## Prompt Engineering

The final prompts are stored in `prompts/` and loaded at runtime. The important prompt changes were:

- Initial answers are not forced into fixed YES/NO roles.
- Debater outputs must begin with `Answer: YES` or `Answer: NO`.
- Debater B receives Debater A's current-round argument before responding.
- Judge outputs must include `Final Answer` and `Confidence`.
- Separate templates are used for Direct QA, Self Consistency, and Jury Judge prompts.

Prompt iteration was driven by failure analysis. Early logs showed one-sided debates, forced YES/NO roles, judge outputs without parseable verdicts, and truncation before confidence scores. The final version fixes these with independent initialization, current-round rebuttal context, strict answer labels, higher max-token budget, and editable prompt templates.

## Qualitative Analysis

The report now analyzes ten concrete saved transcripts:

- Firewall vs short circuit: correct consensus from clear category separation.
- Aerosmith in a Mitsubishi Outlander: debate resolves ambiguous group/entity wording.
- Baseball "Homer": debate rejects a plausible but unsupported etymology.
- Snowboarding in Hilo: debate clarifies local rarity versus regional access.
- C-SPAN and satellite telecommunications: debate recovers the key acronym evidence.
- Kayaks on Everest: wrong consensus locks in a shared assumption.
- Wool hand washing: judge overweights modern exceptions to an "only" question.
- Michael Vick and PETA: judge treats a hypothetical blacklist as an official-policy claim.
- Meatballs and origin: judge chooses broad cultural reasoning over dataset framing.
- San Francisco nature escape: debate exposes ambiguity, but the judge selects the broader interpretation.

Overall, debate helps when one agent introduces a missing distinction, but it fails when both agents share the same hidden premise or when the judge chooses a plausible interpretation that does not match the StrategyQA label.

## Requirement Coverage

| Requirement | Status | Evidence |
|------|------|------|
| 100+ questions | Complete | `data/strategyqa_100.json` |
| Modular agents | Complete | `agents/` |
| Debate orchestrator | Complete | `debate/debate_orchestrator.py` |
| Baselines | Complete | `experiments/run_direct_qa.py`, `experiments/run_self_consistency.py` |
| Evaluation script | Complete | `evaluation/evaluate_accuracy.py` |
| JSON logs | Complete | `logs/*.json` |
| Web UI | Complete | `index.html`, `app.py` |
| Prompt appendix | Complete | `REPORT.md`, `prompts/` |
| Bonus jury panel | Complete | `agents/jury.py`, `logs/jury_results.json` |

## Artifacts

- Code: `agents/`, `debate/`, `experiments/`, `evaluation/`
- Prompts: `prompts/`
- Config: `config/config.yaml`
- Logs: `logs/`
- Report: [REPORT.md](./REPORT.md)
