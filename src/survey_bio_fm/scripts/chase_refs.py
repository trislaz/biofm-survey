"""Print the prompt to dispatch to an opus reference-chasing agent.

Usage::

    uv run -- python -m survey_bio_fm.scripts.chase_refs <paper-id>
"""

from __future__ import annotations

import argparse
import sys

from survey_bio_fm.notes import CACHE_DIR, REPO_ROOT, load_note, note_path
from survey_bio_fm.prompts import render_ref_chase_prompt


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("paper_id")
    args = p.parse_args(argv)
    note = load_note(note_path(args.paper_id))
    if not note.md_path:
        sys.stderr.write(f"{args.paper_id}: md_path not set; run fetch_paper first.\n")
        return 1
    refs_dir = CACHE_DIR / "refs"
    refs_dir.mkdir(parents=True, exist_ok=True)
    out_path = refs_dir / f"{note.id}.json"
    prompt = render_ref_chase_prompt(
        paper_id=note.id,
        title=note.title,
        md_path=str(REPO_ROOT / note.md_path),
        note_path=str(note_path(note.id)),
        out_path=str(out_path),
    )
    print(prompt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
