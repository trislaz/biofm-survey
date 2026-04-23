"""Resolve note slugs to canonical URLs (DOI > arXiv > URL).

Usage:
    from survey_bio_fm.scripts.cite import slug_to_url, slug_to_link
    slug_to_url("highly-accurate-protein-structure-2021")
    # → "https://doi.org/10.1038/s41586-021-03819-2"
    slug_to_link("highly-accurate-protein-structure-2021", text="AlphaFold 2")
    # → "[AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2)"

Or run as a script to dump a slug->URL JSON map:
    uv run -- python -m survey_bio_fm.scripts.cite > slug_urls.json
"""

from __future__ import annotations

import json
import sys
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
NOTES_DIR = ROOT / "notes"


def _parse_frontmatter(path: Path) -> dict:
    """Return YAML frontmatter as a dict (empty if none)."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError:
        return {}


def _normalize_doi(doi: str) -> str:
    doi = doi.strip()
    if doi.startswith("http"):
        return doi
    if doi.startswith("doi:"):
        doi = doi[4:]
    return f"https://doi.org/{doi}"


def _normalize_arxiv(arxiv: str) -> str:
    arxiv = arxiv.strip()
    if arxiv.startswith("http"):
        return arxiv
    if arxiv.startswith("arxiv:"):
        arxiv = arxiv[6:]
    return f"https://arxiv.org/abs/{arxiv}"


@lru_cache(maxsize=1)
def slug_url_map() -> dict[str, str]:
    """Build the slug → URL map from all notes."""
    out: dict[str, str] = {}
    for note in NOTES_DIR.glob("*.md"):
        fm = _parse_frontmatter(note)
        slug = note.stem
        url = None
        if fm.get("doi"):
            url = _normalize_doi(str(fm["doi"]))
        elif fm.get("arxiv"):
            url = _normalize_arxiv(str(fm["arxiv"]))
        elif fm.get("url"):
            url = str(fm["url"]).strip()
        if url:
            out[slug] = url
    return out


@lru_cache(maxsize=1)
def slug_title_map() -> dict[str, str]:
    out: dict[str, str] = {}
    for note in NOTES_DIR.glob("*.md"):
        fm = _parse_frontmatter(note)
        title = fm.get("title")
        if title:
            out[note.stem] = str(title)
    return out


def slug_to_url(slug: str) -> str | None:
    return slug_url_map().get(slug)


def slug_to_link(slug: str, text: str | None = None) -> str:
    """Return a markdown link `[text](url)`. Falls back to bare slug if no URL."""
    url = slug_to_url(slug)
    label = text or slug
    if url:
        return f"[{label}]({url})"
    return f"[{label}]"


def is_fm(slug: str) -> bool | None:
    """Return ``is_fm`` flag from frontmatter (None if absent)."""
    note = NOTES_DIR / f"{slug}.md"
    if not note.exists():
        return None
    fm = _parse_frontmatter(note)
    val = fm.get("is_fm")
    if val is None:
        return None
    return bool(val)


def main() -> None:
    print(json.dumps(slug_url_map(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
