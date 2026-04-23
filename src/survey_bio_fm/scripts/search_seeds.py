"""Seed the survey with candidate bio-FM papers across all modalities.

For each modality we run a curated arxiv search query and write seed-stub
notes (status=seed) for the top-K results. The main session then fetches
+ extracts each seed and chases its references.

Usage::

    uv run -- python -m survey_bio_fm.scripts.search_seeds [--per-query 8]
"""

from __future__ import annotations

import argparse
import datetime as dt
import logging
import sys

from survey_bio_fm.metadata import search_arxiv
from survey_bio_fm.notes import PaperNote, note_path, upsert_note
from survey_bio_fm.slug import slugify

logger = logging.getLogger(__name__)

# (modality, arxiv search query). Cast a wide net; later iterations can refine.
SEED_QUERIES: list[tuple[str, str]] = [
    ("dna", 'abs:"foundation model" AND (abs:"DNA" OR abs:"genomic")'),
    ("dna", 'abs:"genomic language model"'),
    (
        "dna",
        'ti:"DNABERT" OR ti:"HyenaDNA" OR ti:"Caduceus" OR ti:"Nucleotide Transformer" OR ti:"Evo"',
    ),
    ("rna", 'abs:"RNA language model" OR abs:"RNA foundation model"'),
    ("rna", 'ti:"RNA-FM" OR ti:"Uni-RNA" OR ti:"RNAErnie" OR ti:"RiNALMo"'),
    ("protein-sequence", 'abs:"protein language model"'),
    (
        "protein-sequence",
        'ti:"ESM" OR ti:"ProtTrans" OR ti:"ProGen" OR ti:"Ankh" OR ti:"SaProt" OR ti:"ProstT5"',
    ),
    ("protein-structure", 'abs:"protein structure prediction" AND abs:"foundation model"'),
    ("protein-structure", 'ti:"AlphaFold" OR ti:"ESMFold" OR ti:"RoseTTAFold" OR ti:"OpenFold"'),
    ("proteomics", 'abs:"mass spectrometry" AND abs:"deep learning" AND abs:"foundation"'),
    ("epigenome", 'ti:"Enformer" OR ti:"Borzoi" OR ti:"ChromBPNet" OR ti:"scBasset"'),
    ("epigenome", 'abs:"epigenome" AND abs:"foundation model"'),
    ("interactome", 'abs:"protein-protein interaction" AND abs:"foundation model"'),
    ("scrna", 'abs:"single-cell" AND (abs:"foundation model" OR abs:"language model")'),
    (
        "scrna",
        'ti:"scGPT" OR ti:"scBERT" OR ti:"Geneformer" OR ti:"scFoundation" OR ti:"UCE" OR ti:"scPRINT"',
    ),
    ("single-cell-multiomics", 'abs:"single-cell multi-omics" AND abs:"foundation"'),
    ("imaging-pathology", 'abs:"computational pathology" AND abs:"foundation model"'),
    (
        "imaging-pathology",
        'ti:"UNI" OR ti:"Virchow" OR ti:"GigaPath" OR ti:"CONCH" OR ti:"Phikon" OR ti:"RudolfV"',
    ),
    ("imaging-cell", 'abs:"cell painting" AND abs:"foundation model"'),
    ("imaging-cell", 'ti:"Phenom" OR ti:"OpenPhenom" OR ti:"CellSAM" OR ti:"Cellpose"'),
    ("imaging-microscopy", 'abs:"microscopy" AND abs:"foundation model"'),
    ("imaging-radiology", 'abs:"medical imaging" AND abs:"foundation model"'),
    ("multimodal", 'abs:"biomedical" AND abs:"multimodal" AND abs:"foundation"'),
    ("multimodal", 'ti:"BioMedCLIP" OR ti:"CLOOME" OR ti:"GenePT" OR ti:"BioReason"'),
    ("small-molecule", 'abs:"molecular" AND abs:"foundation model" AND abs:"chemistry"'),
]


def seed_one(modality: str, query: str, per_query: int) -> int:
    """Run one query, upsert seed notes. Returns count added."""
    try:
        results = search_arxiv(query, max_results=per_query)
    except Exception as e:
        logger.warning("query failed (%s): %s", query, e)
        return 0
    added = 0
    for meta in results:
        if not meta.arxiv:
            continue
        slug = slugify(meta.title, meta.year)
        if note_path(slug).exists():
            # Existing note: just merge modality tag.
            existing = PaperNote(
                id=slug,
                title=meta.title,
                modalities=[modality],
                status="seed",
                arxiv=meta.arxiv,
                year=meta.year,
                url=meta.url,
                authors=meta.authors,
            )
            upsert_note(existing)
            continue
        note = PaperNote(
            id=slug,
            title=meta.title,
            modalities=[modality],
            status="seed",
            authors=meta.authors,
            year=meta.year,
            arxiv=meta.arxiv,
            url=meta.url,
            tags=[],
            added_at=dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
            body=(
                f"## TL;DR\n\n_(seed — not yet extracted)_\n\n"
                f"## Abstract (from arxiv)\n\n{meta.abstract or '_n/a_'}\n"
            ),
        )
        upsert_note(note)
        added += 1
    return added


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--per-query", type=int, default=8)
    p.add_argument(
        "--only-modality", default=None, help="If set, only run queries for this modality."
    )
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    total = 0
    for modality, query in SEED_QUERIES:
        if args.only_modality and modality != args.only_modality:
            continue
        n = seed_one(modality, query, args.per_query)
        logger.info("[%s] +%d (query=%s)", modality, n, query[:60])
        total += n
    print(f"Added {total} new seed notes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
