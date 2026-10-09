#!/usr/bin/env python3
"""Fix common label misspellings in fl_studio_dataset.csv.

Replaces exact occurrences of 'Recommedation/Discussion' with
'Recommendation/Discussion'. Creates a timestamped backup before
overwriting the CSV.
"""
from pathlib import Path
from datetime import datetime


def main():
    repo_root = Path(__file__).resolve().parents[1]
    csv_path = repo_root / "fl_studio_dataset.csv"
    if not csv_path.exists():
        print(f"ERROR: {csv_path} not found")
        return 2

    text = csv_path.read_text(encoding="utf-8")
    old = "Recommedation/Discussion"
    new = "Recommendation/Discussion"
    count = text.count(old)
    if count == 0:
        print("No occurrences of typo found. Nothing to do.")
        return 0

    # backup
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    bak_path = repo_root / f"fl_studio_dataset.csv.bak.{ts}"
    bak_path.write_text(text, encoding="utf-8")

    new_text = text.replace(old, new)
    csv_path.write_text(new_text, encoding="utf-8")

    print(f"Replaced {count} occurrence(s) of '{old}' with '{new}'.")
    print(f"Backup written to: {bak_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
