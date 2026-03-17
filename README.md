Full report: [REPORT.md](REPORT.md)

# Multi-Agent Debate System for Reasoning Tasks

This project implements a multi-agent debate framework for answering
reasoning questions using Large Language Models (LLMs).

The system simulates a structured debate between two agents and a judge
in order to evaluate whether debate improves reasoning performance.

------------------------------------------------------------------------

## System Architecture

The system contains three main agents:

-   Debater A -- proposes an answer and reasoning
-   Debater B -- challenges the argument
-   Judge -- evaluates the debate and produces the final decision

The debate process follows these steps:

1.  Both debaters generate initial answers independently.
2.  The agents exchange arguments over multiple rounds.
3.  The judge evaluates the entire transcript.
4.  The final answer is produced.

An adaptive stopping rule is used. If both agents produce the same
answer for two consecutive rounds, the debate stops early.

------------------------------------------------------------------------

## Dataset

We use the StrategyQA dataset, which contains reasoning questions that
require multi‑step thinking.

For this project we selected:

100 questions

Each question has a YES or NO ground truth answer.

------------------------------------------------------------------------

## Experiments

We compare the debate system with two baseline approaches.

### Debate Pipeline

Two agents debate and the judge decides the final answer.

### Direct QA

The LLM answers the question directly without debate.

### Self‑Consistency

The model generates multiple answers and the final answer is selected
using majority vote.

------------------------------------------------------------------------

## Experimental Results

  Method             Accuracy
  ------------------ ----------
  Debate Pipeline    0.53
  Direct QA          0.72
  Self Consistency   0.72

------------------------------------------------------------------------

## Project Structure

HW2/ │ ├── agents/ ├── debate/ ├── experiments/ ├── evaluation/ ├──
utils/ ├── config/ ├── data/ ├── logs/ ├── REPORT.md └── README.md

------------------------------------------------------------------------

## Running the Experiments

Run the debate system:

python experiments/run_debate_experiment.py

Run the direct QA baseline:

python experiments/run_direct_qa.py

Run the self-consistency baseline:

python experiments/run_self_consistency.py

Evaluate the results:

python evaluation/evaluate_accuracy.py

------------------------------------------------------------------------

## Logs

Experiment outputs are saved in the logs directory.

Examples:

logs/debate_results.json\
logs/direct_qa_results.json\
logs/self_consistency_results.json

------------------------------------------------------------------------

## Report

Detailed explanation of the methodology and experiments is available in
REPORT.md
