#!/usr/bin/env python3
"""
update_metrics_table.py
─────────────────────────────────────────────────────────────────────────────
Scan data/eval/results/*.json, sort by timestamp DESC, and rebuild the
markdown table inside docs/metrics.md.

Table region is delimited by:

<!-- METRICS-TABLE:START -->
… (generated rows) …
<!-- METRICS-TABLE:END -->

Run manually or via GitHub Actions.
"""

import json
from pathlib import Path
from datetime import datetime

RESULTS_DIR = Path("data/eval/results")
MD_PATH = Path("docs/metrics.md")

START_TAG = "<!-- METRICS-TABLE:START -->"
END_TAG = "<!-- METRICS-TABLE:END -->"


def load_results():
    rows = []
    for f in RESULTS_DIR.glob("*.json"):
        data = json.loads(f.read_text())
        ts = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        rows.append((
            ts,
            data["model"],
            data["rougeL"],
            data["bleu4"],
            data["pass@3"],
            data["num_samples"],
        ))
    return sorted(rows, key=lambda r: r[0], reverse=True)


def build_table(rows):
    header = "| Timestamp (UTC) | Model | Rouge-L | BLEU-4 | Pass@3 | #Samples |\n" \
             "|-----------------|-------|---------|--------|--------|----------|\n"
    body = "\n".join(
        f"| {r[0].strftime('%Y-%m-%d %H:%M')} | `{r[1]}` | **{r[2]:.2f}** | "
        f"**{r[3]:.2f}** | **{r[4]:.2f}** | {r[5]} |"
        for r in rows
    )
    return header + body + "\n"


def inject_table(md_text, table_md):
    if START_TAG not in md_text or END_TAG not in md_text:
        raise RuntimeError("Metrics tags not found in docs/metrics.md")
    pre, _middle, post = md_text.partition(START_TAG)
    _junk, _table, post = post.partition(END_TAG)
    return f"{pre}{START_TAG}\n{table_md}{END_TAG}{post}"


def main():
    rows = load_results()
    table_md = build_table(rows)

    md = MD_PATH.read_text()
    new_md = inject_table(md, table_md)

    if new_md != md:
        MD_PATH.write_text(new_md)
        print("✅ docs/metrics.md updated.")
    else:
        print("No changes detected; table already up-to-date.")


if __name__ == "__main__":
    main()
