"""Fetch a paper PDF and convert it to markdown.

Usage::

    uv run -- python -m survey_bio_fm.scripts.fetch_paper <paper-id>

The note ``notes/<paper-id>.md`` must already exist (created by ``search_seeds``
or ``add_paper``) with at least an ``arxiv`` or ``url`` field. On success the
note's ``status`` advances to ``converted`` and ``pdf_path`` / ``md_path`` are
filled in.
"""

from __future__ import annotations

import argparse
import datetime as dt
import logging
import sys

from survey_bio_fm.convert import convert_pdf_to_markdown
from survey_bio_fm.fetch import download_arxiv, download_pdf
from survey_bio_fm.notes import (
    PAPERS_DIR,
    PAPERS_MD_DIR,
    REPO_ROOT,
    load_note,
    note_path,
    save_note,
)

logger = logging.getLogger(__name__)


def fetch_one(paper_id: str, *, force: bool = False) -> str:
    """Fetch + convert a single paper. Returns the conversion method used."""
    note = load_note(note_path(paper_id))
    pdf_out = PAPERS_DIR / f"{paper_id}.pdf"
    md_out = PAPERS_MD_DIR / f"{paper_id}.md"

    # Download PDF.
    if note.arxiv:
        download_arxiv(note.arxiv, pdf_out)
    elif note.url and note.url.lower().endswith(".pdf"):
        download_pdf(note.url, pdf_out)
    else:
        raise RuntimeError(
            f"{paper_id}: no arxiv id and no direct .pdf url; please populate "
            "frontmatter (arxiv/url/doi) or fetch manually."
        )

    note.pdf_path = str(pdf_out.relative_to(REPO_ROOT))
    if note.status == "seed":
        note.status = "fetched"

    # Convert PDF → markdown.
    md_path, method = convert_pdf_to_markdown(pdf_out, md_out, force=force)
    note.md_path = str(md_path.relative_to(REPO_ROOT))
    note.status = "converted"
    note.updated_at = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    save_note(note)
    logger.info("[%s] fetched + converted via %s", paper_id, method)
    return method


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("paper_id", help="Paper id (notes/<id>.md must exist).")
    p.add_argument("--force", action="store_true", help="Re-convert even if cached.")
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    method = fetch_one(args.paper_id, force=args.force)
    print(method)
    return 0


if __name__ == "__main__":
    sys.exit(main())
