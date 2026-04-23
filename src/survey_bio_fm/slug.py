"""Slugify paper titles into stable IDs."""

from __future__ import annotations

import re
import unicodedata

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(title: str, year: int | None = None, max_words: int = 4) -> str:
    """Slugify ``title`` into a short, filename-safe id.

    Examples
    --------
    >>> slugify("DNABERT-2: Efficient Foundation Model", 2023)
    'dnabert-2-efficient-foundation-2023'
    """
    norm = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    norm = norm.lower()
    norm = _NON_ALNUM.sub("-", norm).strip("-")
    parts = [p for p in norm.split("-") if p]
    if max_words and len(parts) > max_words:
        parts = parts[:max_words]
    slug = "-".join(parts) or "paper"
    if year:
        slug = f"{slug}-{year}"
    return slug
