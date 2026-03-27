"""Fetch recent papers from Semantic Scholar API (Phase 2).

Covers venues not well-represented on arXiv: Interspeech, ICASSP, IEEE, ACL, EMNLP.
"""

import time
import requests

from config import S2_API_KEY, S2_VENUES


S2_API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
S2_FIELDS = "title,abstract,authors,venue,year,citationCount,tldr,externalIds,openAccessPdf,url"
RATE_LIMIT_DELAY = 1.0  # seconds between requests (free tier)


def fetch(year=None, limit_per_venue=30):
    """Fetch recent papers from Semantic Scholar for configured venues.

    Args:
        year: Filter by publication year. Defaults to current year.
        limit_per_venue: Max papers per venue query.

    Returns:
        List of paper dicts in the standard schema.
    """
    from datetime import date as _date
    if year is None:
        year = _date.today().year

    headers = {}
    if S2_API_KEY:
        headers["x-api-key"] = S2_API_KEY

    all_papers = []

    for venue in S2_VENUES:
        print(f"[s2] Fetching from venue: {venue}")
        try:
            papers = _fetch_venue(venue, year, limit_per_venue, headers)
            all_papers.extend(papers)
            print(f"[s2] Got {len(papers)} papers from {venue}")
        except Exception as e:
            print(f"[s2] Error fetching {venue}: {e}")
        time.sleep(RATE_LIMIT_DELAY)

    print(f"[s2] Total: {len(all_papers)} papers from {len(S2_VENUES)} venues")
    return all_papers


def _fetch_venue(venue, year, limit, headers):
    """Fetch papers for a single venue."""
    params = {
        "query": "",
        "venue": venue,
        "year": str(year),
        "limit": limit,
        "fields": S2_FIELDS,
    }

    resp = requests.get(S2_API_URL, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    papers = []
    for item in data.get("data", []):
        paper = _parse_paper(item)
        if paper:
            papers.append(paper)

    return papers


def _parse_paper(item):
    """Parse a Semantic Scholar paper into our standard schema."""
    title = item.get("title", "")
    if not title:
        return None

    # Extract arXiv ID if available
    ext_ids = item.get("externalIds") or {}
    arxiv_id = ext_ids.get("ArXiv", "")
    doi = ext_ids.get("DOI", "")
    s2_id = item.get("paperId", "")

    paper_id = arxiv_id or doi or s2_id

    # Authors
    authors = [a.get("name", "") for a in (item.get("authors") or []) if a.get("name")]

    # Abstract
    abstract = item.get("abstract") or ""

    # TLDR from S2
    tldr = ""
    if item.get("tldr"):
        tldr = item["tldr"].get("text", "")

    # URL
    url = item.get("url", "")
    if arxiv_id:
        url = f"https://arxiv.org/abs/{arxiv_id}"

    # PDF
    pdf_url = ""
    if item.get("openAccessPdf"):
        pdf_url = item["openAccessPdf"].get("url", "")
    elif arxiv_id:
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"

    return {
        "id": paper_id,
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "summary_en": tldr,  # Use S2 TLDR as initial summary
        "summary_ko": "",
        "categories": [],
        "venue_hint": item.get("venue", ""),
        "source": "semantic_scholar",
        "url": url,
        "pdf_url": pdf_url,
        "code_url": None,
        "published": str(item.get("year", "")),
    }
