# Contributing to Software-3.0 Lab

First off, thanks for taking the time to contribute!  
This project demonstrates production-grade “Software 3.0” practices, so code quality and reproducibility matter.

## 1 – Development Quick Start

```bash
git clone https://github.com/Trojan3877/Software3-Lab.git
cd Software3-Lab
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
make build-rust build-cpp
make test   # all green? you’re ready!
