"""Deduplicate papers across multiple sources."""

from difflib import SequenceMatcher


TITLE_SIMILARITY_THRESHOLD = 0.9


def merge(*paper_lists):
    """Merge multiple paper lists, removing duplicates.

    Priority: first source wins (earlier lists have higher priority).
    Dedup by: arXiv ID > DOI-like ID > fuzzy title match.

    Args:
        *paper_lists: Variable number of paper lists.

    Returns:
        Merged, deduplicated list of papers.
    """
    seen_ids = set()
    seen_titles = []
    merged = []

    for papers in paper_lists:
        for paper in papers:
            pid = paper.get("id", "")
            title = paper.get("title", "")

            # Skip if same ID already seen
            if pid and pid in seen_ids:
                continue

            # Skip if very similar title already seen
            if _is_title_duplicate(title, seen_titles):
                continue

            seen_ids.add(pid)
            if title:
                seen_titles.append(title.lower().strip())
            merged.append(paper)

    return merged


def _is_title_duplicate(title, seen_titles):
    """Check if a title is too similar to any already-seen title."""
    if not title:
        return False
    normalized = title.lower().strip()
    for seen in seen_titles:
        ratio = SequenceMatcher(None, normalized, seen).ratio()
        if ratio >= TITLE_SIMILARITY_THRESHOLD:
            return True
    return False
