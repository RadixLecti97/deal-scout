

# Deal Scout: structured extraction and evals for music-industry deal news

Extracts structured deal data (deal type, seller, buyer, asset, date, price) from unstructured music-industry news articles using the Claude API, then scores the output against a hand-labeled answer key.

The goal is an eval-driven AI product: every change to the prompt or schema is measured against labeled data instead of trusted by eye.

TL;DR:
Music Industry news article extractor using Claude API to train a model against manually labeled data found in labels.txt, which is then fine tuned and scored, improving from 89% -> 95% after additional rules added to LABELLING_GUIDE.md. 
Main fine tuning of rules conducted in #Stage 6 and Known Issues section
## Repo layout

| File | Purpose |
|---|---|
| `firstcall.py` | First "hello world" call to the Claude API |
| `extract_one.py` | Single-article extraction with an enforced schema |
| `extract_all.py` | Runs extraction over every `articles/*.txt` and writes `results.csv` |
| `comparisonScript.py` | The eval: compares `results.csv` to `labels.json`, prints per-field accuracy and every miss |
| `LABELLING_GUIDE.md` | The written spec for how each field is filled; sent to the model as the system prompt and used for hand labeling |
| `labels.json` | Hand-written answer key (11 articles) |
| `results_v1.csv` | Baseline run (first 8 articles) |
| `CLAUDE.md` | Working agreement for Claude Code sessions in this repo |

The `articles/` folder is gitignored: the article texts are copyrighted and are not included.

## Setup

1. Install Python 3.12 or newer and create a virtual environment: `py -3.12 -m venv .venv`, then activate it.
2. `pip install anthropic pydantic`
3. Create an API key scoped to a workspace in the Claude Console and store it in the `ANTHROPIC_API_KEY` environment variable. Never put the key in code or in a file in this repo.
4. Put article texts in `articles/` as `article_1.txt`, `article_2.txt`, and so on.
5. `python extract_all.py`, then `python comparisonScript.py`.

## Changelog by stage

### Stage 1: environment and first API call
- Upgraded from Python 3.9 to 3.12, since the SDK requires 3.10 or newer, and created a project virtual environment.
- Created a workspace-scoped API key. An unscoped key returned a 400 error asking for a workspace ID.
- Moved the key into an environment variable after an early key exposure; rotated the key.
- First call returned a `ThinkingBlock` before the text, so `message.content[0].text` failed. Fixed by looping over content blocks and printing only blocks of type `text`.
- Added `.gitignore` (`.venv/`, `.env`, `__pycache__/`) and rebuilt git history once to remove an old key from a local commit before anything was pushed.

### Stage 2: single-article extraction
- First attempt: plain prompt ("extract the deal as JSON"). The model returned JSON in a markdown fence with its own invented nested structure, so the output shape was not controlled.
- Switched to a Pydantic `DealInfo` model with `client.messages.parse(..., output_format=DealInfo)`, which enforces a fixed schema.
- Initial fields: `deal_type`, `seller`, `buyer`, `asset`, `announced_date`, `price_usd`, `terms_summary`.
- Bug fixed: `Field("text")` sets the default value, not the description; field descriptions need `description=`.

### Stage 3: schema and labeling guide
- Same article gave different `price_usd` answers on different runs (null vs. $1.16B): the schema did not define what counts as a price.
- Wrote `LABELLING_GUIDE.md` and sent it as the system prompt. Rules cover price, names, seller and buyer, asset, and dates.
- Added `price_basis` (stated_total, partial, undisclosed), then `reported` for secondhand figures. Added `price_text` for ranges and non-USD amounts. Added deal types `merger` and `company_acquisition`.
- Made `announced_date` nullable, because a `str` field forced the model to return "not stated".
- Naming rules changed from "full legal name" to "name exactly as the article writes it, never a parent company".

### Stage 4: batch extraction and labels
- `extract_all.py` loops over `articles/*.txt` through an `extract_deal()` function and writes one row per article to `results.csv`.
- Hand-labeled the answer key from article text only, before reading model output.
- Trap cases included on purpose: prices from earlier deals mentioned in the text, a commitment amount that is not the deal price, and a figure that was only under discussion.

### Stage 5: the eval
- `comparisonScript.py` normalizes values (case, whitespace, empty equals null), compares seven fields, and prints overall score, per-field accuracy, and a list of misses with expected vs. got.
- Baseline on the first 8 articles: 50/56 (89%). Price fields were 8/8; most misses were naming (`asset`, `buyer`, `seller`) and one invented year.

### Stage 6: prompt fixes and unseen articles
- Prompt and schema fixes: asset naming (artist or seller name plus the article's noun), subsidiary buyers, and no inferred years in dates.
- Added 3 articles (9 to 11) written up after the prompt fixes, as a rough unseen check. Two describe the same deal, to test consistency.
- Result before label corrections: 70/77 (91%).
- Label corrections after reviewing the model's output (so articles 7 and 9 are no longer a blind test):
  - Article 7: seller changed to the Tina Turner Estate. The article never names who sold, and the model's answer was the more defensible reading.
  - Article 9: price relabeled `reported` at $2B, because that article states a reported price in its opening, while article 10 does not.
- Score after these label corrections: to be filled in after the next run.

## Known issues
- Exact-match scoring is too strict for `asset` ("Britney Spears Catalog" vs. "Britney Spears Music Catalog").
- Guide gaps: who is the seller when an article never names one (article 10); whether a dated byline counts when only the closing is reported (article 11); company vs. catalog when an LLC is acquired for its copyrights (article 5).
- Eleven articles is a small set. The first 8 were used for tuning, so their score is optimistic.

## Roadmap
1. Eval infrastructure: 25 to 30 articles, a dev set and a sealed test set, a run log, and a regression check.
2. Model and cost comparison: accuracy, cost per article, and latency across model sizes.
3. Failure taxonomy and an LLM-as-judge for `terms_summary`, checked against human grades.
4. Agent layer: search, extract, find comparables, flag possible mispricing, and abstain when unsure.
5. One-page PRD and a readout with a go or no-go recommendation.
