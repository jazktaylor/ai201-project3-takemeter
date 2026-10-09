#!/usr/bin/env python3
"""Replace 'Recommendation' labels with 'Recommendation/Discussion' in the CSV.
Creates a backup file with .bak and prints a brief summary and line numbers changed.
"""
import csv
from pathlib import Path

CSV_PATH = Path('fl_studio_dataset.csv')
BACKUP_PATH = CSV_PATH.with_suffix('.csv.bak')

if not CSV_PATH.exists():
    raise SystemExit(f"CSV not found: {CSV_PATH}")

with CSV_PATH.open('r', newline='', encoding='utf-8') as fh:
    rows = list(csv.DictReader(fh))
    fieldnames = rows[0].keys() if rows else ['text', 'label', 'notes']

changed = []
for i, row in enumerate(rows, start=2):
    # CSV has header on line 1; data starts at line 2
    label = (row.get('label') or '').strip()
    if label == 'Recommendation':
        row['label'] = 'Recommendation/Discussion'
        changed.append((i, row.get('text', '')[:120].replace('\n', ' ')))

if changed:
    # write backup
    CSV_PATH.replace(BACKUP_PATH)
    # write new file
    with CSV_PATH.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=list(fieldnames))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Updated {len(changed)} label(s). Backup written to {BACKUP_PATH}")
    for ln, txt in changed:
        print(f"Changed line {ln}: {txt}")
else:
    print("No 'Recommendation' labels found to update.")
