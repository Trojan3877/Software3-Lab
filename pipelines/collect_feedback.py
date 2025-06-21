"""
collect_feedback.py
────────────────────────────────────────────────────────────────────────────
Collect structured user feedback (prompt, model_response, rating, comments)
and append it to a JSONL file ready for OpenAI / HuggingFace fine-tuning.

Usage (interactive CLI):
    python pipelines/collect_feedback.py

Usage (import):
    from pipelines.collect_feedback import save_feedback
    save_feedback(prompt="...", response="...", rating=4, comments="Good")

Output:
    data/feedback/2025-MM-DD.jsonl   # one JSON object per line
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional

# --------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------- #

DATA_DIR = Path("data/feedback")
DATA_DIR.mkdir(parents=True, exist_ok=True)

RATING = Literal[1, 2, 3, 4, 5]  # type alias


def _output_path() -> Path:
    """Return today's JSONL path (one file per day)."""
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    return DATA_DIR / f"{date_str}.jsonl"


# --------------------------------------------------------------------- #
# Core Function
# --------------------------------------------------------------------- #
def save_feedback(
    prompt: str,
    response: str,
    rating: RATING,
    comments: Optional[str] = None,
) -> None:
    """
    Persist feedback record as JSON line.

    JSON schema:
    {
      "timestamp": "2025-06-30T12:34:56Z",
      "prompt": "...",
      "response": "...",
      "rating": 4,
      "comments": "optional"
    }
    """
    record = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "prompt": prompt.strip(),
        "response": response.strip(),
        "rating": rating,
        "comments": comments or "",
    }

    with _output_path().open("a", encoding="utf-8") as f:
        json.dump(record, f)
        f.write("\n")

    print(f"✅ Saved feedback ({rating}/5)")


# --------------------------------------------------------------------- #
# Interactive CLI
# --------------------------------------------------------------------- #
def _interactive():
    print("📝 Enter feedback (Ctrl+C to exit)\n")
    try:
        while True:
            prompt = input("User prompt  : ").strip()
            response = input("Model answer : ").strip()
            rating = int(input("Rating (1-5) : ").strip())
            comments = input("Comments     : ").strip()

            save_feedback(prompt, response, rating, comments)
            print("-" * 40)
    except KeyboardInterrupt:
        print("\nExiting…")


if __name__ == "__main__":
    _interactive()
