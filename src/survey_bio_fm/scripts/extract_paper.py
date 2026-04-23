"""Print the prompt to dispatch to an opus extraction agent.

The actual LLM call is made by the orchestrating session (Copilot) via the
`task` tool — this script renders the prompt with correct paths so the
orchestrator can copy-paste it into a `task` invocation.

Usage::

    uv run -- python -m survey_bio_fm.scripts.extract_paper <paper-id>
"""

from __future__ import annotations

import argparse
import sys

from survey_bio_fm.notes import REPO_ROOT, load_note, note_path
from survey_bio_fm.prompts import render_extraction_prompt


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("paper_id")
    args = p.parse_args(argv)
    note = load_note(note_path(args.paper_id))
    if not note.md_path:
        sys.stderr.write(f"{args.paper_id}: md_path not set; run fetch_paper first.\n")
        return 1
    prompt = render_extraction_prompt(
        paper_id=note.id,
        title=note.title,
        md_path=str(REPO_ROOT / note.md_path),
        note_path=str(note_path(note.id)),
        repo_root=str(REPO_ROOT),
    )
    print(prompt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
