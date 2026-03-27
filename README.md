# Daily Papers

Daily aggregation and AI-powered summaries (EN/KO) of new papers from arXiv, Interspeech, ICASSP, IEEE, and ACL.

## Quick Start (Fork & Deploy)

1. **Fork** this repo
2. Go to **Settings → Secrets → Actions** → add `OPENAI_API_KEY`
3. Go to **Settings → Pages** → Source: `Deploy from a branch` → Branch: `gh-pages` / `/ (root)`
4. Go to **Actions** → `Daily Paper Build` → **Run workflow**

Your site will be live at `https://<username>.github.io/daily_archive/` and auto-update daily at 06:00 KST.

## Local Usage

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
python scripts/run_daily.py
```

Open `site/index.html` in your browser.
