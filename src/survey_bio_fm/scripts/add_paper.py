"""Add a single new bio-FM paper to the survey end-to-end.

Resolves metadata, creates a seed note, downloads the PDF and converts to
markdown. Extraction (LLM) is left to the orchestrating session via
``extract_paper`` (which renders the agent prompt).

Usage::

    uv run -- python -m survey_bio_fm.scripts.add_paper --arxiv 2306.15006
    uv run -- python -m survey_bio_fm.scripts.add_paper \
        --url https://example.com/paper.pdf --title "..." --modality dna
"""

from __future__ import annotations

import argparse
import datetime as dt
import logging
import sys

from survey_bio_fm.metadata import fetch_arxiv_metadata
from survey_bio_fm.notes import PaperNote, upsert_note
from survey_bio_fm.scripts.fetch_paper import fetch_one
from survey_bio_fm.slug import slugify

logger = logging.getLogger(__name__)


def add_arxiv(arxiv_id: str, modalities: list[str]) -> str:
    meta = fetch_arxiv_metadata(arxiv_id)
    paper_id = slugify(meta.title, meta.year)
    note = PaperNote(
        id=paper_id,
        title=meta.title,
        modalities=modalities or ["other"],
        status="seed",
        authors=meta.authors,
        year=meta.year,
        arxiv=meta.arxiv,
        url=meta.url,
        added_at=dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        body=f"## Abstract (from arxiv)\n\n{meta.abstract or '_n/a_'}\n",
    )
    upsert_note(note)
    fetch_one(paper_id)
    return paper_id


def add_url(url: str, title: str, modalities: list[str]) -> str:
    paper_id = slugify(title)
    note = PaperNote(
        id=paper_id,
        title=title,
        modalities=modalities or ["other"],
        status="seed",
        url=url,
        added_at=dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
    )
    upsert_note(note)
    fetch_one(paper_id)
    return paper_id


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--arxiv", help="arxiv id, e.g. 2306.15006")
    src.add_argument("--url", help="direct PDF url")
    p.add_argument("--title", help="required when --url is used")
    p.add_argument(
        "--modality",
        action="append",
        default=[],
        help="repeat: --modality dna --modality multimodal",
    )
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    if args.arxiv:
        pid = add_arxiv(args.arxiv, args.modality)
    else:
        if not args.title:
            sys.stderr.write("--title is required with --url\n")
            return 2
        pid = add_url(args.url, args.title, args.modality)
    print(pid)
    print(f"Next: dispatch extraction for {pid} (see notes/{pid}.md).")
    print(f"Render prompt with: uv run -- python -m survey_bio_fm.scripts.extract_paper {pid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
