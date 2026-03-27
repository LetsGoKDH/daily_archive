"""Generate paper summaries using OpenAI API."""

import json
from openai import OpenAI, APIError

from config import OPENAI_API_KEY, SUMMARY_MODEL, SUMMARY_BATCH_SIZE


SUMMARY_PROMPT = """\
You are an academic paper summarizer. For each paper below, write:
1. **English summary**: 2-3 sentences covering the problem, proposed method, and key results.
2. **Korean summary (한국어 요약)**: A natural Korean translation of the English summary.

Return ONLY a JSON array with objects like:
[
  {{"id": "paper_id", "summary_en": "...", "summary_ko": "..."}}
]

Papers:
{papers_text}
"""


def summarize_batch(papers):
    """Add AI-generated summaries to a list of papers.

    Processes papers in batches. Papers that already have summaries are skipped.

    Args:
        papers: List of paper dicts. Modified in-place with summary_en/summary_ko.

    Returns:
        The same list with summaries filled in.
    """
    if not OPENAI_API_KEY:
        print("[summarizer] No OPENAI_API_KEY set, skipping summaries")
        _fallback_summaries(papers)
        return papers

    client = OpenAI(api_key=OPENAI_API_KEY)
    needs_summary = [p for p in papers if not p.get("summary_en")]

    print(f"[summarizer] Generating summaries for {len(needs_summary)} papers "
          f"(model: {SUMMARY_MODEL}, batch size: {SUMMARY_BATCH_SIZE})")

    for i in range(0, len(needs_summary), SUMMARY_BATCH_SIZE):
        batch = needs_summary[i:i + SUMMARY_BATCH_SIZE]
        _summarize_one_batch(client, batch)
        print(f"[summarizer] Completed batch {i // SUMMARY_BATCH_SIZE + 1}"
              f"/{(len(needs_summary) + SUMMARY_BATCH_SIZE - 1) // SUMMARY_BATCH_SIZE}")

    return papers


def _summarize_one_batch(client, batch):
    """Send one batch of papers to OpenAI for summarization."""
    papers_text = ""
    for j, paper in enumerate(batch, 1):
        papers_text += (
            f"\n---\nPaper {j} (id: {paper['id']}):\n"
            f"Title: {paper['title']}\n"
            f"Abstract: {paper['abstract'][:1000]}\n"
        )

    prompt = SUMMARY_PROMPT.format(papers_text=papers_text)

    try:
        response = client.chat.completions.create(
            model=SUMMARY_MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )

        text = response.choices[0].message.content.strip()
        # Extract JSON from response (handle markdown code blocks)
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        summaries = json.loads(text)
        summary_map = {s["id"]: s for s in summaries}

        for paper in batch:
            if paper["id"] in summary_map:
                paper["summary_en"] = summary_map[paper["id"]].get("summary_en", "")
                paper["summary_ko"] = summary_map[paper["id"]].get("summary_ko", "")

    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"[summarizer] Failed to parse response: {e}")
        _fallback_summaries(batch)
    except APIError as e:
        print(f"[summarizer] API error: {e}")
        _fallback_summaries(batch)


def _fallback_summaries(papers):
    """Use first 2 sentences of abstract as fallback summary."""
    for paper in papers:
        if not paper.get("summary_en"):
            abstract = paper.get("abstract", "")
            sentences = abstract.split(". ")
            summary = ". ".join(sentences[:2])
            if not summary.endswith("."):
                summary += "."
            paper["summary_en"] = summary
            paper["summary_ko"] = "(요약 생성 실패 - 원문 초록 참조)"
