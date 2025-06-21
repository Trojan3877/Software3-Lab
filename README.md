# Software3-Lab
Software3-lab Shows how fine-tuning, RAG, and model-generated code can replace classic imperative logic.

# 🧬 Software3-Lab

![Project](https://img.shields.io/badge/Project-Software%203.0-darkviolet?style=for-the-badge)
![Build](https://github.com/Trojan3877/Software3-Lab/actions/workflows/ci.yml/badge.svg?style=for-the-badge)
![Coverage](https://codecov.io/gh/Trojan3877/Software3-Lab/branch/main/graph/badge.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Rust](https://img.shields.io/badge/Rust-1.78-orange?style=for-the-badge&logo=rust)
![Java](https://img.shields.io/badge/Java-17-red?style=for-the-badge&logo=openjdk)
![C++](https://img.shields.io/badge/C%2B%2B-17-lightgrey?style=for-the-badge&logo=c%2B%2B)
![Docker](https://img.shields.io/badge/Docker-enabled-blue?style=for-the-badge&logo=docker)
![K8s](https://img.shields.io/badge/Kubernetes-Helm-informational?style=for-the-badge&logo=kubernetes)
![Terraform](https://img.shields.io/badge/Terraform-EKS-critical?style=for-the-badge&logo=terraform)
![Ansible](https://img.shields.io/badge/Ansible-Automation-red?style=for-the-badge&logo=ansible)

> **Software 3.0 = data + model > code**  
> This lab is a sandbox for building, fine-tuning, evaluating, and shipping ML-driven “code-as-data” systems—complete with MLOps, multi-language extensions, and cost / performance telemetry.

---
![Software-3-Lab Flow-chart](docs/flowchart.png)

## 🌟 Key Objectives
1. **Fine-Tuning Loop** – Collect user feedback ➞ generate JSONL ➞ automate OpenAI / LoRA fine-tunes.  
2. **Evaluation Harness** – Regression tests that treat the model as code (Rouge / BLEU / Pass@k).  
3. **Multi-Language Extensions** –  
   - **Rust**: high-perf token counters + embedding utils  
   - **Java**: strict type-safe prompt template engine  
   - **C++**: vector-similarity & math kernels  
4. **MLOps** – Docker, Helm, Terraform (EKS), Ansible rollout; metrics logged to Snowflake; SageMaker for heavy training.  

---

## 📂 Repository Structure

Software3-Lab/
├── pipelines/
│ ├── collect_feedback.py # Python
│ ├── fine_tune.py
│ ├── evaluate.py
│ └── registry.json
├── prompts/
│ └── summarizer_prompt.txt
├── rust/
│ └── tokenizer/src/lib.rs # Cargo crate
├── java/
│ └── template-engine/src/... # Maven project
├── cpp/
│ ├── vector_math.cpp
│ └── libvector.so
├── infra/
│ ├── helm/software3-lab/
│ ├── terraform/
│ └── ansible/deploy.yml
├── tests/
│ └── eval_suite.py
├── Dockerfile
├── requirements.txt
├── docs/
│ ├── architecture.md
│ ├── metrics.md
│ └── flowchart.png
└── README.md
---

## 🚀 Quick Start

```bash
git clone https://github.com/Trojan3877/Software3-Lab.git
cd Software3-Lab
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Build Rust crate
cd rust/tokenizer && cargo build --release && cd ../../

# Compile C++ lib
g++ -O3 -shared -std=c++17 -fPIC cpp/vector_math.cpp -o cpp/libvector.so
