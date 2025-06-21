"""
evaluate.py
────────────────────────────────────────────────────────────────────────────
Run an automated evaluation suite against the latest fine-tuned model
registered in `pipelines/registry.json`.

Metrics computed
----------------
• Rouge-L  (summarization / free-form)
• BLEU-4   (translation-style n-gram match)
• Pass@k   (code-generation success rate) – simple heuristic

Input data
----------
`data/eval/benchmark.jsonl` with JSON lines:
{
  "prompt": "...",
  "expected": "...",      # ground-truth or reference
  "type": "text" | "code" # determines which metric bucket
}

Environment
-----------
OPENAI_API_KEY           (for calling the fine-tuned model)
"""

import json
import os
from pathlib import Path
from typing import List, Dict

import nltk
from rouge_score import rouge_scorer
import openai

REGISTRY_PATH = Path("pipelines/registry.json")
BENCHMARK_PATH = Path("data/eval/benchmark.jsonl")
RESULTS_DIR = Path("data/eval/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

nltk.download("punkt", quiet=True)  # for BLEU tokenizer

# ---------------------------------------------------------------------------- #
# Helper functions
# ---------------------------------------------------------------------------- #
def _latest_model() -> str:
    registry: List[Dict] = json.loads(REGISTRY_PATH.read_text())
    latest = registry[-1]["result_model"]
    if latest == "pending":
        raise RuntimeError("Latest fine-tune not finished yet.")
    return latest


def _load_benchmark() -> List[Dict]:
    with BENCHMARK_PATH.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def _call_model(model: str, prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    return response.choices[0].message.content.strip()


# ---------------------------------------------------------------------------- #
# Metric calculators
# ---------------------------------------------------------------------------- #
scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)


def rouge_l(ref: str, hyp: str) -> float:
    return scorer.score(ref, hyp)["rougeL"].fmeasure


def bleu4(ref: str, hyp: str) -> float:
    ref_tokens = [nltk.word_tokenize(ref.lower())]
    hyp_tokens = nltk.word_tokenize(hyp.lower())
    return nltk.translate.bleu_score.sentence_bleu(ref_tokens, hyp_tokens)


def pass_at_k(pred: str, exp: str, k: int = 3) -> int:
    """Very lightweight heuristic: success if expected substring appears."""
    return int(exp.strip() in pred.strip())


# ---------------------------------------------------------------------------- #
# Main evaluation loop
# ---------------------------------------------------------------------------- #
def run_eval():
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY missing")

    model = _latest_model()
    dataset = _load_benchmark()

    rouge_scores, bleu_scores, pass_scores = [], [], []
    for item in dataset:
        pred = _call_model(model, item["prompt"])

        if item["type"] == "text":
            rouge_scores.append(rouge_l(item["expected"], pred))
            bleu_scores.append(bleu4(item["expected"], pred))
        else:  # code
            pass_scores.append(pass_at_k(pred, item["expected"], k=3))

    metrics = {
        "model": model,
        "rougeL": sum(rouge_scores) / max(1, len(rouge_scores)),
        "bleu4": sum(bleu_scores) / max(1, len(bleu_scores)),
        "pass@3": sum(pass_scores) / max(1, len(pass_scores)),
        "num_samples": len(dataset),
    }

    # Save results JSON
    out_path = RESULTS_DIR / f"eval-{model.replace(':', '_')}.json"
    out_path.write_text(json.dumps(metrics, indent=2))
    print(f"✅ Eval complete → {out_path}")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    run_eval()
