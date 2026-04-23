"""Download paper PDFs from arxiv / biorxiv / generic URLs."""

from __future__ import annotations

import re
import time
from pathlib import Path

import requests

ARXIV_ID_RE = re.compile(r"^(\d{4}\.\d{4,5})(v\d+)?$")
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36 survey-bio-fm/0.1"
)


def _http_get(url: str, *, timeout: int = 60) -> requests.Response:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/pdf,text/html,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    return requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)


def arxiv_pdf_url(arxiv_id: str) -> str:
    """Build the arxiv PDF URL for an id like ``2306.15006`` or ``2306.15006v2``."""
    assert ARXIV_ID_RE.match(arxiv_id), f"bad arxiv id: {arxiv_id}"
    return f"https://arxiv.org/pdf/{arxiv_id}"


def download_pdf(url: str, out_path: Path, *, retries: int = 3) -> Path:
    """Download a PDF to ``out_path``. Returns the path. Raises on failure."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists() and out_path.stat().st_size > 1024:
        return out_path
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            r = _http_get(url)
            r.raise_for_status()
            ctype = r.headers.get("content-type", "")
            if "pdf" not in ctype.lower() and not r.content[:5].startswith(b"%PDF-"):
                raise RuntimeError(f"not a pdf (content-type={ctype!r}) from {url}")
            out_path.write_bytes(r.content)
            return out_path
        except Exception as e:
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"failed to download {url}: {last_err}")


def download_arxiv(arxiv_id: str, out_path: Path) -> Path:
    """Download an arxiv paper by id."""
    return download_pdf(arxiv_pdf_url(arxiv_id), out_path)
