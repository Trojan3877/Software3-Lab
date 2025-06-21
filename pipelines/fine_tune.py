"""
fine_tune.py
────────────────────────────────────────────────────────────────────────────
Automate the end-to-end fine-tune loop.

  1. Discover feedback JSONL files in data/feedback/
  2. Merge into data/fine_tune/dataset-<timestamp>.jsonl
  3. Call OpenAI fine-tune endpoint  (alt: SageMaker LoRA placeholder)
  4. Append new entry to pipelines/registry.json for tracking

Env vars required (OpenAI):
  OPENAI_API_KEY
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# --------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------- #
FEEDBACK_DIR = Path("data/feedback")
FINE_TUNE_DIR = Path("data/fine_tune")
REGISTRY_PATH = Path("pipelines/registry.json")
FINE_TUNE_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------- #
def _merge_feedback() -> Path:
    """Combine all feedback JSONL files into one dataset; return path."""
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    out_path = FINE_TUNE_DIR / f"dataset-{ts}.jsonl"

    with out_path.open("w", encoding="utf-8") as out_file:
        for file in FEEDBACK_DIR.glob("*.jsonl"):
            with file.open(encoding="utf-8") as f:
                for line in f:
                    out_file.write(line)
    print(f"📚 Merged dataset saved → {out_path.relative_to(Path.cwd())}")
    return out_path


def _openai_fine_tune(dataset_path: Path) -> Dict:
    """
    Spawn OpenAI fine-tune via CLI (require openai>=1.0.0).
    Returns job JSON (id, status, model).
    """
    cmd = [
        "openai",
        "api",
        "fine_tunes.create",
        "-t",
        str(dataset_path),
        "-m",
        "gpt-3.5-turbo",
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True, check=True)
    job_json = json.loads(completed.stdout)
    print(f"🚀 Launched OpenAI fine-tune job: {job_json['id']}")
    return job_json


def _update_registry(entry: Dict) -> None:
    """Add fine-tune result to registry.json."""
    registry: List[Dict] = []
    if REGISTRY_PATH.exists():
        registry = json.loads(REGISTRY_PATH.read_text())

    registry.append(entry)
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2))
    print("📑 Updated model registry.")


# --------------------------------------------------------------------- #
# Main pipeline
# --------------------------------------------------------------------- #
def run_fine_tune():
    dataset = _merge_feedback()
    job = _openai_fine_tune(dataset)

    registry_entry = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "job_id": job["id"],
        "base_model": "gpt-3.5-turbo",
        "dataset": dataset.name,
        "status": job["status"],
        "result_model": job.get("fine_tuned_model", "pending"),
    }
    _update_registry(registry_entry)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY env variable is missing")
    run_fine_tune()
