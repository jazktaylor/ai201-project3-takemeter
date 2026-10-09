#!/usr/bin/env python3
import csv
from pathlib import Path

INPUT = Path('fl_studio_dataset.csv')
OUTPUT = Path('fl_studio_dataset_cleaned.csv')

# Known label tokens used to detect the label column reliably
KNOWN_LABELS = [
    'Help/Advice', 'Recommendation', 'Feedback', 'Tutorial'
]
# sort by length descending to prefer longer matches first
KNOWN_LABELS.sort(key=lambda s: -len(s))


def find_closing_quote(s, start=0):
    i = start + 1
    while i < len(s):
        if s[i] == '"':
            # escaped quote "" -> skip both
            if i + 1 < len(s) and s[i+1] == '"':
                i += 2
                continue
            return i
        i += 1
    return -1


def split_unquoted_line(line):
    # Try to find a known label by searching from right for ',<label>,' or ',<label>' at end
    for label in KNOWN_LABELS:
        token = ',' + label + ','
        pos = line.rfind(token)
        if pos != -1:
            text = line[:pos]
            rest = line[pos+1:]
            parts = rest.split(',', 1)
            lbl = parts[0].strip()
            notes = parts[1].strip() if len(parts) > 1 else ''
            return text.strip(), lbl, notes
        # check ending with ',label' (no trailing notes)
        token2 = ',' + label
        if line.endswith(token2):
            text = line[: -len(token2)]
            return text.strip(), label, ''
    # fallback: split into 3 parts (first two commas)
    parts = line.split(',', 2)
    if len(parts) == 3:
        return parts[0].strip(), parts[1].strip(), parts[2].strip()
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip(), ''
    return line.strip(), '', ''


rows = []
with INPUT.open('r', encoding='utf-8', newline='') as f:
    lines = f.readlines()

if not lines:
    raise SystemExit('empty input')

header = lines[0].rstrip('\n')
idx = 1
n = len(lines)

while idx < n:
    line = lines[idx].rstrip('\n')
    if not line:
        idx += 1
        continue
    # quoted text starting line
    if line.lstrip().startswith('"'):
        buf = line
        closing = find_closing_quote(buf, 0)
        while closing == -1:
            idx += 1
            if idx >= n:
                break
            buf += '\n' + lines[idx].rstrip('\n')
            closing = find_closing_quote(buf, 0)
        if closing == -1:
            # malformed, treat whole buffer as text
            text = buf.strip('"')
            rows.append((text, '', ''))
            idx += 1
            continue
        # extract text between first and closing quote
        text = buf[1:closing]
        rest = buf[closing+1:].lstrip()
        if rest.startswith(','):
            rest = rest[1:]
        if rest == '':
            label = ''
            notes = ''
        else:
            # rest may contain commas; split on first comma
            parts = rest.split(',', 1)
            label = parts[0].strip()
            notes = parts[1].strip() if len(parts) > 1 else ''
        rows.append((text, label, notes))
        idx += 1
        continue

    # unquoted single-line record
    text, label, notes = split_unquoted_line(line)
    rows.append((text, label, notes))
    idx += 1

# write cleaned CSV
with OUTPUT.open('w', encoding='utf-8', newline='') as out:
    writer = csv.writer(out, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['text', 'label', 'notes'])
    for t, l, n_ in rows:
        writer.writerow([t, l, n_])

# quick verification (best-effort)
try:
    import pandas as pd
    df = pd.read_csv(OUTPUT)
    print('ok rows=', len(df))
except Exception as e:
    print('verify failed:', e)
    print('wrote', OUTPUT)
