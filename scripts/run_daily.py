#!/usr/bin/env python3
"""Main orchestrator: fetch papers, generate summaries, build site."""

import json
import os
import sys
from datetime import date
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import DATA_DIR, MAX_PAPERS_PER_DAY
from fetchers import arxiv_fetcher
from summarizer import claude_summarizer
from builder import render


def main():
    today = date.today().isoformat()
    data_path = os.path.join(DATA_DIR, f"{today}.json")
    os.makedirs(DATA_DIR, exist_ok=True)

    # Check if already generated today
    if os.path.exists(data_path):
        print(f"[main] Loading existing data for {today}")
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        papers = data.get("papers", [])
    else:
        # 1. Fetch papers
        print(f"[main] Fetching papers for {today}...")
        papers = arxiv_fetcher.fetch(days_back=2)

        # Phase 2: add more sources here
        # s2_papers = semantic_scholar_fetcher.fetch()
        # pwc_papers = pwc_fetcher.fetch_trending()
        # papers = dedup.merge(papers, s2_papers, pwc_papers)

        # Limit total papers
        papers = papers[:MAX_PAPERS_PER_DAY]

        # 2. Generate summaries
        print(f"[main] Generating summaries for {len(papers)} papers...")
        papers = claude_summarizer.summarize_batch(papers)

        # 3. Save JSON data
        save_data(today, papers, data_path)

    # 4. Render HTML
    print(f"[main] Building site...")
    render.build_site(today, papers)

    print(f"[main] Done! Open site/index.html to view.")


def save_data(date_str, papers, data_path):
    """Save paper data to a JSON file."""
    by_category = {}
    for p in papers:
        for cat in p.get("categories", []):
            by_category[cat] = by_category.get(cat, 0) + 1

    data = {
        "date": date_str,
        "papers": papers,
        "stats": {
            "total": len(papers),
            "by_category": dict(sorted(by_category.items(), key=lambda x: -x[1])),
        },
    }

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[main] Saved {len(papers)} papers to {data_path}")


if __name__ == "__main__":
    main()
