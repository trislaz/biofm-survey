"""Resolve paper metadata from arxiv / DOI sources."""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass

import requests

logger = logging.getLogger(__name__)
USER_AGENT = "survey-bio-fm/0.1 (research)"


@dataclass
class PaperMetadata:
    """Bibliographic metadata for a paper."""

    title: str
    authors: list[str]
    year: int | None
    arxiv: str | None = None
    doi: str | None = None
    url: str | None = None
    venue: str | None = None
    abstract: str | None = None


_ARXIV_API = "http://export.arxiv.org/api/query"


def _entry_to_meta(e, arxiv_id: str | None) -> PaperMetadata:
    title = str(getattr(e, "title", "")).strip()
    summary = str(getattr(e, "summary", "")).strip()
    link = str(getattr(e, "link", "")) or None
    pub = str(getattr(e, "published", "") or "")
    year: int | None = None
    m = re.match(r"(\d{4})", pub)
    if m:
        year = int(m.group(1))
    return PaperMetadata(
        title=re.sub(r"\s+", " ", title),
        authors=[a.name for a in getattr(e, "authors", [])],
        year=year,
        arxiv=arxiv_id,
        url=link,
        abstract=re.sub(r"\s+", " ", summary) or None,
    )


def _arxiv_get(params: dict[str, str], *, retries: int = 4) -> str:
    """GET arxiv API with backoff on 429 / transient errors."""
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            r = requests.get(
                _ARXIV_API,
                params=params,
                headers={"User-Agent": USER_AGENT},
                timeout=30,
            )
            if r.status_code == 429:
                wait = 30 * (attempt + 1)
                logger.warning("arxiv 429; sleeping %ds (attempt %d)", wait, attempt + 1)
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.text
        except Exception as e:
            last_err = e
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"arxiv API failed: {last_err}")


def fetch_arxiv_metadata(arxiv_id: str) -> PaperMetadata:
    """Fetch metadata for an arxiv id via the public Atom API."""
    import feedparser

    text = _arxiv_get({"id_list": arxiv_id})
    feed = feedparser.parse(text)
    if not feed.entries:
        raise RuntimeError(f"no arxiv entry for {arxiv_id}")
    return _entry_to_meta(feed.entries[0], arxiv_id)


def search_arxiv(query: str, *, max_results: int = 25) -> list[PaperMetadata]:
    """Search arxiv with a free-text query."""
    import feedparser

    params = {
        "search_query": query,
        "max_results": str(max_results),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    text = _arxiv_get(params)
    feed = feedparser.parse(text)
    out: list[PaperMetadata] = []
    for e in feed.entries:
        eid = str(getattr(e, "id", ""))
        m = re.search(r"abs/([^v\s]+)", eid)
        arxiv_id = m.group(1) if m else None
        out.append(_entry_to_meta(e, arxiv_id))
    time.sleep(3.5)  # arxiv API: be polite (1 req / 3s recommended)
    return out
