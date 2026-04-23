"""Convert PDFs to markdown for downstream LLM extraction.

Tries (in order): docling VLM (granite_docling) → docling default → pdfplumber
→ pypdf. Each fallback is invoked only if the previous one errors out or
produces obviously empty output.

Set the env var ``SBFM_CONVERT_METHOD`` to override the default order:

* ``docling-vlm`` (default when GPU available)
* ``docling`` — plain docling (CPU or GPU)
* ``pdfplumber`` — fast text-only fallback; useful for bulk conversion
* ``pypdf`` — last resort
"""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

MIN_USABLE_CHARS = 1000


def _has_gpu() -> bool:
    try:
        import torch

        return bool(torch.cuda.is_available())
    except Exception:
        return False


def _docling_cli_available() -> bool:
    return shutil.which("docling") is not None


def _try_docling(pdf: Path, out_md: Path, *, vlm: bool) -> bool:
    """Run the docling CLI; return True iff a usable markdown file was produced."""
    if not _docling_cli_available():
        return False
    out_md.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        cmd = ["docling", "--to", "md", "--output", str(tmpdir)]
        if vlm:
            cmd += ["--pipeline", "vlm", "--vlm-model", "granite_docling"]
        cmd.append(str(pdf))
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        except subprocess.TimeoutExpired:
            logger.warning("docling timed out for %s (vlm=%s)", pdf, vlm)
            return False
        if r.returncode != 0:
            logger.warning("docling failed (vlm=%s) for %s: %s", vlm, pdf, r.stderr[:500])
            return False
        produced = list(tmpdir.glob("*.md"))
        if not produced:
            return False
        text = produced[0].read_text(encoding="utf-8", errors="replace")
        if len(text.strip()) < MIN_USABLE_CHARS:
            logger.warning("docling produced too little text for %s", pdf)
            return False
        out_md.write_text(text, encoding="utf-8")
        return True


def _try_pdfplumber(pdf: Path, out_md: Path) -> bool:
    try:
        import pdfplumber
    except ImportError:
        return False
    try:
        with pdfplumber.open(pdf) as doc:
            pages = [p.extract_text() or "" for p in doc.pages]
        text = "\n\n".join(pages).strip()
    except Exception as e:
        logger.warning("pdfplumber failed for %s: %s", pdf, e)
        return False
    if len(text) < MIN_USABLE_CHARS:
        return False
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")
    return True


def _try_pypdf(pdf: Path, out_md: Path) -> bool:
    try:
        from pypdf import PdfReader
    except ImportError:
        return False
    try:
        reader = PdfReader(str(pdf))
        text = "\n\n".join((page.extract_text() or "") for page in reader.pages).strip()
    except Exception as e:
        logger.warning("pypdf failed for %s: %s", pdf, e)
        return False
    if len(text) < 200:
        return False
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")
    return True


def _default_chain() -> list[str]:
    """Return method-name chain to try, in order."""
    forced = os.environ.get("SBFM_CONVERT_METHOD", "").strip()
    if forced:
        # Forced primary; but always keep fallbacks behind it.
        primary = forced
        rest = [m for m in ["docling-vlm", "docling", "pdfplumber", "pypdf"] if m != primary]
        return [primary, *rest]
    if _has_gpu():
        return ["docling-vlm", "docling", "pdfplumber", "pypdf"]
    return ["docling", "pdfplumber", "pypdf"]


def convert_pdf_to_markdown(pdf: Path, out_md: Path, *, force: bool = False) -> tuple[Path, str]:
    """Convert ``pdf`` to markdown at ``out_md``.

    Returns ``(out_md, method)`` where ``method`` is one of
    ``{"docling-vlm", "docling", "pdfplumber", "pypdf", "cached"}``.
    Raises ``RuntimeError`` if all methods fail.
    """
    assert pdf.exists(), f"missing pdf: {pdf}"
    if out_md.exists() and not force and out_md.stat().st_size > MIN_USABLE_CHARS:
        return out_md, "cached"
    for method in _default_chain():
        ok = False
        if method == "docling-vlm":
            ok = _try_docling(pdf, out_md, vlm=True)
        elif method == "docling":
            ok = _try_docling(pdf, out_md, vlm=False)
        elif method == "pdfplumber":
            ok = _try_pdfplumber(pdf, out_md)
        elif method == "pypdf":
            ok = _try_pypdf(pdf, out_md)
        if ok:
            return out_md, method
    raise RuntimeError(f"all PDF→MD methods failed for {pdf}")
