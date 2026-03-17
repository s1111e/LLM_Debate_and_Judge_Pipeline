# LLM Debate and Judge Pipeline

This project implements a **multi-agent debate framework** using Large Language Models (LLMs) to improve reasoning on complex questions.

 Project Webpage:  
https://s1111e.github.io/LLM_Debate_and_Judge_Pipeline/

 Full Report:  
[Click here to read the report](./report.md)

---

## Overview

The system consists of three agents:

- Debater A → argues YES  
- Debater B → argues NO  
- Judge → selects the stronger argument  

---

## Results

| Method | Accuracy |
|------|------|
| Debate | 0.48 |
| Direct QA | 0.74 |
| Self Consistency | 0.74 |

---

## How to Run

python experiments/run_debate.py
python experiments/run_direct_qa.py
python experiments/run_self_consistency.py

---

## Links

-  Webpage: https://s1111e.github.io/LLM_Debate_and_Judge_Pipeline/
-  Report: ./report.md
