"""Rewrite the old numbered citations of docs/ALGEBRA.md to the condensed law's anchors (issue #1198, item 4 (e)).

The table `tools/algebra_anchors.json` is the mathematician's table on PR #1209: each old
section 9.NN and the anchor that now carries it, null where the section was history. A
citation group is "ALGEBRA.md" (or "ALGEBRA") followed by one or more section references
joined by commas, semicolons or "and"; each reference with its qualifiers ("(4)", "(a)",
"item 5", "items 3, 11") becomes its anchor, repeated anchors once. A group whose sections
were all history becomes "ALGEBRA.md" alone. A bare run of references reads as a citation
when its first one carries a qualifier or stands alone in brackets, and is written with
"ALGEBRA.md" in front; any other bare "9.NN" is left as it is and listed, for a hand to read.

Usage: `python tools/rewrite_algebra_citations.py` lists what would change;
`python tools/rewrite_algebra_citations.py --write` rewrites the files.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "tools" / "algebra_anchors.json"
SCOPES = ("src", "tools", "tests", "examples")
SUFFIXES = (".py", ".md")
QUALIFIER = r"(?:,?\s*\((?:\d+[a-z]?|[a-z]|[ivx]+)\))"
ITEMS = r"(?:\s+items?\s+\d+[a-z]?(?:(?:,\s*|\s+and\s+|\s+to\s+)\d+[a-z]?)*)"
REFERENCE = rf"9\.\d{{1,3}}(?![\d.]){QUALIFIER}*{ITEMS}?{QUALIFIER}*"
SEPARATOR = r"(?:\s*[,;]\s*|\s+and\s+)"
GROUP = re.compile(
    rf"(?P<name>ALGEBRA(?:\.md)?)\s+(?P<refs>{REFERENCE}(?:{SEPARATOR}(?:ALGEBRA(?:\.md)?\s+)?{REFERENCE})*)"
)
SECTION = re.compile(r"9\.(\d{1,3})(?![\d.])")
BARE = re.compile(r"(?<![\d.#\w])9\.\d{1,3}(?![\d.])")
# a bare run of references reads as a citation when its first one carries a qualifier, or it
# stands inside brackets: "(9.22 (4): ...", "9.113 item 2", "(9.111)"
CITED = rf"(?:9\.\d{{1,3}}(?![\d.])(?:{QUALIFIER}|{ITEMS})+|(?<=\()9\.\d{{1,3}}(?=[);:,]))"
BARE_GROUP = re.compile(
    rf"(?<![\d.#\w])(?P<refs>(?:{CITED}){QUALIFIER}*{ITEMS}?{QUALIFIER}*(?:{SEPARATOR}{REFERENCE})*)"
)


def load_table(path: Path = TABLE) -> dict[str, str | None]:
    loaded: dict[str, str | None] = json.loads(path.read_text(encoding="utf-8"))["sections"]
    return loaded


def rewrite(text: str, table: dict[str, str | None]) -> tuple[str, list[str]]:
    """The text with every citation rewritten, and the old sections the table does not hold."""
    unknown: set[str] = set()

    def anchored(name: str, refs: str, original: str) -> str:
        anchors: list[str] = []
        for number in SECTION.findall(refs):
            key = f"9.{number}"
            if key not in table:
                unknown.add(key)
                return original
            anchor = table[key]
            if anchor is not None and anchor not in anchors:
                anchors.append(anchor)
        return f"{name} {', '.join(anchors)}" if anchors else name

    text = GROUP.sub(lambda m: anchored(m["name"], m["refs"], m[0]), text)
    text = BARE_GROUP.sub(lambda m: anchored("ALGEBRA.md", m["refs"], m[0]), text)
    return text, sorted(unknown)


def bare_references(text: str) -> list[str]:
    """The "9.NN" left outside a citation group, for a hand to read."""
    return BARE.findall(text)


def files(root: Path) -> list[Path]:
    found: list[Path] = []
    for scope in SCOPES:
        base = root / scope
        if base.is_dir():
            found.extend(p for p in sorted(base.rglob("*")) if p.suffix in SUFFIXES and p.is_file())
    own = {TABLE.name, Path(__file__).name, "test_rewrite_algebra_citations.py"}
    return [p for p in found if "__pycache__" not in p.parts and p.name not in own]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="rewrite the files in place")
    args = parser.parse_args()
    table = load_table()
    changed = groups = bare = 0
    for path in files(ROOT):
        text = path.read_text(encoding="utf-8")
        new, unknown = rewrite(text, table)
        if unknown:
            print(f"{path.relative_to(ROOT)}: sections not in the table: {sorted(set(unknown))}")
        left = bare_references(new)
        bare += len(left)
        if new != text:
            changed += 1
            groups += len(GROUP.findall(text))
            if args.write:
                path.write_text(new, encoding="utf-8")
    verb = "rewrote" if args.write else "would rewrite"
    print(f"{verb} {groups} citation groups in {changed} files; {bare} bare references left for a hand")


if __name__ == "__main__":
    main()
