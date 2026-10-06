"""Check every bibliography entry with a DOI against Crossref.

Usage: python crossref_check.py main.tex [supplement.tex ...]. For each \\bibitem the DOI is read from its
\\href, Crossref's record is fetched with curl, and the entry's text is checked for the record's volume, year
and first page and for the title's first words; the mismatches and the entries without a DOI are printed.
Needs the network; the entries are fetched once each across the files.
"""

import html
import json
import re
import subprocess
import sys


def entries(text: str) -> dict[str, tuple[str | None, str]]:
    start = text.find("\\begin{thebibliography}")
    end = text.find("\\end{thebibliography}")
    found: dict[str, tuple[str | None, str]] = {}
    for item in re.findall(r"\\bibitem\{[^}]*\}.*?(?=\\bibitem\{|$)", text[start:end], re.S):
        key = re.match(r"\\bibitem\{([^}]*)\}", item).group(1)
        doi = re.search(r"doi\.org/([^}\s]+)\}", item)
        plain = re.sub(r"\\href\{[^}]*\}\{[^}]*\}", "", item)
        plain = re.sub(r"\\[a-zA-Z]+|[{}$]", "", plain)
        found[key] = (doi.group(1) if doi else None, plain.strip())
    return found


def crossref(doi: str) -> dict:
    result = subprocess.run(
        ["curl", "-sS", "--max-time", "25", f"https://api.crossref.org/works/{doi}"],
        capture_output=True,
        text=True,
        timeout=40,
    )
    return json.loads(result.stdout)["message"]


def problems(record: dict, text: str) -> list[str]:
    found: list[str] = []
    volume = record.get("volume", "")
    year = (record.get("issued", {}).get("date-parts") or [[None]])[0][0]
    page = record.get("page", "") or record.get("article-number", "")
    title = html.unescape((record.get("title") or [""])[0]).lower()
    if volume and volume not in text:
        found.append(f"volume {volume}")
    if year and str(year) not in text:
        found.append(f"year {year}")
    first_page = page.split("-")[0].lstrip("0") if page else ""
    if first_page and first_page not in text:
        found.append(f"page {page}")
    title_words = re.findall(r"[a-z]{5,}", title)[:6]
    lowered = text.lower()
    if title_words and sum(word in lowered for word in title_words) < max(1, len(title_words) // 2):
        found.append(f"title {title[:60]!r}")
    return found


def main() -> None:
    seen: dict[str, tuple[str | None, str]] = {}
    for name in sys.argv[1:]:
        for key, value in entries(open(name, encoding="utf-8").read()).items():
            seen.setdefault(key, value)
    print(len(seen), "entries")
    for key, (doi, text) in seen.items():
        if not doi:
            print(key, "| no DOI |", text[:100])
            continue
        try:
            record = crossref(doi)
        except Exception as error:  # noqa: BLE001 (the network's own failures are reported, not raised)
            print(key, "| Crossref failed |", doi, str(error)[:80])
            continue
        found = problems(record, text)
        if found:
            print(key, "|", doi, "|", "; ".join(found))


if __name__ == "__main__":
    main()
