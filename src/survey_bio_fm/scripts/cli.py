"""Convenience CLI entry point: `sbfm <command> ...`."""

from __future__ import annotations

import sys

COMMANDS = {
    "seed": "survey_bio_fm.scripts.search_seeds",
    "fetch": "survey_bio_fm.scripts.fetch_paper",
    "extract": "survey_bio_fm.scripts.extract_paper",
    "refs": "survey_bio_fm.scripts.chase_refs",
    "add": "survey_bio_fm.scripts.add_paper",
    "consolidate": "survey_bio_fm.scripts.consolidate",
}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in {"-h", "--help"}:
        print("Usage: sbfm <command> [args...]")
        print("Commands: " + ", ".join(COMMANDS))
        return 0
    cmd, *rest = argv
    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        return 2
    import importlib

    mod = importlib.import_module(COMMANDS[cmd])
    return mod.main(rest)


if __name__ == "__main__":
    sys.exit(main())
