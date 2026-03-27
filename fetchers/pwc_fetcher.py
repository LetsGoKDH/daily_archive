"""Fetch trending papers from Papers With Code API (Phase 2)."""

import requests


PWC_API_URL = "https://paperswithcode.com/api/v1/papers/"


def fetch_trending(limit=30):
    """Fetch trending papers from Papers With Code.

    Args:
        limit: Max number of papers to fetch.

    Returns:
        List of paper dicts in the standard schema.
    """
    print(f"[pwc] Fetching trending papers...")

    try:
        resp = requests.get(
            PWC_API_URL,
            params={"ordering": "-trending", "items_per_page": limit},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[pwc] Error: {e}")
        return []

    papers = []
    for item in data.get("results", []):
        paper = _parse_paper(item)
        if paper:
            papers.append(paper)

    print(f"[pwc] Got {len(papers)} trending papers")
    return papers


def _parse_paper(item):
    """Parse a Papers With Code paper into our standard schema."""
    title = item.get("title", "")
    if not title:
        return None

    arxiv_id = item.get("arxiv_id", "")
    url_slug = item.get("url_abs", "") or item.get("paper_url", "")

    # Build URL
    url = ""
    if arxiv_id:
        url = f"https://arxiv.org/abs/{arxiv_id}"
    elif url_slug:
        url = url_slug

    pdf_url = ""
    if arxiv_id:
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"

    # Code repository
    code_url = None
    if item.get("proceeding"):
        code_url = item.get("proceeding")

    return {
        "id": arxiv_id or title[:40],
        "title": title,
        "authors": item.get("authors", []) or [],
        "abstract": item.get("abstract", "") or "",
        "summary_en": "",
        "summary_ko": "",
        "categories": [],
        "venue_hint": item.get("conference", "") or "Papers With Code",
        "source": "pwc",
        "url": url,
        "pdf_url": pdf_url,
        "code_url": code_url,
        "published": (item.get("published") or "")[:10],
    }
