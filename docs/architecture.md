# 🏗️ Software-3.0 Lab — System Architecture

> **Mission**: Prove that in “Software 3.0” the **data & model** _are_ the code.  
> Fine-tune, evaluate, and ship models with full MLOps rigor while leveraging multi-language performance boosters.

---

## 1 – Component Map

| Layer | Language | Responsibility |
|-------|----------|----------------|
| **Fine-Tune Orchestrator** | **Python** (`pipelines/fine_tune.py`) | Merge feedback → launch OpenAI/SageMaker fine-tune → update registry |
| **Evaluation Harness** | **Python** (`pipelines/evaluate.py`) | Rouge-L, BLEU-4, Pass@3 regression; writes metrics JSON |
| **Tokenizer Utils** | **Rust + PyO3** (`rust/tokenizer`) | Ultra-fast whitespace / BPE token counts for cost estimation |
| **Vector Math** | **C++17** (`cpp/libvector.so`) | Dot product + cosine similarity for embedding analytics |
| **Prompt Template Engine (planned)** | **Java 17** | Type-safe prompt placeholders and schema validation |
| **API Layer** | **FastAPI** (Python) | Exposes evaluate results & model registry endpoints |
| **Data Store** | **Snowflake** | Stores metrics & lineage |
| **Cloud Training** | **AWS SageMaker** | Optional LoRA jobs for compute-heavy fine-tunes |

---

## 2 – Data / Execution Flow

```mermaid
flowchart TD
    U[User Feedback] --> F1[collect_feedback.py]
    F1 -->|JSONL| S[data/feedback/*.jsonl]
    S --> FT[fine_tune.py]
    FT -->|dataset.jsonl| FT_job[OpenAI / SageMaker job]
    FT_job --> R[registry.json]
    R --> EV[evaluate.py]
    benchmark[benchmark.jsonl] --> EV
    EV --> metrics(Snowflake Metrics) & J[results/*.json]
    EV --> API[FastAPI /metrics endpoint]
