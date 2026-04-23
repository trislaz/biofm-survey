"""Add a paper by DOI using OpenAlex + Europe PMC + NCBI E-utilities.

Strategy (Cloudflare-free):
  1. OpenAlex by DOI → title, year, abstract, references
  2. Europe PMC search by DOI → PMC ID (if open access in PMC)
  3. NCBI E-utilities efetch → full-text JATS XML
  4. Convert JATS XML to markdown with provenance header
  5. Fallback: write abstract + OpenAlex metadata only (evidence_quality=abstract-only)

Writes:
  papers/md/<slug>.md         — converted full text or abstract+metadata
  notes/<slug>.md             — note stub with frontmatter
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from xml.etree import ElementTree as ET

from survey_bio_fm.notes import PAPERS_DIR, PaperNote, upsert_note
from survey_bio_fm.slug import slugify

LOGGER = logging.getLogger(__name__)
MD_DIR = PAPERS_DIR / "md"

UA = "Mozilla/5.0 (X11; Linux x86_64; survey-bio-fm research)"


def _http_get(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def openalex_by_doi(doi: str) -> dict | None:
    try:
        raw = _http_get(f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi)}")
        return json.loads(raw)
    except Exception as e:
        LOGGER.warning("OpenAlex failed for %s: %s", doi, e)
        return None


def europepmc_pmcid(doi: str) -> str | None:
    q = urllib.parse.quote(f"DOI:{doi}")
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}&format=json&resultType=lite"
    for attempt in range(3):
        try:
            raw = _http_get(url)
            data = json.loads(raw)
            for r in data.get("resultList", {}).get("result", []):
                pmcid = r.get("pmcid")
                if pmcid:
                    return pmcid.replace("PMC", "")
            return None
        except Exception as e:
            LOGGER.warning("EuropePMC search failed for %s (attempt %d): %s", doi, attempt + 1, e)
            time.sleep(2 * (attempt + 1))
    return None


def pmcid_from_openalex(oa: dict) -> str | None:
    """Look in OpenAlex locations for any pmc.ncbi.nlm.nih.gov/articles/PMC<n> URL."""
    pat = re.compile(r"PMC(\d+)")
    for loc in oa.get("locations", []) or []:
        for key in ("pdf_url", "landing_page_url"):
            url = loc.get(key) or ""
            m = pat.search(url)
            if m:
                return m.group(1)
    return None


def ncbi_pmc_xml(pmcid_num: str) -> bytes | None:
    try:
        return _http_get(
            f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={pmcid_num}&rettype=full&retmode=xml",
            timeout=60,
        )
    except Exception as e:
        LOGGER.warning("NCBI efetch failed for PMC%s: %s", pmcid_num, e)
        return None


# Minimal JATS-XML → markdown converter (no external dep).
_NS = {"x": "https://jats.nlm.nih.gov"}


def _node_text(node) -> str:
    parts = []
    if node.text:
        parts.append(node.text)
    for child in node:
        tag = child.tag.split("}")[-1]
        if tag in {"sup", "sub", "italic", "bold", "underline"}:
            parts.append(_node_text(child))
        elif tag == "xref":
            parts.append(_node_text(child))
        elif tag == "ext-link":
            parts.append(_node_text(child))
        else:
            parts.append(_node_text(child))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def jats_to_markdown(xml_bytes: bytes) -> str:
    """Coarse JATS→markdown — keeps section titles and paragraphs."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        return f"<!-- JATS parse error: {e} -->\n"
    out: list[str] = []
    article = root.find(".//article")
    if article is None:
        return "<!-- no <article> in JATS -->\n"

    # Title
    title_el = article.find(".//article-title")
    if title_el is not None:
        out.append(f"# {_node_text(title_el).strip()}\n\n")

    # Abstract
    abstract = article.find(".//abstract")
    if abstract is not None:
        out.append("## Abstract\n\n")
        for p in abstract.iter():
            tag = p.tag.split("}")[-1]
            if tag == "p":
                out.append(_node_text(p).strip() + "\n\n")

    # Body
    body = article.find(".//body")
    if body is not None:
        for sec in body.iter():
            tag = sec.tag.split("}")[-1]
            if tag == "title":
                # depth from ancestors of type 'sec'
                lvl = 2
                par = sec
                while True:
                    par = _parent_map.get(par)
                    if par is None:
                        break
                    if par.tag.split("}")[-1] == "sec":
                        lvl += 1
                lvl = min(lvl, 5)
                out.append(f"\n{'#' * lvl} {_node_text(sec).strip()}\n\n")
            elif tag == "p":
                out.append(_node_text(sec).strip() + "\n\n")

    # Tables - extract caption + simple grid
    for tw in article.iter():
        if tw.tag.split("}")[-1] == "table-wrap":
            cap = tw.find(".//caption")
            if cap is not None:
                out.append(f"\n**Table:** {_node_text(cap).strip()}\n\n")

    return re.sub(r"\n{3,}", "\n\n", "".join(out))


_parent_map: dict = {}


def jats_to_markdown_with_parents(xml_bytes: bytes) -> str:
    global _parent_map
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        return f"<!-- JATS parse error: {e} -->\n"
    _parent_map = {c: p for p in root.iter() for c in p}
    return jats_to_markdown(xml_bytes)


def main() -> None:
    parser = argparse.ArgumentParser(description="Add paper by DOI via PMC/OpenAlex.")
    parser.add_argument("--doi", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--modality", action="append", default=[])
    parser.add_argument("--year", type=int)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    slug = slugify(args.title, year=args.year)
    LOGGER.info("processing %s (slug=%s)", args.doi, slug)

    note = PaperNote(
        id=slug,
        title=args.title,
        doi=args.doi,
        modalities=args.modality or ["other"],
        year=args.year,
        status="seed",
    )
    upsert_note(note)

    md_path = MD_DIR / f"{slug}.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)

    sources: list[str] = []
    body_chunks: list[str] = [f"# {args.title}\n\n", f"<!-- doi: {args.doi} -->\n\n"]

    # 1. OpenAlex metadata
    oa = openalex_by_doi(args.doi)
    abstract_md = ""
    if oa:
        sources.append("openalex")
        # Reconstruct abstract from inverted index
        inv = oa.get("abstract_inverted_index") or {}
        if inv:
            positions: list[tuple[int, str]] = []
            for word, idxs in inv.items():
                for i in idxs:
                    positions.append((i, word))
            positions.sort()
            abstract_md = " ".join(w for _, w in positions)
        body_chunks.append(
            f"<!-- source: openalex -->\n\n## Abstract (OpenAlex)\n\n{abstract_md or '(none)'}\n\n"
        )
        if not args.year:
            args.year = oa.get("publication_year")

    # 2. EuropePMC PMC ID (with OpenAlex fallback)
    pmcid = europepmc_pmcid(args.doi)
    if not pmcid and oa:
        pmcid = pmcid_from_openalex(oa)
        if pmcid:
            LOGGER.info("PMC ID %s recovered from OpenAlex locations", pmcid)
    full_text_ok = False
    if pmcid:
        time.sleep(0.4)
        xml = ncbi_pmc_xml(pmcid)
        if xml and len(xml) > 5000:
            md_text = jats_to_markdown_with_parents(xml)
            if len(md_text) > 1500:
                sources.append(f"pmc-PMC{pmcid}")
                body_chunks.append(
                    f"<!-- source: pmc PMC{pmcid} via NCBI efetch -->\n\n## Full Text (PMC)\n\n{md_text}\n\n"
                )
                full_text_ok = True

    # 3. Decide evidence quality
    if full_text_ok:
        evidence = "full-text" if len(sources) == 2 else "full-text"
    elif abstract_md:
        evidence = "abstract+metadata"
    else:
        evidence = "metadata-only"

    md_path.write_text("".join(body_chunks))

    note.year = args.year
    note.md_path = str(md_path)
    note.status = "fetched" if full_text_ok else "abstract-only"
    note.evidence_quality = evidence
    upsert_note(note)
    print(
        f"{'OK' if full_text_ok else 'PARTIAL'}: {slug}  evidence={evidence} sources={','.join(sources) or '(none)'}"
    )


if __name__ == "__main__":
    main()
