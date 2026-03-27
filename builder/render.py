"""Render static HTML from paper data using Jinja2 templates."""

import json
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from config import (
    CATEGORY_LABELS, DATA_DIR, SITE_DIR, ARCHIVE_DIR, TEMPLATE_DIR
)


def build_site(date_str, papers):
    """Build all HTML pages for the site.

    Args:
        date_str: Today's date as YYYY-MM-DD.
        papers: List of paper dicts.
    """
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=True,
    )

    # Collect unique categories from today's papers
    categories = sorted(set(
        cat for p in papers for cat in p.get("categories", [])
        if cat in CATEGORY_LABELS
    ))

    stats = _compute_stats(papers)

    # Render today's page as both index.html and archive/YYYY-MM-DD.html
    ctx = {
        "date": date_str,
        "papers": papers,
        "categories": categories,
        "category_labels": CATEGORY_LABELS,
        "stats": stats,
        "root": "",
    }

    index_tpl = env.get_template("index.html")

    # Main index.html
    _write(os.path.join(SITE_DIR, "index.html"), index_tpl.render(**ctx))

    # Archive copy
    ctx["root"] = "../"
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    _write(
        os.path.join(ARCHIVE_DIR, f"{date_str}.html"),
        index_tpl.render(**ctx),
    )

    # Archive index
    _build_archive_index(env)

    print(f"[render] Built site for {date_str} ({len(papers)} papers)")


def _build_archive_index(env):
    """Build the archive listing page from existing data files."""
    data_path = Path(DATA_DIR)
    dates = []

    if data_path.exists():
        for f in sorted(data_path.glob("*.json"), reverse=True):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                dates.append({
                    "date": f.stem,
                    "count": data.get("stats", {}).get("total", len(data.get("papers", []))),
                })
            except (json.JSONDecodeError, OSError):
                continue

    archive_tpl = env.get_template("archive.html")
    _write(
        os.path.join(ARCHIVE_DIR, "index.html"),
        archive_tpl.render(dates=dates, root="../", category_labels=CATEGORY_LABELS),
    )


def _compute_stats(papers):
    """Compute summary statistics for a set of papers."""
    by_category = {}
    for p in papers:
        for cat in p.get("categories", []):
            if cat in CATEGORY_LABELS:
                by_category[cat] = by_category.get(cat, 0) + 1

    return {
        "total": len(papers),
        "by_category": dict(sorted(by_category.items(), key=lambda x: -x[1])),
    }


def _write(path, content):
    """Write content to a file, creating parent dirs if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
