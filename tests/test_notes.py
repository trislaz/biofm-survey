"""Smoke tests for the survey-bio-fm pipeline plumbing."""

from __future__ import annotations

from pathlib import Path

import pytest

from survey_bio_fm import notes as notes_mod
from survey_bio_fm.notes import PaperNote, load_note, save_note, upsert_note
from survey_bio_fm.slug import slugify


@pytest.fixture
def isolated_notes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect NOTES_DIR to a tmp dir so tests don't touch the real survey."""
    notes_dir = tmp_path / "notes"
    notes_dir.mkdir()
    monkeypatch.setattr(notes_mod, "NOTES_DIR", notes_dir)
    return notes_dir


def test_slugify_basic() -> None:
    """Slugify should lowercase, ascii-fold, hyphenate, and append year."""
    assert slugify("DNABERT-2: Efficient Foundation Model", 2023).startswith("dnabert-2")
    assert slugify("Évolution biologique", 2024) == "evolution-biologique-2024"
    assert slugify("", None) == "paper"


def test_save_and_load_note_roundtrip(isolated_notes: Path) -> None:
    """A saved note must load back with identical fields."""
    note = PaperNote(
        id="dnabert-2-2023",
        title="DNABERT-2",
        modalities=["dna"],
        status="seed",
        year=2023,
        arxiv="2306.15006",
        body="## TL;DR\nhello\n",
    )
    p = save_note(note)
    assert p.exists()
    loaded = load_note(p)
    assert loaded.id == note.id
    assert loaded.modalities == ["dna"]
    assert loaded.arxiv == "2306.15006"
    assert "hello" in loaded.body


def test_upsert_advances_status_and_unions_modalities(isolated_notes: Path) -> None:
    """upsert_note must merge modalities and only advance status forward."""
    base = PaperNote(
        id="x-2024",
        title="X",
        modalities=["dna"],
        status="extracted",
        parameters="100M",
        body="## TL;DR\nfoo",
    )
    save_note(base)
    incoming = PaperNote(id="x-2024", title="X", modalities=["multimodal"], status="seed")
    upsert_note(incoming)
    out = load_note(isolated_notes / "x-2024.md")
    assert out.status == "extracted"  # cannot regress
    assert set(out.modalities) == {"dna", "multimodal"}
    assert out.parameters == "100M"  # preserved
    assert "foo" in out.body  # body preserved when incoming empty


def test_invalid_modality_rejected(isolated_notes: Path) -> None:
    """Validation must reject unknown modality strings."""
    note = PaperNote(id="bad-2024", title="bad", modalities=["nonsense"], status="seed")
    with pytest.raises(AssertionError):
        save_note(note)


def test_invalid_id_rejected(isolated_notes: Path) -> None:
    """IDs must be slug-shaped."""
    note = PaperNote(id="Bad ID!", title="x", modalities=["dna"], status="seed")
    with pytest.raises(AssertionError):
        save_note(note)


def test_schema_loads() -> None:
    """The JSON schema must parse and have the expected top-level fields."""
    s = notes_mod.load_schema()
    assert "properties" in s
    assert "modalities" in s["properties"]
    assert "status" in s["properties"]
