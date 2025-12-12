# 🚀 Software3-Lab — LLM-Augmented AI Control Plane

![Python](https://img.shields.io/badge/Python-3.10-blue)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-blue)
![LangChain](https://img.shields.io/badge/LangChain-MCP-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![CI](https://github.com/Trojan3877/Software3-Lab/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

**Software3-Lab** is a **production-style AI system** that combines:

- Classical Machine Learning
- Experiment tracking (MLflow)
- LLM-based orchestration (GPT-4)
- Model Control Plane (MCP) architecture
- FastAPI service layer
- CI/CD + Docker parity

This project demonstrates **how modern AI systems are actually built in industry**.

---

## 🧠 Architecture Overview
User / API Request ↓ FastAPI Service ↓ LLM MCP Agent (GPT-4) ↓ LangChain Tools ↓ ML Training / Evaluation ↓ MLflow Metrics & Artifacts

---
---

## 🧩 Key Components

### 1. Machine Learning Layer
- Algorithm: Logistic Regression
- Dataset: Iris
- Framework: Scikit-learn
- Metrics logged via MLflow

### 2. LLM Model Control Plane (MCP)
- LLM: GPT-4
- Framework: LangChain
- Pattern: Tool-based orchestration
- Separation of reasoning and execution

### 3. API Layer
- Framework: FastAPI
- Swagger UI enabled
- Safe, auditable LLM execution

### 4. Experiment Tracking
- MLflow for parameters, metrics, and models
- Reproducible experiments
- CI-validated training

---

## 🔧 Tech Stack

| Layer | Technology |
|----|----|
| ML | Scikit-learn |
| LLM | GPT-4 |
| MCP | LangChain |
| Tracking | MLflow |
| API | FastAPI |
| CI/CD | GitHub Actions |
| Container | Docker |
| Language | Python 3.10 |

---

## 📊 Metrics & Evaluation

Detailed performance metrics, experiment logs, and system evaluation are available in:

➡ **[`Metrics.md`](Metrics.md)**

---
docker build -t software3-lab .
docker run -p 8000:8000 software3-lab


## ▶️ How to Run

### Local
```bash
pip install -r requirements.txt
uvicorn src.api:app --reload
http://localhost:8000/docs

Future Enhancements

RAG over experiment history

Model registry promotion

Performance regression alerts

Multi-agent orchestration
