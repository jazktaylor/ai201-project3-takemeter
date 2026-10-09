import re
import pandas as pd

CSV_PATH = 'fl_studio_dataset.csv'

HELP_KW = [
    r"how do i",
    r"how do you",
    r"how can i",
    r"how to fix",
    r"help",
    r"any ideas",
    r"crash",
    r"fix",
    r"error",
    r"can't",
    r"cannot",
    r"lost",
    r"troubleshoot",
    r"issue",
    r"problem",
]

TUTORIAL_KW = [
    r"step",
    r"step-by-step",
    r"tutorial",
    r"guide",
    r"here's how",
    r"walkthrough",
    r"quick guide",
    r"how to",
]

FEEDBACK_KW = [
    r"feedback",
    r"rate my",
    r"critique",
    r"what do you think",
    r"any tips",
    r"thoughts",
    r"how's this",
    r"looking for feedback",
    r"open to critique",
]

RECOMMEND_KW = [
    r"recommend",
    r"what's the best",
    r"which plugin",
    r"suggest",
    r"suggestions",
    r"recommendations",
    r"do people prefer",
    r"looking for",
]

def score_text(text):
    t = text.lower()
    scores = {"Help/Advice":0, "Tutorial":0, "Feedback":0, "Recommendation/Discussion":0}
    for p in HELP_KW:
        if re.search(p, t):
            scores['Help/Advice'] += 1
    for p in TUTORIAL_KW:
        if re.search(p, t):
            scores['Tutorial'] += 1
    for p in FEEDBACK_KW:
        if re.search(p, t):
            scores['Feedback'] += 1
    for p in RECOMMEND_KW:
        if re.search(p, t):
            scores['Recommendation/Discussion'] += 1
    return scores

def pick_label(scores):
    # Return top label and second label
    items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return items[0], items[1]

def is_ambiguous(text, top, second):
    # Ambiguous if both scores >0 and close, or text short and contains multiple intents
    if top[1] == 0:
        return False
    if second[1] == 0:
        return False
    if top[1] - second[1] <= 1:
        return True
    # short mixed posts heuristics
    if len(text.split()) < 30 and ('here' in text.lower() or "track" in text.lower()) and ('how' in text.lower() or 'help' in text.lower() or 'tutorial' in text.lower()):
        return True
    return False

def main():
    df = pd.read_csv(CSV_PATH)
    if 'notes' not in df.columns:
        df['notes'] = ''
    changed = 0
    ambiguous_count = 0
    for idx, row in df[df['label'].isna() | (df['label'].astype(str).str.strip() == '')].iterrows():
        text = '' if pd.isna(row.get('text')) else str(row.get('text'))
        if not text.strip():
            # default to Recommendation if empty (rare), and note
            df.at[idx, 'label'] = 'Recommendation'
            df.at[idx, 'notes'] = (row.get('notes') or '') + 'Empty text; defaulted to Recommendation.'
            changed += 1
            continue
        scores = score_text(text)
        top, second = pick_label(scores)
        label = top[0]
        ambiguous = is_ambiguous(text, top, second)
        if ambiguous:
            ambiguous_count += 1
            note = f"Ambiguous between {top[0]} and {second[0]}. Applied primary-rule: {top[0]}." 
            existing = row.get('notes') if not pd.isna(row.get('notes')) else ''
            df.at[idx, 'notes'] = (existing + ' ' + note).strip()
        # As fallback, if no keyword matched, try heuristics
        if top[1] == 0:
            # heuristics: presence of 'my track' or 'here's my' => Feedback
            low = text.lower()
            if "my track" in low or "here's my" in low or "heres my" in low or "posted" in low or "mix" in low or "song" in low:
                label = 'Feedback'
            elif 'how' in low or 'help' in low or 'fix' in low or 'error' in low or 'crash' in low:
                label = 'Help/Advice'
            elif 'step' in low or 'tutorial' in low or 'guide' in low:
                label = 'Tutorial'
            else:
                label = 'Recommendation/Discussion'
        df.at[idx, 'label'] = label
        changed += 1

    df.to_csv(CSV_PATH, index=False)
    print(f"Labeled {changed} examples; flagged {ambiguous_count} ambiguous cases. Updated {CSV_PATH}.")

if __name__ == '__main__':
    main()
