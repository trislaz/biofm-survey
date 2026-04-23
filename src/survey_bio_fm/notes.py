"""Read/write per-paper markdown notes with YAML frontmatter.

Notes live at ``survey-bio-fm/notes/<id>.md`` and follow ``schema/paper.schema.json``.
We intentionally avoid a heavy frontmatter library — the format is::

    ---
    <yaml>
    ---

    <markdown body>
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
NOTES_DIR = REPO_ROOT / "notes"
PAPERS_DIR = REPO_ROOT / "papers"
PAPERS_MD_DIR = PAPERS_DIR / "md"
CACHE_DIR = REPO_ROOT / ".cache"
SCHEMA_PATH = REPO_ROOT / "schema" / "paper.schema.json"

VALID_STATUSES = {
    "seed",
    "fetched",
    "converted",
    "extracted",
    "abstract-only",
    "paywalled-no-mirror",
    "extraction-failed",
}

VALID_MODALITIES = {
    "dna",
    "rna",
    "protein-sequence",
    "protein-structure",
    "proteomics",
    "epigenome",
    "interactome",
    "scrna",
    "single-cell-multiomics",
    "imaging-cell",
    "imaging-pathology",
    "imaging-microscopy",
    "imaging-radiology",
    "small-molecule",
    "multimodal",
    "other",
}

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)


@dataclass
class PaperNote:
    """In-memory representation of one paper note."""

    id: str
    title: str
    modalities: list[str]
    status: str = "seed"
    authors: list[str] = field(default_factory=list)
    year: int | None = None
    venue: str | None = None
    arxiv: str | None = None
    doi: str | None = None
    url: str | None = None
    pdf_path: str | None = None
    md_path: str | None = None
    evidence_quality: str = "unknown"
    tags: list[str] = field(default_factory=list)
    parameters: str | None = None
    training_tokens: str | None = None
    training_compute: str | None = None
    references_chased: bool = False
    added_at: str | None = None
    updated_at: str | None = None
    body: str = ""

    def to_frontmatter(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "venue": self.venue,
            "arxiv": self.arxiv,
            "doi": self.doi,
            "url": self.url,
            "pdf_path": self.pdf_path,
            "md_path": self.md_path,
            "modalities": self.modalities,
            "status": self.status,
            "evidence_quality": self.evidence_quality,
            "tags": self.tags,
            "parameters": self.parameters,
            "training_tokens": self.training_tokens,
            "training_compute": self.training_compute,
            "references_chased": self.references_chased,
            "added_at": self.added_at,
            "updated_at": self.updated_at,
        }

    def validate(self) -> None:
        assert self.status in VALID_STATUSES, f"bad status: {self.status}"
        assert self.modalities, "modalities must be non-empty"
        for m in self.modalities:
            assert m in VALID_MODALITIES, f"bad modality: {m}"
        assert re.match(r"^[a-z0-9][a-z0-9._-]*$", self.id), f"bad id: {self.id}"


def note_path(paper_id: str) -> Path:
    """Return the notes file path for ``paper_id``."""
    return NOTES_DIR / f"{paper_id}.md"


def list_notes() -> list[Path]:
    """Return all existing note paths, sorted."""
    if not NOTES_DIR.exists():
        return []
    return sorted(p for p in NOTES_DIR.glob("*.md") if p.is_file())


def load_note(path: Path) -> PaperNote:
    """Load a ``PaperNote`` from a markdown file with YAML frontmatter."""
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"{path}: missing YAML frontmatter")
    fm = yaml.safe_load(m.group(1)) or {}
    body = m.group(2)
    return PaperNote(
        id=fm["id"],
        title=fm["title"],
        modalities=list(fm.get("modalities") or []),
        status=fm.get("status", "seed"),
        authors=list(fm.get("authors") or []),
        year=fm.get("year"),
        venue=fm.get("venue"),
        arxiv=fm.get("arxiv"),
        doi=fm.get("doi"),
        url=fm.get("url"),
        pdf_path=fm.get("pdf_path"),
        md_path=fm.get("md_path"),
        evidence_quality=fm.get("evidence_quality", "unknown"),
        tags=list(fm.get("tags") or []),
        parameters=fm.get("parameters"),
        training_tokens=fm.get("training_tokens"),
        training_compute=fm.get("training_compute"),
        references_chased=bool(fm.get("references_chased", False)),
        added_at=fm.get("added_at"),
        updated_at=fm.get("updated_at"),
        body=body,
    )


def load_all_notes() -> list[PaperNote]:
    """Load every note currently in ``notes/``."""
    return [load_note(p) for p in list_notes()]


def save_note(note: PaperNote) -> Path:
    """Persist a ``PaperNote`` to ``notes/<id>.md`` (idempotent overwrite)."""
    note.validate()
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    fm_yaml = yaml.safe_dump(
        note.to_frontmatter(),
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )
    body = note.body.strip("\n")
    text = f"---\n{fm_yaml}---\n\n{body}\n" if body else f"---\n{fm_yaml}---\n"
    out = note_path(note.id)
    out.write_text(text, encoding="utf-8")
    return out


def upsert_note(note: PaperNote) -> Path:
    """Save a note, merging with any existing one (existing fields take precedence
    only for fields that are populated; new note's non-None values overwrite)."""
    out = note_path(note.id)
    if out.exists():
        existing = load_note(out)
        for fld in (
            "title",
            "authors",
            "year",
            "venue",
            "arxiv",
            "doi",
            "url",
            "pdf_path",
            "md_path",
            "evidence_quality",
            "parameters",
            "training_tokens",
            "training_compute",
        ):
            new_val = getattr(note, fld)
            if new_val in (None, "", []):
                setattr(note, fld, getattr(existing, fld))
        # Tags / modalities: union.
        note.tags = sorted(set(existing.tags) | set(note.tags))
        note.modalities = sorted(set(existing.modalities) | set(note.modalities))
        # references_chased: OR.
        note.references_chased = note.references_chased or existing.references_chased
        # Body: keep existing if new is empty.
        if not note.body.strip():
            note.body = existing.body
        # Status: only "advance" forward.
        note.status = _advance_status(existing.status, note.status)
        # added_at preserved.
        if existing.added_at and not note.added_at:
            note.added_at = existing.added_at
    return save_note(note)


_STATUS_ORDER = [
    "seed",
    "fetched",
    "converted",
    "abstract-only",
    "paywalled-no-mirror",
    "extracted",
    "extraction-failed",
]


def _advance_status(old: str, new: str) -> str:
    """Pick the more 'advanced' status; never regress past extracted."""
    if old == "extracted" and new not in {"extracted", "extraction-failed"}:
        return "extracted"
    return new if _STATUS_ORDER.index(new) >= _STATUS_ORDER.index(old) else old


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
