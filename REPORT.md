# Multi-Agent Debate System for Reasoning Tasks

## 1. Methodology

In this project we implemented a multi-agent debate system to solve
reasoning questions. The system is inspired by AI debate frameworks
where multiple agents argue about a question before a final decision is
made.

The system includes three agents:

-   Debater A
-   Debater B
-   Judge

------------------------------------------------------------------------

### Phase 1 --- Initialization

Both debaters receive the question independently.\
Each debater produces an initial answer and short reasoning.

At this stage the debaters cannot see each other's answers.

------------------------------------------------------------------------

### Phase 2 --- Multi‑Round Debate

The debate continues for several rounds (3 rounds in our experiments).

Each round contains:

1.  Debater A presents an argument.
2.  Debater B responds with a counterargument.

Both agents receive the full transcript from previous rounds.

An adaptive stopping rule is implemented.\
If both agents give the same answer for two consecutive rounds, the
debate stops early.

------------------------------------------------------------------------

### Phase 3 --- Judgment

After the debate finishes, the transcript is given to the judge.

The judge produces:

-   analysis of both arguments
-   strongest arguments
-   weakest arguments
-   final verdict (YES or NO)
-   confidence score

The final answer of the system is the judge's verdict.

------------------------------------------------------------------------

## 2. Experiments

### Dataset

We used the StrategyQA dataset.

For this assignment we sampled:

100 questions

Each question requires a YES/NO answer.

------------------------------------------------------------------------

### Baseline Methods

We compare the debate system with two baseline approaches.

Direct QA\
The model answers the question directly without debate.

Self‑Consistency\
The model generates multiple answers and the final answer is chosen
using majority vote.

------------------------------------------------------------------------

### Results

  Method             Accuracy
  ------------------ ----------
  Debate Pipeline    0.53
  Direct QA          0.72
  Self Consistency   0.72

------------------------------------------------------------------------

### Discussion

The debate system achieved lower accuracy than the baseline methods.

This shows that structured debate does not always improve reasoning
performance. In some cases incorrect arguments from one debater
influenced the other debater and the judge.

Self‑consistency performed similarly to direct question answering.

------------------------------------------------------------------------

## 3. Debate Analysis

Example question:

Are kayaks used at the summit of Mount Everest?

Debater B used geographic and historical evidence to show that kayaks
are not used at the summit.\
Debater A failed to provide strong arguments in some rounds.

The judge correctly selected NO as the final answer.

------------------------------------------------------------------------

## 4. Prompt Engineering

Different prompts were designed for the debaters and the judge.

During development we improved the prompts to:

-   avoid repeating arguments
-   encourage logical reasoning
-   respond directly to the opponent's claims

This improved the clarity of the debate transcripts.

------------------------------------------------------------------------

## Appendix

Prompt templates were used for:

Debater A\
Debater B\
Judge

These prompts instruct the agents to produce structured reasoning and
clear final answers.
