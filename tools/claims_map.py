"""The claims map, docs/CLAIMS.md, written from the proofs' inventory (tools/derivations/proofs_inventory.json): every theorem, lemma, identity and quantitative claim of the law, the paper and its supplement as one row with its place, its statement, its ground, its kind, its verdict and the function that checks it, so a reader finds every claim beside its check in one document. The rule it serves: the map is generated and never edited by hand, the same inventory giving the same bytes, and `tests/test_claims_map.py` holds the file equal to what this script writes, so the map and the inventory cannot drift apart; a row's check runs in `tests/test_proofs_check_the_law.py`, which asserts its verdict. The inventory's words stand as they are, with two forms of the rendering: a pipe inside a table cell is a slash, so the table stays well formed, and a row id named in a row's text stands in a code span (`L17`), a cross-reference and not a word of the sentence, which the documents gate's rule on runs of capitals (tests/test_documents.py) exempts.

Usage: `python tools/claims_map.py` writes docs/CLAIMS.md; `python tools/claims_map.py --check` prints one line naming where docs/CLAIMS.md departs from what it would write and exits 1, or exits 0 where the two are equal byte for byte.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "tools" / "derivations" / "proofs_inventory.json"
MAP = ROOT / "docs" / "CLAIMS.md"
COLUMNS = ("id", "name", "place", "kind", "verdict")
TITLE = "# The claims map"
OPENING = (
    "Every theorem, lemma, identity and quantitative claim of the law (docs/ALGEBRA.md), the paper and "
    "its supplement, as the proofs' inventory quotes them at the heads its header names (the law at "
    "3a334eeb, the paper and the supplement at d7e97674, the long version), stands here as one row, "
    "generated from tools/derivations/proofs_inventory.json by "
    "tools/claims_map.py, so the two cannot drift apart (tests/test_claims_map.py). Each row names where "
    "the claim stands, its exact statement, the ground its check stands on, its kind and its verdict, and "
    "the function that checks it; tests/test_proofs_check_the_law.py runs every check and asserts every "
    "verdict, so a green run of `python -m pytest tests/test_proofs_check_the_law.py -q` runs every check "
    "of the map to its verdict; the rows with no check stand as statements only, and a witness is not a "
    "proof."
)
LEGEND = (
    "**The kinds and the verdicts.** The kinds, in the words of tools/derivations/README.md: (A) an exact "
    "identity, checked in Python's integers, `fractions.Fraction` and Gaussian rationals at random integer "
    "witnesses with the symmetric cases forced; (B) a series expansion with its order, checked by the "
    "residual against the exact function at two step sizes, the ratio 2^order the test of the order; (C) a "
    "hand proof with a numerical witness only, the witness recomputed where a script exists and the row "
    "counted as unchecked; (D) a statement of the engine's structure that only a test of the engine shows, "
    'the engine\'s tests named and no check here. The verdicts: "holds" (the check returns true), '
    '"witness only" (a hand proof with a numerical witness, the check a witness and not a proof), '
    '"finding" (the statement as printed at the place named is false and the check reproduces the '
    "mismatch; the commits, what was found and what was done about it stand in docs/ERRATA.md), "
    '"none" (no check, the row stands as a statement only).'
)


def rows(path: Path = INVENTORY) -> list[dict[str, Any]]:
    """The inventory's rows, in the inventory's order."""
    return json.loads(path.read_text(encoding="utf-8"))["rows"]


def named(ids: frozenset[str]) -> re.Pattern[str] | None:
    """The pattern of a row id standing as a whole word in a text, or None where there is no row."""
    return re.compile(r"\b(" + "|".join(sorted(ids)) + r")\b") if ids else None


def text(value: Any, ids: re.Pattern[str] | None) -> str:
    """A field's text: a string unchanged, any other value as compact JSON; a row id it names in a code span."""
    shown = value if isinstance(value, str) else json.dumps(value, separators=(",", ":"))
    return ids.sub(r"`\1`", shown) if ids else shown


def cell(value: Any, ids: re.Pattern[str] | None) -> str:
    """A table cell: the field's text with every pipe replaced by a slash, so the table stays well formed."""
    return text(value, ids).replace("|", "/")


def section(row: dict[str, Any], ids: re.Pattern[str] | None) -> list[str]:
    """One row's section: its heading and its lines, a blank line after each."""
    check = row["check"]
    lines = [
        f"## {row['id']}. {text(row['name'], ids)}",
        f"**Place.** {text(row['place'], ids)}",
        f"**Statement.** {text(row['statement'], ids)}",
        f"**Ground.** {text(row['ground'], ids)}",
        f"**Kind and verdict.** {row['kind']}, {row['verdict']}.",
        f"**Check.** {check['module']}, `{check['function']}`" if check else "**Check.** none.",
    ]
    if "note" in row:
        lines.append(f"**Note.** {text(row['note'], ids)}")
    if "far_regime_witness" in row:
        lines.append(f"**Far-regime witness.** {text(row['far_regime_witness'], ids)}")
    if row["verdict"] == "finding":
        lines.append("**Finding.** See docs/ERRATA.md.")
    return [line for pair in lines for line in (pair, "")]


def render(inventory: list[dict[str, Any]]) -> str:
    """The whole map as text: the title, the opening, the legend, the summary table and one section per row."""
    ids = named(frozenset(row["id"] for row in inventory))
    table = ["| " + " | ".join(COLUMNS) + " |", "| " + " | ".join("---" for _ in COLUMNS) + " |"]
    table += [
        "| " + " | ".join(cell(row[c], None if c == "id" else ids) for c in COLUMNS) + " |"
        for row in inventory
    ]
    lines = [TITLE, "", OPENING, "", LEGEND, "", *table, ""]
    for row in inventory:
        lines += section(row, ids)
    return "\n".join(lines).rstrip("\n") + "\n"


def departure(rendered: str, path: Path = MAP) -> str | None:
    """One line naming how the file departs from the rendered text (missing, or the first line that differs), or None where the two are equal byte for byte."""
    name = path.relative_to(ROOT).as_posix()
    if not path.is_file():
        return f"{name} is missing: run python tools/claims_map.py"
    standing = path.read_bytes()
    if standing == rendered.encode("utf-8"):
        return None
    old, new = standing.decode("utf-8", errors="replace").splitlines(), rendered.splitlines()
    pairs = enumerate(zip(old, new, strict=False), 1)
    at = next((i for i, (a, b) in pairs if a != b), min(len(old), len(new)) + 1)
    return (
        f"{name} departs from the inventory's map at line {at} ({len(old)} lines against {len(new)}): "
        "run python tools/claims_map.py"
    )


def main(argv: list[str]) -> int:
    inventory = rows()
    rendered = render(inventory)
    name = MAP.relative_to(ROOT).as_posix()
    if "--check" in argv:
        found = departure(rendered)
        print(found or f"{name} is the inventory's map, {len(inventory)} rows")
        return 1 if found else 0
    MAP.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"{name} written, {len(inventory)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
