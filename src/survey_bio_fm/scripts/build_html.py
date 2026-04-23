"""Render the bio-FM survey as a static HTML site.

Outputs to ``survey-bio-fm/site/``:
  - ``index.html``         → insights.md (the guidebook)
  - ``modalities.html``    → modalities.md
  - ``readme.html``        → README.md
  - ``papers/<slug>.html`` → one page per note in ``notes/``
  - ``papers.html``        → sortable index of all papers

Usage:
    uv run -- python -m survey_bio_fm.scripts.build_html
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[3]
NOTES_DIR = ROOT / "notes"
SITE_DIR = ROOT / "site"
PAPERS_DIR = SITE_DIR / "papers"

CSS = """
:root { --fg:#1f2328; --muted:#6e7781; --bg:#ffffff; --accent:#0969da;
        --code-bg:#f6f8fa; --border:#d0d7de; }
@media (prefers-color-scheme: dark) {
  :root { --fg:#e6edf3; --muted:#8b949e; --bg:#0d1117; --accent:#2f81f7;
          --code-bg:#161b22; --border:#30363d; }
}
* { box-sizing: border-box; }
body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",
       Helvetica,Arial,sans-serif; color:var(--fg); background:var(--bg);
       line-height:1.55; }
.layout { display:grid; grid-template-columns:280px 1fr; min-height:100vh; }
nav.sidebar { border-right:1px solid var(--border); padding:1.25rem 1rem;
              overflow-y:auto; max-height:100vh; position:sticky; top:0;
              background:var(--bg); }
nav.sidebar h2 { font-size:.8rem; text-transform:uppercase; color:var(--muted);
                 margin:1.25rem 0 .4rem; letter-spacing:.05em; }
nav.sidebar a { display:block; padding:.2rem .4rem; border-radius:4px;
                color:var(--fg); text-decoration:none; font-size:.9rem; }
nav.sidebar a:hover { background:var(--code-bg); color:var(--accent); }
nav.sidebar input { width:100%; padding:.4rem .5rem; border:1px solid var(--border);
                    border-radius:6px; background:var(--bg); color:var(--fg); }
main { padding:2rem 3rem; max-width:1100px; }
h1,h2,h3,h4 { line-height:1.25; }
h1 { border-bottom:1px solid var(--border); padding-bottom:.3em; }
h2 { border-bottom:1px solid var(--border); padding-bottom:.2em; margin-top:2em; }
a { color:var(--accent); }
code { background:var(--code-bg); padding:.15em .35em; border-radius:4px;
       font-size:.9em; }
pre { background:var(--code-bg); padding:1rem; border-radius:6px; overflow-x:auto; }
pre code { background:transparent; padding:0; }
table { border-collapse:collapse; margin:1rem 0; display:block; overflow-x:auto; }
th,td { border:1px solid var(--border); padding:.4rem .7rem; text-align:left;
        vertical-align:top; }
th { background:var(--code-bg); }
blockquote { border-left:4px solid var(--border); margin:1em 0; padding:.2em 1em;
             color:var(--muted); }
.meta { color:var(--muted); font-size:.85rem; margin-bottom:1.5rem; }
.tag { display:inline-block; padding:.1em .55em; margin:.1em .2em .1em 0;
       background:var(--code-bg); border:1px solid var(--border);
       border-radius:10px; font-size:.75rem; color:var(--muted); }
@media (max-width:800px) {
  .layout { grid-template-columns:1fr; }
  nav.sidebar { position:static; max-height:none; border-right:none;
                border-bottom:1px solid var(--border); }
  main { padding:1.5rem 1rem; }
}
"""

MD_EXTS = ["fenced_code", "tables", "toc", "sane_lists", "attr_list"]


def parse_note(path: Path) -> tuple[dict, str]:
    """Split YAML frontmatter from body."""
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            fm = yaml.safe_load(text[4:end]) or {}
            return fm, text[end + 5 :]
    return {}, text


def md_to_html(md_text: str) -> str:
    return markdown.markdown(md_text, extensions=MD_EXTS)


def render_page(title: str, body_html: str, sidebar_html: str,
                rel_root: str = ".") -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Bio-FM Survey</title>
<link rel="stylesheet" href="{rel_root}/style.css">
</head>
<body>
<div class="layout">
<nav class="sidebar">
<input type="search" id="filter" placeholder="Filter…" oninput="filterLinks()">
{sidebar_html}
</nav>
<main>{body_html}</main>
</div>
<script>
function filterLinks() {{
  const q = document.getElementById('filter').value.toLowerCase();
  document.querySelectorAll('nav.sidebar a').forEach(a => {{
    a.style.display = a.textContent.toLowerCase().includes(q) ? '' : 'none';
  }});
}}
</script>
</body>
</html>
"""


def rewrite_note_links(html: str) -> str:
    """Convert ``[slug](slug.md)`` style links to ``slug.html``."""
    return re.sub(r'href="([^"#]+)\.md(#[^"]*)?"',
                  lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"', html)


def build() -> None:
    SITE_DIR.mkdir(exist_ok=True)
    PAPERS_DIR.mkdir(exist_ok=True)
    (SITE_DIR / "style.css").write_text(CSS, encoding="utf-8")

    notes: list[tuple[str, dict, str]] = []
    for p in sorted(NOTES_DIR.glob("*.md")):
        fm, body = parse_note(p)
        notes.append((p.stem, fm, body))

    # Sort by year desc, then title
    def sort_key(item: tuple[str, dict, str]) -> tuple[int, str]:
        slug, fm, _ = item
        year = fm.get("year") or 0
        try:
            year = int(year)
        except (TypeError, ValueError):
            year = 0
        return (-year, fm.get("title", slug).lower())

    notes_sorted = sorted(notes, key=sort_key)

    # Sidebar for top-level pages
    top_sidebar = (
        '<h2>Survey</h2>'
        '<a href="index.html">Guidebook (insights)</a>'
        '<a href="modalities.html">Modalities</a>'
        '<a href="papers.html">All papers</a>'
        '<a href="readme.html">README</a>'
    )

    # Papers index page
    rows = ['<table><thead><tr><th>Year</th><th>Title</th>'
            '<th>Modality</th><th>Status</th></tr></thead><tbody>']
    for slug, fm, _ in notes_sorted:
        title = fm.get("title", slug)
        year = fm.get("year", "—")
        modality = fm.get("modality", "")
        if isinstance(modality, list):
            modality = ", ".join(modality)
        status = fm.get("status", "")
        rows.append(
            f'<tr><td>{year}</td>'
            f'<td><a href="papers/{slug}.html">{title}</a></td>'
            f'<td>{modality}</td><td>{status}</td></tr>'
        )
    rows.append("</tbody></table>")
    papers_index_html = (
        f"<h1>All papers ({len(notes_sorted)})</h1>" + "".join(rows)
    )
    (SITE_DIR / "papers.html").write_text(
        render_page("All papers", papers_index_html, top_sidebar), encoding="utf-8"
    )

    # Top-level md pages
    for src_name, out_name, title in [
        ("insights.md", "index.html", "Guidebook"),
        ("modalities.md", "modalities.html", "Modalities"),
        ("README.md", "readme.html", "README"),
    ]:
        src = ROOT / src_name
        if not src.exists():
            continue
        body = md_to_html(src.read_text(encoding="utf-8"))
        body = rewrite_note_links(body)
        # Rewrite notes/<slug>.html → papers/<slug>.html
        body = re.sub(r'href="notes/([^"]+)\.html"',
                      r'href="papers/\1.html"', body)
        (SITE_DIR / out_name).write_text(
            render_page(title, body, top_sidebar), encoding="utf-8"
        )

    # Sidebar for paper pages: list every paper
    paper_links = []
    for slug, fm, _ in notes_sorted:
        title = fm.get("title", slug)
        year = fm.get("year", "")
        label = f"{year} · {title}" if year else title
        paper_links.append(f'<a href="{slug}.html">{label}</a>')
    paper_sidebar = (
        '<h2>Survey</h2>'
        '<a href="../index.html">Guidebook</a>'
        '<a href="../modalities.html">Modalities</a>'
        '<a href="../papers.html">All papers</a>'
        f'<h2>Papers ({len(paper_links)})</h2>' + "".join(paper_links)
    )

    # Per-paper pages
    for slug, fm, body in notes_sorted:
        title = fm.get("title", slug)
        year = fm.get("year", "")
        meta_bits = []
        if year:
            meta_bits.append(f"<span>{year}</span>")
        for key in ("authors", "venue", "doi", "arxiv", "url"):
            v = fm.get(key)
            if not v:
                continue
            if key in ("doi", "arxiv", "url"):
                href = v if v.startswith("http") else (
                    f"https://doi.org/{v}" if key == "doi"
                    else f"https://arxiv.org/abs/{v}"
                )
                meta_bits.append(f'<a href="{href}">{key}:{v}</a>')
            else:
                if isinstance(v, list):
                    v = ", ".join(map(str, v))
                meta_bits.append(f"<span>{key}: {v}</span>")
        tags = []
        for key in ("modality", "task", "status", "evidence_quality"):
            v = fm.get(key)
            if not v:
                continue
            if isinstance(v, list):
                for vi in v:
                    tags.append(f'<span class="tag">{key}: {vi}</span>')
            else:
                tags.append(f'<span class="tag">{key}: {v}</span>')

        body_html = (
            f"<h1>{title}</h1>"
            f'<div class="meta">{" · ".join(meta_bits)}</div>'
            f'<div>{"".join(tags)}</div>'
            + md_to_html(body)
        )
        body_html = rewrite_note_links(body_html)
        (PAPERS_DIR / f"{slug}.html").write_text(
            render_page(title, body_html, paper_sidebar, rel_root=".."),
            encoding="utf-8",
        )

    # Manifest
    manifest = {
        "papers": len(notes_sorted),
        "pages": ["index.html", "modalities.html", "papers.html", "readme.html"],
    }
    (SITE_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Built site/ with {len(notes_sorted)} paper pages.")
    print(f"Open: file://{SITE_DIR / 'index.html'}")


if __name__ == "__main__":
    build()
