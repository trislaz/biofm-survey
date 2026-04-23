default:
    @just --list

env:
    uv sync --all-extras

format:
    uv run --extra quality -- ruff format

lint:
    uv run --extra quality -- ruff check --fix

types:
    uv run --extra quality -- pyright

check: format lint types

test:
    uv run --extra test -- pytest

# --- Survey pipeline shortcuts ---

# Discover seed papers across all modalities, writing seed stubs to notes/.
seed +ARGS="":
    uv run -- python -m survey_bio_fm.scripts.search_seeds {{ARGS}}

# Fetch + convert a single paper to markdown.
fetch ID:
    uv run -- python -m survey_bio_fm.scripts.fetch_paper {{ID}}

# Run extraction agent for a single paper.
extract ID:
    uv run -- python -m survey_bio_fm.scripts.extract_paper {{ID}}

# Reference-chase a single paper.
refs ID:
    uv run -- python -m survey_bio_fm.scripts.chase_refs {{ID}}

# Add a new paper end-to-end (fetch + extract).
add +ARGS:
    uv run -- python -m survey_bio_fm.scripts.add_paper {{ARGS}}

# Regenerate index.json, modalities.md, insights.md from notes/.
consolidate:
    uv run -- python -m survey_bio_fm.scripts.consolidate
