# Planning: TakeMeter Project

## Community

Community chosen: r/FL_Studio

Why this community: r/FL_Studio is a focused, active subreddit for users of the FL Studio digital audio workstation. Posts cover a wide range of topics such as technical troubleshooting, plugin and sample recommendations, project showcases, production techniques, and step-by-step tutorials. This provides varied, structured discourse that I have deemed suitable for classification. Posts typically include concrete metadata (plugin names, file types, timestamps) and short descriptions of a problem or goal, which makes labels easier to define.

## Labels

The four labels I chose for r/FL_Studio posts are:

- **Help/Advice:** The author asking for assistance with a specific technical problem, troubleshooting issue, or difficulty involving for FL Studio, plugins, or project files
- **Tutorial:** The author is teaching or explaining a process for producing a specific sound, effect, technique, or workflow in FL Studio, rather than asking the community to solve a personal problem.
- **Feedback:** The author shares their own music, mix, project, or loop and explicitly seeks feedback, critique, evaluation, or reactions from the community.
- **Recommendation/Discussion:** The author asks for or provides recommendations about plugins, presets, samples, instruments, or production tools OR initiates a broader discussion/opinion about music-production choices that is not primarily a request for technical troubleshooting, a tutorial, or feedback on their own work.

 Below are two example post summaries per label (short, anonymized excerpts):

- Help/Advice — Example 1: "My project crashes when I load Serum; FL Studio freezes at 30% CPU—any ideas how to fix the buffer or plugin settings?"
- Help/Advice — Example 2: "I've lost the mixer routing in my .flp after moving samples—how can I relink files without breaking automation?"

- Tutorial — Example 1: "Step-by-step: how I sidechain a bass to a kick in FL Studio using Fruity Limiter for a punchy mix."
- Tutorial — Example 2: "Quick guide: creating a 2-step drum roll using the piano roll and pattern clips for live performance."

- Feedback — Example 1: "Here’s a 30-second mix I made—looking for feedback on low-end clarity and arrangement." 
- Feedback — Example 2: "Sharing my latest beat made with only stock FL plugins; open to critique and improvement tips." 

- Recommendation/Discussion — Example 1: "What's the best free reverb plugin for pads? Looking for something lightweight for laptop use."
- Recommendation/Discussion — Example 2: "Do people prefer template workflows or start-from-scratch for film scoring? Pros and cons?"


## Hard edge cases

 - Ambiguous posts: short posts that mix a demo with a question (e.g., "Here's my track—also how did I get this wet vocal sound?") can be ambiguous between `Feedback` and `Help/Advice`. Posts that include both a mini-tutorial and a request for plugin recommendations may blur `Tutorial` and `Recommendation`.
 - Handling strategy: apply a primary-label rule: if the post's explicit request is for help or a fix, label `Help/Advice`; if the post primarily demonstrates a finished work and asks for critique, label `Feedback`; if instructional content is the main body, prefer `Tutorial`; otherwise prefer `Recommendation` for broad opinion threads. If annotator confidence is low, flag as `uncertain` and route to a third annotator for adjudication with a short rationale. Keep `uncertain` examples in a separate set for error analysis and potential guideline refinement.


## Data collection plan

- Sources: r/FL_Studio
- Quantity: 

initial pilot: 200 examples to verify labelability and annotator agreement. 

- Underrepresentation handling: if a label is underrepresented, do the following in order:
  1. Use targeted queries/keywords and time filters to find rarer label instances (e.g., search for ".flp", "project file", "how do I", plugin names like "Serum", "Omnisphere", or "stock plugins" for Help/Advice; search for "feedback", "rate my" for Feedback).
  2. Relax filtering thresholds (allow shorter posts, include cross-posts, and include top-level comments if original post is short) while keeping annotation quality checks.
  3. Augment minority-class examples using manual paraphrase or by sampling related subthreads and verifying labels with human annotators (avoid automated label assignment).
  4. As a last resort, merge labels only if confusion is systematic and justified by annotation studies.


## Evaluation metrics

- **Macro F1-score:** primary metric to balance performance across labels regardless of class frequency.
 - **Per-class precision and recall:** to reveal which label types the model struggles with (e.g., confusing `Tutorial` and `Recommendation`).
 - **Confusion matrix:** to inspect systematic confusions (e.g., `Feedback` vs `Help/Advice`).
 - **Top-2 accuracy:** useful because posts may legitimately fit two labels (e.g., a demo that includes a tutorial segment); top-2 measures whether a correct label appears among the top two model predictions.
- **Annotator agreement (Cohen's kappa or Krippendorff's alpha):** to set a human baseline for label separability and to contextualize model performance.

Why these metrics: accuracy alone hides class imbalance and does not penalize per-class failures. Macro F1 ensures low-frequency labels are treated as important. Precision/recall let us tune for different error costs (e.g., prefer high precision for `Help/Advice` so users get reliable troubleshooting suggestions). Annotator agreement is necessary to contextualize achievable model performance.


## Definition of success

- Deployment-ready target: macro F1 ≥ 0.80 with per-major-label F1 ≥ 0.75 and no major systematic bias (e.g., consistently labeling `Feedback` when posts are actually `Help/Advice`).
- Minimal acceptable "good enough": macro F1 ≥ 0.70 with per-class F1 ≥ 0.65 for the three most common labels, plus demonstrably higher than a simple majority-class baseline and comparable to inter-annotator agreement.
- Operational constraints: the classifier should favor conservative behavior on ambiguous examples (e.g., abstain or flag for human review when prediction confidence < 0.6). For community tools, require a UI pattern that surfaces model confidence and a clear human-overrule path, and ensure automated suggestions (if provided) include sources or note when a recommendation is speculative.

These thresholds are provisional — they should be revisited after pilot annotation to measure human agreement and realistic label separability.

## AI Tool Plan

- **Label stress-testing:** Before annotating 200 examples, give an AI the finalized label definitions and the edge-case description and ask it to generate 5–10 synthetic posts that sit on the boundary between two labels (e.g., `Feedback` vs `Help/Advice`, or `Tutorial` vs `Recommendation`). Review each generated post: if you cannot consistently map the synthetic posts to a single label using your guidelines, tighten the label definitions and repeat the stress test until boundary cases are classifiable. This prevents ambiguous definitions from polluting the pilot dataset.

- **Annotation assistance:** We will use a large language model to pre-label an initial batch to speed annotation, but all pre-labeled examples will be human-reviewed before being accepted into the dataset. Suggested tool: a hosted LLM with reliability and audit logs (for example, OpenAI's API or a hosted instruction-tuned model). Track pre-label provenance by storing metadata fields for each example: `prelabeled_by` (tool name and model version), `prelabel_confidence` (model score or softmax probability when available), and `prelabel_date`. Maintain a separate CSV/JSONL column `human_reviewed` (boolean) and `reviewer_id` to document human verification.

- **Failure analysis:** After training a baseline model, give the list of wrong predictions (and their context) to an AI tool and ask it to identify error patterns and plausible root causes. Ask the AI to surface recurring features (keywords, post length, plugin mentions, presence of links/media, multi-intent posts, or sarcastic/informal language) and hypothesize why the model failed. Verify patterns by sampling flagged examples manually and computing simple statistics (error rates by post length, by presence of plugin names, or by label pair confusions). Use findings to refine preprocessing, augmentation, or annotation guidelines.

These AI-supported steps are intended to accelerate labeling and insight while keeping humans in the loop for quality control and disclosure.

---

## AI Usage — Pre-labeling Completed

- **Tool used:** A local Python pre-labeling script (`label_fl_studio.py`) implementing the label definitions and the primary-label rule from the **Hard edge cases** section.
- **What it did:** Pre-labeled the 200 previously unlabeled `text` examples in `fl_studio_dataset.csv` with exactly one of the four labels: `Help/Advice`, `Tutorial`, `Feedback`, or `Recommendation`. The script also appended notes for ambiguous cases using the primary-label rule.
- **Counts:** 200 examples labeled; 30 cases flagged as ambiguous and annotated in the `notes` column with a short rationale (e.g., "Ambiguous between X and Y. Applied primary-rule: X.").
- **Files created/modified:**
  - `label_fl_studio.py` — the pre-labeling script used for the pilot.
  - `fl_studio_dataset.csv` — updated in-place: `label` column populated for all 200 rows; `notes` column populated for ambiguous cases.
- **Limitations & deviations from original plan:**
  - The pilot used a deterministic, keyword-heuristic script rather than an LLM model. Per the original plan, the intent was to use an AI model with provenance fields (`prelabeled_by`, `prelabel_confidence`, `prelabel_date`). Those metadata fields were not added by the script; consider adding them if provenance is required.
  - A handful of short/mixed-intent posts were flagged as ambiguous (30); these require human review to resolve or to be moved into an `uncertain` set for adjudication.
- **Recommended next steps (human-in-the-loop):**
  1. Human-review the 30 ambiguous rows (filter `notes` for "Ambiguous") and confirm or correct the assigned label.
  2. Optionally add provenance metadata columns (`prelabeled_by`, `prelabel_confidence`, `prelabel_date`, `human_reviewed`, `reviewer_id`) to the CSV so future automation is auditable.
  3. If desired, re-run an LLM-based stress-test (as in the plan) on the ambiguous examples to produce more targeted synthetic boundary cases and help refine keyword heuristics or guidelines.

These AI-supported steps are intended to accelerate labeling and insight while keeping humans in the loop for quality control and disclosure.


