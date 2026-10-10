"""The references: every \\cite key of arrow.tex exists in refs.bib or refs_more.bib, every entry of the two .bib files is cited, the first paper's entry prints its DOI once (read from arrow.bbl), and every entry is verified against its record: for a DOI, the Crossref record (https://api.crossref.org/works/<doi>), its title (case and punctuation folded), first author's family name, year, volume and first page against the .bib; for the two Zenodo DOIs, the Zenodo record (https://zenodo.org/api/records/<id>), its title, creator and version; an entry without a DOI is marked as checked by hand against the journal's record. The fetched records are cached under papers/spacetime_events/refs_check/ (committed), so the check runs offline once they are there; a record that cannot be fetched passes with a warning, a MISMATCH fails. Usage: python3 -I check_refs.py."""
from __future__ import annotations
from pathlib import Path
import json
import os
import re
import ssl
import subprocess
import sys
import unicodedata
import urllib.request

CACHE = Path(__file__).resolve().parent.parent / "refs_check"
BY_HAND = {  # entries without a DOI: checked by hand against the journal's record
    "loschmidt1876": "Sitzungsberichte der Akademie der Wissenschaften zu Wien, mathematisch-naturwissenschaftliche Classe 73, 128-142 (1876)",
    "boltzmann1877": "Sitzungsberichte der Kaiserlichen Akademie der Wissenschaften, Mathematisch-Naturwissenschaftliche Classe 76, 373-435 (1877)",
    "zuse1969": "Rechnender Raum, Vieweg, Braunschweig (1969)",
    "wolfram2002": "A New Kind of Science, Wolfram Media, Champaign (2002)",
}


def fold(text: str) -> str:
    """Case, accents, braces and punctuation folded, for comparing titles and names."""
    text = re.sub(r"\\ss\b", "ss", text)  # the German sharp s
    text = re.sub(r"\\[\"'^`~=.]", "", text)  # accent commands: \"o, \'e, ...
    text = re.sub(r"\\[a-zA-Z]+|[{}\\]", "", text)
    text = re.sub(r"<[^>]+>", " ", text)  # a record's markup, <i>...</i>
    text = unicodedata.normalize("NFKD", text.replace("ß", "ss"))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def bib_entries() -> dict[str, dict[str, str]]:
    out = {}
    for fname in ("refs.bib", "refs_more.bib"):
        text = (CACHE.parent / fname).read_text(encoding="utf-8")
        for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", text, flags=re.S):
            fields = {"type": m.group(1)}
            for f in re.finditer(r"(\w+)\s*=\s*\{(.*?)\}\s*,?\s*\n", m.group(3) + "\n", flags=re.S):
                fields[f.group(1).lower()] = " ".join(f.group(2).split())
            out[m.group(2).strip()] = fields
    return out


def fetch(url: str, cache_file: Path) -> dict | None:
    """The record from the cache, else fetched and cached; None when unreachable."""
    if cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))
    data = None
    for attempt in range(3):
        try:
            ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or os.environ.get("CURL_CA_BUNDLE") or None)
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "arrow.tex check_refs (mailto:alon@defounder.ai)"}), timeout=40, context=ctx) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                break
        except Exception:
            try:
                out = subprocess.run(["curl", "-sS", "-m", "40", url], capture_output=True, text=True, timeout=60).stdout
                data = json.loads(out)
                break
            except Exception:
                data = None
    if data is not None:
        CACHE.mkdir(exist_ok=True)
        cache_file.write_text(json.dumps(data, indent=0, ensure_ascii=False) + "\n", encoding="utf-8")
    return data


def verify(key: str, e: dict[str, str]) -> tuple[str, str]:
    """('ok' | 'MISMATCH' | 'not reachable' | 'by hand', detail) for one entry."""
    doi = e.get("doi")
    if not doi:
        return ("by hand", BY_HAND.get(key, "no DOI, no hand record")) if key in BY_HAND else ("MISMATCH", "no DOI and no hand record")
    if doi.startswith("10.5281/zenodo."):
        rec = fetch(f"https://zenodo.org/api/records/{doi.split('.')[-1]}", CACHE / f"{key}.zenodo.json")
        if rec is None:
            return "not reachable", f"zenodo {doi}"
        m = rec.get("metadata", {})
        bad = []
        if fold(m.get("title", "")) != fold(e.get("title", "")):
            bad.append(f"title (record: {m.get('title')})")
        creators = [fold(c.get("name", "")) for c in m.get("creators", [])]
        if fold(e.get("author", "")) not in creators:
            bad.append(f"creator (record: {creators})")
        if str(m.get("publication_date", ""))[:4] != e.get("year", ""):
            bad.append(f"year (record: {m.get('publication_date')})")
        version = m.get("version", "")
        concept = (rec.get("conceptdoi") or "").lower() == doi.lower()  # a concept DOI resolves to the latest version and names none
        if version and not concept and version not in e.get("howpublished", "") and version not in e.get("note", "") and version not in e.get("title", ""):
            bad.append(f"version (record: {version})")
        if (rec.get("doi") or "").lower() != doi.lower() and (rec.get("conceptdoi") or "").lower() != doi.lower():
            bad.append("doi")
        return ("MISMATCH", "; ".join(bad)) if bad else ("ok", f"zenodo {doi}, version {version}")
    rec = fetch(f"https://api.crossref.org/works/{doi}", CACHE / f"{key}.crossref.json")
    if rec is None:
        return "not reachable", f"crossref {doi}"
    m = rec.get("message", {})
    bad = []
    rt = fold(" ".join(m.get("title", [])))
    bt = fold(e.get("title", ""))
    if not (bt == rt or bt in rt or rt in bt):
        bad.append(f"title (record: {' '.join(m.get('title', []))})")
    first_author = (m.get("author") or [{}])[0]
    first_family = fold(first_author.get("family") or first_author.get("name", ""))  # a collaboration is listed by its name, no family
    bib_family = fold(e.get("author", "").split(" and ")[0].split(",")[0])
    if first_family != bib_family and not (bib_family and (bib_family in first_family or first_family in bib_family)):
        bad.append(f"first author (record: {first_family})")
    years = {str(((m.get(k) or {}).get("date-parts") or [[None]])[0][0]) for k in ("issued", "published-print", "published-online")}
    year = str(((m.get("issued") or {}).get("date-parts") or [[None]])[0][0])
    if e.get("year", "") not in years:
        bad.append(f"year (record: {sorted(years)})")
    if e.get("volume") and m.get("volume"):  # a book's series volume is not in its record
        rv = re.sub(r"^.*?(\d+)$", r"\1", str(m.get("volume", "")))
        if rv != e.get("volume"):
            bad.append(f"volume (record: {m.get('volume')})")
    if e.get("pages"):
        rp = str(m.get("page") or m.get("article-number") or "").split("-")[0]  # an article number stands for the pages
        bp = e.get("pages", "").replace("--", "-").split("-")[0]
        if rp != bp:
            bad.append(f"pages (record: {m.get('page')}, article number {m.get('article-number')})")
    return ("MISMATCH", "; ".join(bad)) if bad else ("ok", f"crossref {doi}: {year}, vol. {m.get('volume')}, pp. {m.get('page') or m.get('article-number')}")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import PAPER, read_tex


def main() -> int:
    tex = read_tex()
    cited = set()
    for m in re.finditer(r"\\cite\{([^}]*)\}", tex):
        cited.update(k.strip() for k in m.group(1).split(","))
    entries = {}
    for fname in ("refs.bib", "refs_more.bib"):
        text = (PAPER / fname).read_text(encoding="utf-8")
        for m in re.finditer(r"@\w+\{([^,]+),", text):
            entries[m.group(1).strip()] = fname
    problems = []
    for k in sorted(cited - set(entries)):
        problems.append(f"cited but not in a .bib: {k}")
    for k in sorted(set(entries) - cited):
        problems.append(f"in {entries[k]} but never cited: {k}")
    bbl = PAPER / "arrow.bbl"
    if bbl.exists():
        text = bbl.read_text(encoding="utf-8")
        items = text.split("\\bibitem")
        entry = next((it for it in items if it.lstrip().startswith("{first}") or re.match(r"\s*\[[^\]]*\]\{first\}", it)), None)
        if entry is None:
            problems.append("no printed entry with the key 'first'")
        else:
            n = entry.count("10.5281/zenodo.23190113")
            if n != 1:
                problems.append(f"the first paper's entry prints the DOI {n} times, once required")
        if "v1.1.0" in text:
            problems.append("the tag v1.1.0 is printed")
    else:
        problems.append("no arrow.bbl to check the printed entry")
    print(f"check_refs: {len(cited)} keys cited, {len(entries)} entries in the .bib files")
    # every entry against its record
    for key, e in bib_entries().items():
        status, detail = verify(key, e)
        print(f"  {status:13} {key:16} {detail}")
        if status == "MISMATCH":
            problems.append(f"{key}: {detail}")
        elif status == "not reachable":
            print(f"  warning: {key} could not be fetched; the record is not cached under refs_check/")
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  " + p)
        return 1
    print("the references pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
