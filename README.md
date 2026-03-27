# Daily Papers

Daily aggregation and AI-powered summaries (EN/KO) of new papers from arXiv, Interspeech, ICASSP, IEEE, and ACL.

## Quick Start (Fork & Deploy)

1. **Fork** this repo
2. Go to **Settings → Secrets → Actions** → add `OPENAI_API_KEY`
3. Go to **Settings → Pages** → Source: `Deploy from a branch` → Branch: `gh-pages` / `/ (root)`
4. Go to **Actions** → `Daily Paper Build` → **Run workflow**

Your site will be live at `https://<username>.github.io/daily_archive/` and auto-update daily at 06:00 KST.

## Custom Categories

By default, papers are fetched from: `cs.AI`, `cs.CL`, `cs.SD`, `eess.AS`, `cs.LG`, `cs.CV`.

To customize, go to **Settings → Variables → Actions** → add `ARXIV_CATEGORIES` with comma-separated values:

```
cs.CL,cs.SD,eess.AS
```

Available categories: `cs.AI`, `cs.CL`, `cs.SD`, `eess.AS`, `cs.LG`, `cs.CV`, `cs.CR`, `cs.DB`, `cs.DC`, `cs.DS`, `cs.GT`, `cs.HC`, `cs.IR`, `cs.IT`, `cs.LO`, `cs.MA`, `cs.NE`, `cs.NI`, `cs.PL`, `cs.RO`, `cs.SE`, `cs.SI`, `cs.SY`, `eess.SP`, `stat.ML`, `math.OC`, and more from [arXiv](https://arxiv.org/category_taxonomy).

## Local Usage

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
export ARXIV_CATEGORIES="cs.CL,cs.SD"  # optional
python scripts/run_daily.py
```

Open `site/index.html` in your browser.
