"""Apply is_fm flag from rev4_classification.json to note frontmatters."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
NOTES_DIR = ROOT / "notes"
CLASSIFICATION = ROOT / ".cache" / "rev4_classification.json"


def main() -> None:
    raw = json.loads(CLASSIFICATION.read_text())
    if isinstance(raw, dict):
        items = raw.get("classifications", raw.get("papers", []))
    else:
        items = raw

    n_changed = 0
    for entry in items:
        slug = entry["slug"]
        is_fm = bool(entry["is_fm"])
        reason = entry.get("reason", "")
        path = NOTES_DIR / f"{slug}.md"
        if not path.exists():
            print(f"MISSING: {slug}")
            continue
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\n"), slug
        end = text.find("\n---\n", 4)
        fm = yaml.safe_load(text[4:end]) or {}
        body = text[end + 5 :]
        fm["is_fm"] = is_fm
        fm["fm_classification_reason"] = reason
        new_fm = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
        path.write_text(f"---\n{new_fm}---\n{body}", encoding="utf-8")
        n_changed += 1
    print(f"Updated {n_changed} notes")


if __name__ == "__main__":
    main()
