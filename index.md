<div align="center">

# Multi-Agent Debate for StrategyQA

### Evaluating Multi-Agent Reasoning with LLM Debate

</div>

---

## Table of Contents

1. Methodology
2. Experiments
3. Analysis
4. Prompt Engineering
5. Appendix: Full Prompts

---

# 1. Methodology

## System Architecture

The system implements a **multi-agent debate pipeline** consisting of three agents:

* Debater A
* Debater B
* Judge

The architecture follows a four-phase reasoning pipeline.

<p align="center">
<img src="figures/architecture.png" width="600">
</p>

Pipeline flow:

```
Question
   ↓
Initial Answers
   ↓
Debate Rounds
   ↓
Judge Evaluation
   ↓
Final Prediction
```

## Debate Protocol

Each debate proceeds as follows:

1. Both agents generate **initial answers**.
2. Agents respond to the opponent’s argument.
3. Debate continues for multiple rounds.
4. A judge evaluates the full debate transcript.

### Adaptive Stopping

To reduce unnecessary computation, the debate stops early when both agents converge to the same answer for two consecutive rounds.

## Model Configuration

Experiments are configured through:

```
config/config.yaml
```

Parameters include:

* number of debate rounds
* model temperature
* self-consistency samples

---

# 2. Experiments

## Experimental Setup

Three reasoning approaches are evaluated:

1. Debate Pipeline
2. Direct Question Answering
3. Self Consistency

All systems are evaluated on **100 StrategyQA questions**.

Results are logged for reproducibility.

```
logs/debate_results.json
logs/direct_qa_results.json
logs/self_consistency_results.json
```

---

## Results

<div align="center">

| Method           | Accuracy |
| ---------------- | -------- |
| Debate Pipeline  | 0.54     |
| Direct QA        | 0.72     |
| Self Consistency | 0.72     |

</div>

<p align="center">
<img src="figures/results_chart.png" width="500">
</p>

Direct QA and Self-Consistency outperform the debate pipeline in our experiments.

This suggests that debate-based reasoning may introduce additional reasoning errors.

---

# 3. Analysis

To understand the behavior of the debate system, we analyze several debate transcripts.

## Successful Case

**Question**

Are kayaks used at the summit of Mount Everest?

Debater B correctly explains that the summit contains no bodies of water and therefore kayaks cannot be used.

The judge concludes:

**NO**

This demonstrates that debate works well when one agent provides strong factual reasoning.

---

## Failure Case

**Question**

Can Aerosmith fit in a 2020 Mitsubishi Outlander?

Both agents incorrectly focused on cargo capacity and equipment size.

The debate introduced several incorrect assumptions, causing the judge to rely on flawed reasoning.

This illustrates a key weakness of debate systems.

---

## Relation to Debate Research

Irving et al. (2018) proposed debate as a mechanism for improving reasoning transparency in AI systems.

In theory, debate should expose incorrect reasoning through adversarial arguments.

However, our results show that debate may fail when both agents rely on incorrect assumptions.

---

# 4. Prompt Engineering

The system uses **role-based prompting** to simulate debate.

Three prompt types are used:

* Debater prompts
* Judge prompts
* Baseline prompts

## Debater Prompt

Debaters are instructed to provide structured reasoning and respond to opponent arguments.

```
You are Debater A.

Answer the question with YES or NO and provide reasoning.

Question:
{question}

Debate transcript:
{transcript}

Provide your argument for round {round_number}.
```

## Judge Prompt

The judge evaluates the entire debate transcript.

```
You are the judge of a debate.

Analyze the arguments from both debaters.

Question:
{question}

Debate transcript:
{transcript}

Return YES or NO.
```

Prompts were iteratively refined to encourage consistent output formats.

---

# Appendix: Full Prompts

<details>
<summary>Debater Prompt</summary>

```
You are Debater {A or B}.

Answer the question with YES or NO and provide reasoning.

Question:
{question}

Debate transcript:
{transcript}

Provide your argument for round {round_number}.
```

</details>

---

<details>
<summary>Judge Prompt</summary>

```
You are the judge of a debate.

Analyze the arguments from both debaters.

Question:
{question}

Debate transcript:
{transcript}

Return YES or NO.
```

</details>

---

<details>
<summary>Direct QA Prompt</summary>

```
Answer the following question with YES or NO.

Question:
{question}
```

</details>

---

<details>
<summary>Self Consistency Prompt</summary>

```
Answer the following question with YES or NO.

Question:
{question}
```

</details>
