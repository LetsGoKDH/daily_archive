"""Fetch recent papers from arXiv API."""

import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

import feedparser

from config import ARXIV_CATEGORIES, ARXIV_MAX_RESULTS


ARXIV_API_URL = "http://export.arxiv.org/api/query"
ATOM_NS = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"


def fetch(days_back=2, max_results=None):
    """Fetch recent papers from arXiv for configured categories.

    Args:
        days_back: How many days back to look for papers.
        max_results: Max papers to return. Defaults to ARXIV_MAX_RESULTS.

    Returns:
        List of paper dicts in the standard schema.
    """
    if max_results is None:
        max_results = ARXIV_MAX_RESULTS

    cat_query = "+OR+".join(f"cat:{cat}" for cat in ARXIV_CATEGORIES)
    query_url = (
        f"{ARXIV_API_URL}?"
        f"search_query={cat_query}"
        f"&sortBy=submittedDate&sortOrder=descending"
        f"&start=0&max_results={max_results}"
    )

    print(f"[arxiv] Fetching from: {query_url}")
    req = urllib.request.Request(query_url)
    with urllib.request.urlopen(req, timeout=60) as resp:
        xml_data = resp.read()
    feed = feedparser.parse(xml_data)

    if feed.bozo and not feed.entries:
        print(f"[arxiv] Error parsing feed: {feed.bozo_exception}")
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    papers = []

    for entry in feed.entries:
        published = _parse_date(entry.get("published", ""))
        if published and published < cutoff:
            continue

        paper = _parse_entry(entry)
        if paper:
            papers.append(paper)

    print(f"[arxiv] Found {len(papers)} papers from last {days_back} days")
    return papers


def _parse_entry(entry):
    """Parse a single arXiv feed entry into our paper schema."""
    arxiv_id = entry.get("id", "").split("/abs/")[-1]
    if not arxiv_id:
        return None

    # Extract categories
    categories = []
    for tag in entry.get("tags", []):
        term = tag.get("term", "")
        if term:
            categories.append(term)

    # Extract authors
    authors = []
    for author in entry.get("authors", []):
        name = author.get("name", "")
        if name:
            authors.append(name)

    # Extract links
    pdf_url = ""
    for link in entry.get("links", []):
        if link.get("type") == "application/pdf":
            pdf_url = link.get("href", "")
            break

    return {
        "id": arxiv_id,
        "title": _clean_text(entry.get("title", "")),
        "authors": authors,
        "abstract": _clean_text(entry.get("summary", "")),
        "summary_en": "",
        "summary_ko": "",
        "categories": categories,
        "venue_hint": "arXiv",
        "source": "arxiv",
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": pdf_url or f"https://arxiv.org/pdf/{arxiv_id}",
        "code_url": None,
        "published": entry.get("published", "")[:10],
    }


def _parse_date(date_str):
    """Parse arXiv date string to datetime."""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        return None


def _clean_text(text):
    """Clean up whitespace in text."""
    return " ".join(text.split())


if __name__ == "__main__":
    papers = fetch(days_back=2, max_results=10)
    for p in papers[:3]:
        print(f"\n{p['title']}")
        print(f"  Categories: {p['categories']}")
        print(f"  URL: {p['url']}")
