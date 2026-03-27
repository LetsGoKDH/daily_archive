# Daily Papers

Daily aggregation and AI-powered summaries (EN/KO) of new papers from arXiv, Interspeech, ICASSP, IEEE, and ACL.

## Usage

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
python scripts/run_daily.py
```

Open `site/index.html` in your browser.

## Automation

GitHub Actions runs daily at 06:00 KST. Add `OPENAI_API_KEY` to repository secrets.
