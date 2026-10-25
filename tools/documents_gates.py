"""The documents' three gates on the law's text and the engine's document, run by `tests/test_documents.py` (the owner's word of 2026-10-04, a perfect algebra; the advisor's proposals, #1793 comment 5974878000): (1) no undated history clause stands in docs/ALGEBRA.md or docs/ENGINE.md beyond the ones `tools/history_allowed.json` lists, and no listed clause has left the text without leaving the list, so the list only shrinks; (2) every number of `tools/numbers.json` stands in one of its canonical forms where the table names it and in none of its forbidden forms in the two documents; (3) every number the table derives by a script of `tools/derivations/` is that script's output to the digits named.

Usage: `python tools/documents_gates.py` prints every departure; `python tools/documents_gates.py --history` prints the history clauses standing now in the list's own form, to refresh `tools/history_allowed.json` after a fill that dates or strikes some.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = ("docs/ALGEBRA.md", "docs/ENGINE.md")
ALLOWED, NUMBERS = ROOT / "tools" / "history_allowed.json", ROOT / "tools" / "numbers.json"
HISTORY = [  # a clause about the state of the work, which the law states dated or not at all
    re.compile(p, re.IGNORECASE)
    for p in (
        r"\b(?:the engine|the law|the algebra|rule3|the gate|the engine's line|the engine's round)"
        r"[^.;]{0,40}?\bas it stands\b",
        r"\bpending\b",
        r"\bnot yet (?:run|built|asserted|stood|implemented|merged|landed|in the engine|a line)\b",
        r"\buntil the (?:engine )?round(?: lands)?\b",
        r"\bthe engine runs today\b",
        r"\bis being checked\b",
        r"\bthe engine's to-do\b",
        r"\ba round of its own\b",
        r"\bthe next version\b",
        r"\btoday\b",
        r"\btonight\b",
        r"\bmerging\b",
        r"\bthis round\b",
        r"\buntil the (?:act|round) lands\b",
        r"\b(?:since|before) the locality round\b",
        r"\bpresent convention\b",
    )
]
WINDOW = 36  # the characters kept on either side of a clause, its key in the list


def clauses(root: Path = ROOT) -> list[dict[str, str]]:
    """Every history clause standing in the two documents: the file, the clause and its context, the key of the list."""
    found = []
    for name in DOCUMENTS:
        text = (root / name).read_text(encoding="utf-8")
        for pattern in HISTORY:
            for match in pattern.finditer(text):
                context = " ".join(text[max(0, match.start() - WINDOW) : match.end() + WINDOW].split())
                found.append({"file": name, "clause": match.group(0).lower(), "context": context})
    return found


def undated_history(root: Path = ROOT) -> list[str]:
    """The departures of gate (1): a clause the list does not hold, and a listed clause the text no longer holds."""
    listed = json.loads(ALLOWED.read_text(encoding="utf-8"))
    keys = {(entry["file"], entry["context"]) for entry in listed}
    standing = {(entry["file"], entry["context"]) for entry in clauses(root)}
    new = [
        f"{f}: a history clause the law states dated or not at all: ...{c}..."
        for f, c in sorted(standing - keys)
    ]
    gone = [
        f"{f}: listed clause gone from the text, strike it from tools/history_allowed.json: ...{c}..."
        for f, c in sorted(keys - standing)
    ]
    return new + gone


def numbers(root: Path = ROOT) -> list[str]:
    """The departures of gate (2): a forbidden form standing, or no canonical form standing where the table names one."""
    table, departures = json.loads(NUMBERS.read_text(encoding="utf-8")), []
    texts = {name: (root / name).read_text(encoding="utf-8") for name in DOCUMENTS}
    for entry in table:
        files = entry.get("files", list(DOCUMENTS))
        for name in files:
            departures += [
                f"{name}: {entry['name']}: the forbidden form {form!r} stands"
                for form in entry.get("forbidden", ())
                if form in texts[name]
            ]
        if entry.get("canonical") and not any(
            form in texts[name] for name in files for form in entry["canonical"]
        ):
            departures.append(
                f"{entry['name']}: no canonical form of {entry['canonical']} stands in {files}"
            )
    return departures


def derived() -> list[str]:
    """The departures of gate (3): a table number its script does not return to the digits named; a rule's `arguments`, where it has them, are the table's own inputs passed to the function (a run's reading among them, which no derivation module holds)."""
    table, departures = json.loads(NUMBERS.read_text(encoding="utf-8")), []
    for entry in (e for e in table if "derivation" in e):
        rule: dict[str, Any] = entry["derivation"]
        spec = importlib.util.spec_from_file_location(Path(rule["module"]).stem, ROOT / rule["module"])
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        found = getattr(module, rule["function"])(*rule.get("arguments", []))
        values = [round(float(v), rule["digits"]) for v in found]
        expected = [round(float(v), rule["digits"]) for v in rule["expected"]]
        if values != expected:
            departures.append(
                f"{entry['name']}: {rule['module']}:{rule['function']} returns {values}, the table holds {expected}"
            )
    return departures


def main() -> int:
    if "--history" in sys.argv:
        print(json.dumps(clauses(), indent=1))
        return 0
    departures = undated_history() + numbers() + derived()
    print("\n".join(departures) if departures else "the documents' three gates hold")
    return 1 if departures else 0


if __name__ == "__main__":
    sys.exit(main())
