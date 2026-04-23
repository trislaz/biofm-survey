"""Add a paper to the survey by biorxiv DOI (constructs PDF URL)."""

from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path

from survey_bio_fm.fetch import download_pdf
from survey_bio_fm.notes import (
    PAPERS_DIR,
    PaperNote,
    upsert_note,
)
from survey_bio_fm.slug import slugify

LOGGER = logging.getLogger(__name__)


def biorxiv_pdf_url(doi: str) -> str:
    """Build a biorxiv full-text PDF URL from a 10.1101/... DOI."""
    assert doi.startswith("10.1101/"), f"not a biorxiv doi: {doi}"
    suffix = doi.split("/", 1)[1]
    return f"https://www.biorxiv.org/content/{doi}v1.full.pdf"


def main() -> None:
    parser = argparse.ArgumentParser(description="Add paper by biorxiv DOI.")
    parser.add_argument("--doi", required=True, help="biorxiv DOI, e.g. 10.1101/...")
    parser.add_argument("--title", required=True)
    parser.add_argument("--modality", action="append", default=[])
    parser.add_argument("--year", type=int)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    slug = slugify(args.title, year=args.year)
    note = PaperNote(
        id=slug,
        title=args.title,
        doi=args.doi,
        modalities=args.modality or ["other"],
        year=args.year,
        status="seed",
    )
    upsert_note(note)

    url = biorxiv_pdf_url(args.doi)
    pdf_path = PAPERS_DIR / f"{slug}.pdf"
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    LOGGER.info("downloading biorxiv pdf: %s", url)
    download_pdf(url, pdf_path)

    # Mark fetched; conversion is done by fetch_paper script
    note.status = "fetched"
    note.pdf_path = str(pdf_path)
    upsert_note(note)
    print(f"seeded: {slug} (pdf at {pdf_path})")
    print(f"next: uv run -- python -m survey_bio_fm.scripts.fetch_paper {slug}")


if __name__ == "__main__":
    main()
