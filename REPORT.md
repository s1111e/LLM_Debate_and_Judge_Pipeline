# LLM Debate and Judge Pipeline - Report

Webpage / UI: https://s1111e.github.io/LLM_Debate_and_Judge_Pipeline/

Repository README: [README.md](./README.md)

## 1. Methodology

This project evaluates whether an adversarial multi-agent debate pipeline improves yes/no commonsense reasoning on StrategyQA compared with simpler single-model baselines. The core research question is whether a judge can make a better final decision after seeing two agents challenge each other's reasoning than after seeing one direct answer.

The system has three main agents:

- Debater A: proponent role
- Debater B: opponent role
- Judge: neutral evaluator

The bonus experiment adds a fourth component:

- Jury Panel: 3 independent judges that vote over the same debate transcript

### Architecture

The code is organized into separate modules:

- `agents/debater.py`: debater agent behavior
- `agents/judge.py`: single judge behavior
- `agents/jury.py`: optional multi-judge panel
- `debate/debate_orchestrator.py`: initialization, debate rounds, judgment, and logging
- `experiments/`: debate, direct QA, self-consistency, and jury experiment runners
- `evaluation/evaluate_accuracy.py`: accuracy and paired McNemar tests
- `prompts/`: editable prompt templates
- `config/config.yaml`: model profile, temperature, max tokens, rounds, stopping, and sample counts
- `app.py` and `index.html`: local web UI

### Debate Protocol

The implemented protocol follows the assignment's four phases.

1. Initialization: both debaters answer the question independently without seeing each other.
2. Consensus check: if both initial answers match, the system records consensus and skips debate rounds.
3. Multi-round debate: when the debaters disagree, Debater A argues first and Debater B responds after seeing Debater A's current-round argument. Each round receives the previous transcript as context.
4. Judgment and evaluation: the judge receives the complete transcript and returns analysis, strongest and weakest arguments, final answer, and confidence.

The debate is configured for 3 rounds with adaptive stopping. The system logs the original question, ground truth, initial positions, per-round arguments, judge reasoning, verdict, confidence, and transcript.

### Model and Hyperparameters

The model endpoint is OpenAI-compatible and selected through environment variables:

- `UTSA_API_KEY`
- `UTSA_BASE_URL`
- `UTSA_MODEL`

The saved run used the UTSA-hosted model profile configured during the experiment. Hyperparameters are stored in `config/config.yaml`:

- Debate rounds: 3
- Adaptive stopping: enabled
- Convergence rounds: 2
- Model temperature: 0.3
- Max tokens: 900
- Self-consistency samples: 9
- Jury judges: 3

The self-consistency sample count matches the maximum debate call budget for 3 rounds: 2 initial calls, 6 debate calls, and 1 judge call.

LLM-assisted tools were used for coding support and debugging. The final project structure, code, logs, and report were reviewed and edited by the author.

## 2. Experiments

The main dataset is a 100-question subset of StrategyQA. StrategyQA is appropriate for this assignment because it contains yes/no commonsense questions that often require implicit multi-hop reasoning.

### Compared Methods

- Debate Pipeline: two debaters plus a judge, with 3 configured rounds and adaptive stopping.
- Direct QA: one direct answer with visible rationale.
- Self Consistency: 9 independent samples with majority vote.
- Jury Panel: bonus setting with 3 independent judges voting over the debate transcript.

### Quantitative Results

Current checked-in results from `logs/*.json`:

| Method | N | Accuracy |
|------|---:|------:|
| Debate | 100 | 0.700 |
| Direct QA | 100 | 0.680 |
| Self Consistency | 100 | 0.710 |
| Jury Panel | 100 | 0.660 |

Paired McNemar tests against Debate:

| Comparison | Debate-only correct | Baseline-only correct | Chi-square | p-value |
|------|---:|---:|---:|---:|
| Debate vs Direct QA | 7 | 5 | 0.083 | 0.7728 |
| Debate vs Self Consistency | 4 | 5 | 0.000 | 1.0000 |
| Debate vs Jury Panel | 7 | 3 | 0.900 | 0.3428 |

These results show that the revised debate pipeline is competitive with the direct and self-consistency baselines. Debate outperforms Direct QA in this run, and Self Consistency achieves the best accuracy by a small margin. The paired tests do not show a statistically significant difference from debate at the 0.05 level in this 100-question run.

### Interpretation

Direct QA remains strong because many StrategyQA examples can be answered correctly with a concise reasoning trace. Self-consistency improves on Direct QA by reducing variance across independent samples. Debate improves transparency because it creates a transcript of competing arguments, but it can also introduce new opportunities for error if agents make unsupported claims.

The jury panel result is important for the bonus objective because it demonstrates a multi-judge extension, but this run does not show an accuracy gain from judge-time scaling. The panel reached 0.660, below the single-judge debate result. This suggests that independent judges can add stability in some cases, but they can also reinforce the same transcript-level errors when the debate evidence is weak or misleading.

### Multi-Agent Judge Panel Analysis

The bonus jury experiment uses 3 LLM judges. Each judge independently evaluates the same debate transcript, and the final panel answer is selected by majority vote. This implements a multi-judge panel and allows direct comparison against the single-judge debate result. It is not a full multi-turn VERDICT-style deliberation protocol where judges see and revise their answers after reading each other's critiques; rather, it is an independent jury panel with majority aggregation.

In the final logs, the jury panel produced:

- 100 jury decisions
- 3 judge outputs per question
- 0.660 jury accuracy
- 0.700 single-judge debate accuracy in the main reported debate run
- 1 internal panel disagreement out of 100 questions
- 5 cases where the panel answer differed from the single judge recorded during the jury run

The only internal panel disagreement occurred on the question "Would a Common warthog starve in a greenhouse?" The three judges voted NO, YES, NO, so the majority answer was NO, matching the ground truth. This suggests that disagreement can flag a question with competing plausible interpretations, but one disagreement out of 100 is too sparse for a reliable statistical correlation with difficulty.

The panel changed several single-judge outcomes in the jury run. It corrected cases where the single judge produced `unknown` or selected the wrong answer, such as the Michael Vick/PETA question and the Nancy Pelosi/Pearl Harbor question. However, the panel also produced incorrect majority decisions on some questions where all judges shared the same mistaken framing. Therefore, the final evidence does not show that the jury panel improved consensus quality overall. The main lesson is that adding judges helps only if the panel introduces genuinely diverse interpretations; if all judges inherit the same transcript-level bias, majority voting can make the wrong answer look more stable.

## 3. Analysis

I reviewed the final saved transcripts rather than only the aggregate accuracy table. The final debate run contains 100 questions: 16 entered full debate rounds and 84 skipped rounds after initial agreement. The no-round cases were easier overall, with 61/84 correct, while the round cases were harder, with 9/16 correct. This is expected because disagreement tends to occur on ambiguous or fact-sensitive questions.

The table below summarizes ten representative transcripts. I selected cases that show different behaviors: correct consensus, correct debate recovery, semantic ambiguity, wrong consensus, and judge failures.

| # | Question Short Name | Ground Truth | Debate Prediction | Rounds | Main Pattern |
|---:|------|------|------|---:|------|
| 1 | Firewall vs short circuit | NO | NO | 0 | Correct consensus from clear category separation |
| 2 | Aerosmith in Outlander | YES | YES | 3 | Debate resolves ambiguous entity/group wording |
| 3 | Baseball "Homer" | NO | NO | 3 | Debate rejects unsupported etymology |
| 4 | Snowboarding in Hilo | YES | YES | 3 | Debate clarifies local rarity vs regional access |
| 5 | C-SPAN and satellite | YES | YES | 3 | Debate recovers key acronym evidence |
| 6 | Kayaks on Everest | YES | NO | 0 | Wrong consensus locks in shared assumption |
| 7 | Wool hand washed only | YES | NO | 3 | Judge overweights modern exceptions |
| 8 | Michael Vick and PETA blacklist | YES | NO | 3 | Judge treats hypothetical as official-policy question |
| 9 | Meatballs and country of origin | YES | NO | 3 | Judge chooses broad cultural answer over dataset framing |
| 10 | San Francisco nature escape | NO | YES | 3 | Judge accepts broad interpretation despite weak confidence |

### Case 1: Correct Consensus, Firewall vs Short Circuit

Question: Can a firewall protect against a short circuit?

Ground truth: NO. Debate prediction: NO. Rounds: 0.

Both debaters independently answered NO. The useful reasoning was a category distinction: a firewall is a cybersecurity or fire-safety concept, while a short circuit is an electrical fault. The judge selected NO with confidence 5 because both arguments separated software/building protection from electrical protection devices such as breakers. This is the ideal use of the consensus shortcut. The agents agreed because the question had a clear domain mismatch, so skipping debate saved calls without losing accuracy.

### Case 2: Successful Debate on Ambiguity, Aerosmith in an Outlander

Question: Can Aerosmith fit in a 2020 Mitsubishi Outlander?

Ground truth: YES. Debate prediction: YES. Rounds: 3.

The initial positions disagreed. Debater A treated "Aerosmith" as the five band members and argued that a 2020 Mitsubishi Outlander has enough seats. Debater B argued that a band is not a single physical object and that the question may be ill-posed. Across the rounds, Debater A kept the focus on physical seating capacity, while Debater B repeated the entity-wording objection. The judge chose YES with confidence 4 because the most natural reading is whether the members can fit, not whether an abstract band entity can fit. This is a strong example of debate helping the judge choose between two interpretations.

### Case 3: Successful Debate on False Etymology, Baseball "Homer"

Question: In baseball, is a "Homer" named after the poet Homer who wrote the Odyssey?

Ground truth: NO. Debate prediction: NO. Rounds: 3.

Debater A initially defended a literary origin, claiming "Homer" came from "homeric" epic feats. Debater B argued that the term is baseball-specific and tied to "home run" rather than the Greek poet. The debate was useful because it forced the judge to compare a plausible-sounding but unsupported origin story against a simpler etymological explanation. The judge selected NO with confidence 4, explicitly noting that Debater A's literary story lacked concrete historical evidence. This matches Irving et al.'s prediction that adversarial argument can expose weak reasoning when one side invents a fluent but fragile explanation.

### Case 4: Successful Debate on Scope, Snowboarding in Hilo

Question: Snowboarding is a rarity in Hilo?

Ground truth: YES. Debate prediction: YES. Rounds: 3.

The disagreement was about scope. Debater A argued NO because people in Hawaii could travel to snowboarding locations, so snowboarding is regionally accessible. Debater B argued YES because Hilo itself has a tropical climate and lacks local snowboarding infrastructure. The judge selected YES with confidence 5 because "rarity in Hilo" is about local prevalence, not whether residents can travel elsewhere. This transcript shows debate working well on semantic scope: the winning argument narrowed the question to the relevant geographic unit.

### Case 5: Successful Recovery, C-SPAN and Satellite Telecommunications

Question: Does the name C-SPAN refer to a form of telecommunications that utilizes outer space?

Ground truth: YES. Debate prediction: YES. Rounds: 3.

Debater A started with NO, despite mentioning that C-SPAN stands for Cable-Satellite Public Affairs Network. Debater B corrected the key point: "Satellite" refers to satellite technology, and satellites rely on outer-space infrastructure. The judge selected YES with confidence 5. This is one of the clearest successes in the final run because the transcript contains an actual correction. Debate helped because the opposing agent surfaced the missing bridge between the acronym and the question's wording.

### Case 6: Wrong Consensus, Kayaks on Everest

Question: Are kayaks used at the summit of Mount Everest?

Ground truth: YES. Debate prediction: NO. Rounds: 0.

Both debaters answered NO immediately because they interpreted "kayak" only as a watercraft and reasoned that Everest's summit has no liquid water. The judge accepted the consensus with confidence 5. This failure is important because there was no adversarial pressure after the shared initial assumption. If the dataset label depends on a less obvious interpretation or rare fact, the pipeline cannot recover when both debaters miss it before the debate begins. This is the main cost of the consensus shortcut.

### Case 7: Failure on "Only", Wool Hand Washing

Question: Should wool be hand washed only?

Ground truth: YES. Debate prediction: NO. Rounds: 3.

Debater A argued YES because wool can shrink, felt, or stretch under agitation. Debater B argued NO because modern machines have wool cycles and wool-specific detergents. The judge chose NO with confidence 4, treating the existence of safe machine-washing exceptions as enough to defeat "only." The likely failure is semantic: the dataset appears to expect the conservative garment-care rule, while the judge interpreted the question as an absolute claim about all wool under all modern conditions. Debate did not fail by being empty; it failed because the judge selected the more practical but label-mismatched interpretation.

### Case 8: Failure on Hypothetical Framing, Michael Vick and PETA

Question: Is Michael Vick on People for the Ethical Treatment of Animals's hypothetical blacklist?

Ground truth: YES. Debate prediction: NO. Rounds: 3.

Debater A argued YES because Michael Vick's dogfighting conviction directly conflicts with PETA's animal-rights stance. Debater B argued NO because PETA does not maintain a formal public blacklist and focuses on advocacy rather than exclusion lists. The judge selected NO with confidence 4. This is a judge failure more than a debater failure: the word "hypothetical" should have made the official-existence objection less important. Direct QA and self-consistency answered this item correctly, suggesting that the debate transcript gave the judge a distracting formalism to overvalue.

### Case 9: Failure on Dataset Framing, Meatballs and Country of Origin

Question: Do restaurants associate meatballs with the wrong country of origin?

Ground truth: YES. Debate prediction: NO. Rounds: 3.

Debater A argued YES by focusing on Swedish association and the idea that restaurants commonly frame meatballs as Italian. Debater B argued NO because meatballs exist across many cultures and therefore no single country "owns" the dish. The judge selected NO with confidence 5. This failure shows a common StrategyQA issue: the model can give a reasonable broad-world answer while missing the dataset's intended contrast. The judge preferred a pluralistic culinary-history argument, but the label expects a narrower fact about restaurant association and origin.

### Case 10: Failure on Broad Interpretation, San Francisco Nature Escape

Question: Would someone go to San Francisco for a nature escape?

Ground truth: NO. Debate prediction: YES. Rounds: 3.

Debater A argued YES using Golden Gate Park, the Presidio, coastal trails, and nearby nature access. Debater B argued NO because San Francisco is primarily an urban destination and a "nature escape" implies getting away from dense city infrastructure. The judge selected YES with confidence 3, which is lower than most other judge decisions. This lower confidence is meaningful: the transcript exposed the ambiguity, but the judge still selected the broader reading. The case shows that debate can make ambiguity visible without necessarily resolving it according to the dataset label.

### Cross-Case Findings

Three patterns appear repeatedly.

First, debate helps when at least one debater contributes a missing distinction. The Aerosmith, Homer, Hilo, and C-SPAN examples all contain a useful correction or scope clarification. These cases fit the theoretical motivation from Irving et al.: adversarial pressure can expose weak or incomplete reasoning and give the judge a clearer comparison.

Second, debate is weak when both agents share the same hidden premise. The kayak example skipped rounds because both debaters agreed immediately. Consensus is efficient, but it removes the chance for adversarial correction. This matters because 84/100 examples skipped full rounds in the final run.

Third, the judge is sensitive to framing. Wool, Michael Vick, meatballs, and San Francisco all contain plausible arguments on both sides. In those cases, the judge sometimes chose a broad, practical, or formal interpretation that did not match the StrategyQA label. This explains why debate produced useful transcripts but did not dominate self-consistency.

### Final Assessment

The final run supports a conditional version of the AI debate hypothesis. Debate improved transparency and sometimes corrected single-agent mistakes, especially on questions where one side introduced a concrete missing fact or semantic distinction. However, debate did not guarantee correctness. It failed when both debaters started from the same mistaken assumption, when the judge overvalued a plausible but label-mismatched interpretation, or when the transcript contained no grounded evidence beyond fluent argumentation. Overall, the debate pipeline is valuable as an inspectable reasoning method, but the results suggest that debate quality depends more on argument diversity and judge calibration than on simply adding more agent turns.

## 4. Prompt Engineering

Prompt design was iterated from simple role prompts toward structured templates.

### Initial Prompt Problems

The first prompt version used simple role instructions: Debater A argued one side, Debater B argued the other, and the judge selected a winner. This produced several issues:

- Missing arguments from one debater
- One-sided debates
- Weak or repeated arguments
- Judge outputs without a parseable final answer
- Truncated judge outputs before confidence

### Final Prompt Design Decisions

- Initial answers are no longer forced to YES/NO by role.
- Debaters must start with `Answer: YES` or `Answer: NO`.
- Debater B receives Debater A's current-round argument before responding.
- The judge must include analysis, strongest arguments, weakest arguments, final answer, and confidence.
- Prompt files are stored in `prompts/` and loaded by the code instead of being hardcoded inside agent classes.
- Direct QA, self-consistency, and jury prompts are separate from the debate prompts.

These changes improved reliability and made evaluation easier because the model outputs became more consistent.

### Iteration Summary

| Observed failure | Change made | Expected effect |
|------|------|------|
| Debater A or B sometimes returned empty content | Added explicit "never return empty responses" style constraints and required `Answer: YES/NO` labels | Reduced one-sided debates and made answer extraction easier |
| Initial roles forced A toward YES and B toward NO | Changed initialization so both debaters answer independently | Made the consensus phase meaningful and closer to the assignment protocol |
| Debater B did not always address Debater A's newest argument | Passed Debater A's current-round argument into Debater B's prompt | Improved round-by-round rebuttal behavior |
| Judge prose was hard to parse | Required `Winning Debater`, `Final Answer`, and `Confidence` labels | Reduced `unknown` predictions |
| Judge output could be truncated | Increased `max_tokens` from the earlier small budget to 900 | Gave the judge enough space for analysis plus verdict |
| Prompt text was hardcoded inside agent classes | Moved final templates into `prompts/` and added `utils/prompt_loader.py` | Made prompt iteration visible, editable, and reproducible |
| Self-consistency used fewer calls than debate | Increased self-consistency samples to 9 | Matched debate's maximum inference-time compute budget |

### Role Framing

The final prompts still describe Debater A as a proponent and Debater B as an opponent, but they do not hard-force the initial answer to fixed labels. This matters because the assignment asks for independent initial positions and then a consensus check. If both agents independently agree, the debate can skip rounds; if they disagree, the adversarial roles become useful in later rounds.

### Reasoning Style

The prompts ask for concise visible rationales rather than hidden reasoning. This keeps the transcript inspectable while avoiding unstructured internal traces. The judge prompt asks for analysis of both debaters, strongest arguments, weakest arguments, a final answer, and a confidence score. This gives enough reasoning for evaluation without making parsing depend on free-form prose.

### Output Format Constraints

The most important practical change was strict output labeling. Debater responses start with `Answer: YES` or `Answer: NO`, and judge responses include `Final Answer:` and `Confidence:`. This was added after early logs produced strong prose but weak machine-readable verdicts. For an experiment evaluated over 100 questions, parseability is not a cosmetic issue; it directly affects accuracy measurement.

## 5. Requirement Coverage

| Requirement | Status | Evidence |
|------|------|------|
| 100+ reasoning questions | Complete | `data/strategyqa_100.json` |
| Debater, judge, orchestrator modules | Complete | `agents/`, `debate/` |
| Initialization, debate, judgment, evaluation phases | Complete | `debate/debate_orchestrator.py`, `evaluation/` |
| Direct QA baseline | Complete | `experiments/run_direct_qa.py` |
| Self-consistency baseline | Complete | `experiments/run_self_consistency.py` |
| Configuration file | Complete | `config/config.yaml` |
| Editable prompt templates | Complete | `prompts/` |
| Full JSON logs | Complete | `logs/*.json` |
| Evaluation scripts | Complete | `evaluation/evaluate_accuracy.py` |
| requirements.txt | Complete | `requirements.txt` |
| Functional web UI | Complete | `index.html`, `app.py` |
| Bonus jury panel | Complete | `agents/jury.py`, `experiments/run_jury.py`, `logs/jury_results.json` |

## Appendix: Full Prompts

### Debater A

```text
You are Debater A, the proponent in a structured reasoning debate.

Question:
{question}

Debate transcript so far:
{transcript}

Round:
{round_number}

Current position:
{position}

Task:
{task}

Rules:
- Start with exactly one line: Answer: YES or Answer: NO
- Give a concise visible rationale using evidence from the question or commonsense facts.
- In debate rounds, defend your current position and respond to Debater B's strongest point.
- Do not repeat earlier arguments unless you are correcting them.
- Do not output hidden reasoning, XML tags, or empty responses.

Answer:
```

### Debater B

```text
You are Debater B, the opponent in a structured reasoning debate.

Question:
{question}

Debate transcript so far:
{transcript}

Round:
{round_number}

Current position:
{position}

Task:
{task}

Rules:
- Start with exactly one line: Answer: YES or Answer: NO
- Give a concise visible rationale using evidence from the question or commonsense facts.
- In debate rounds, challenge Debater A's latest reasoning and defend your current position.
- Do not repeat earlier arguments unless you are correcting them.
- Do not output hidden reasoning, XML tags, or empty responses.

Answer:
```

### Judge

```text
You are a neutral judge evaluating a structured debate.

Question:
{question}

Complete debate transcript:
{transcript}

Your task:
Evaluate both debaters' arguments and select the answer most likely to be correct.

Required output format:
Final Answer: YES or NO
Confidence: integer from 1 to 5
Winning Debater: A, B, or Consensus

Analysis:
- Debater A:
- Debater B:

Strongest Arguments:
- Debater A:
- Debater B:

Weakest Arguments:
- Debater A:
- Debater B:

Rules:
- Base the verdict on logic and evidence, not style or verbosity.
- Give a concise visible rationale, not hidden reasoning.
- Put Final Answer and Confidence at the very top before analysis.
- Always include Final Answer and Confidence exactly as labeled.
```

### Direct QA

```text
Answer the following StrategyQA question directly.

Question:
{question}

Rules:
- Start with exactly one line: Answer: YES or Answer: NO
- Provide a concise visible rationale.

Answer:
```

### Self Consistency

```text
Answer the following StrategyQA question independently.

Question:
{question}

Rules:
- Start with exactly one line: Answer: YES or Answer: NO
- Provide a brief reason.

Answer:
```

### Jury Judge

```text
You are Judge {judge_number} in a multi-judge panel.

Question:
{question}

Complete debate transcript:
{transcript}

Your task:
Independently evaluate the debate and select the answer most likely to be correct.

Required output format:
Final Answer: YES or NO
Confidence: integer from 1 to 5
Rationale: concise explanation
```
