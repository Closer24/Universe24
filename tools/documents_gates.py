"""The documents' six gates on the law's text, the engine's document and the repository's words, run by `tools/check.py` among its ratchets on every selection (since 2026-10-24, the tests' audit on the owner's word; to that day the first three by `tests/test_documents.py`, the last by `tests/test_repository_language.py`; the owner's word of 2026-10-04, a perfect algebra; the advisor's proposals, #1793 comment 5974878000): (1) no undated history clause stands in docs/ALGEBRA.md or docs/ENGINE.md beyond the ones `tools/history_allowed.json` lists, and no listed clause has left the text without leaving the list, so the list only shrinks; (2) every number of `tools/numbers.json` stands in one of its canonical forms where the table names it and in none of its forbidden forms in the two documents; (3) every number the table derives by a script of `tools/derivations/` is that script's output to the digits named; (4) every heading of docs/*.md, README.md and CHANGELOG.md is in sentence case and no run of three or more all-caps words stands in their prose or in the docstrings, comments and strings of src/, tools/ and tests/ (the owner's word of 2026-09-30); (5) ENGINE.md's "The engine is N modules" counts the Python files of src/tensor24/engine beside __init__.py (src/event_universe's until the old engine left the tree, the owner's word of 2026-10-30); (6) every tracked or new text file holds ASCII letters only (the repository's language is English).

Usage: `python tools/documents_gates.py` prints every departure; `python tools/documents_gates.py --history` prints the history clauses standing now in the list's own form, to refresh `tools/history_allowed.json` after a fill that dates or strikes some.
"""

from __future__ import annotations

import ast
import importlib.util
import io
import json
import re
import subprocess
import sys
import tokenize
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = ("docs/ALGEBRA.md", "docs/ENGINE.md")
ALLOWED, NUMBERS = ROOT / "tools" / "history_allowed.json", ROOT / "tools" / "numbers.json"
ENTRY = ("README.md", "CHANGELOG.md")  # the entry documents, under gate (4) with docs/*.md
CODE = ("src", "tools", "tests")  # the folders whose docstrings, comments and strings gate (4) reads
CAPS = re.compile(r"[A-Z][A-Z0-9'-]+")
HEADING = re.compile(r"(\d+\.\s+)?[A-Z](?![A-Z0-9'-]*\s+[A-Z][A-Z0-9'-]+(\s|$))")
WORDS = {  # the counted words gate (5) reads
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "twenty-one": 21,
    "twenty-two": 22,
    "twenty-three": 23,
    "twenty-four": 24,
    "twenty-five": 25,
    "twenty-six": 26,
    "twenty-seven": 27,
    "twenty-eight": 28,
    "twenty-nine": 29,
    "thirty": 30,
    "thirty-one": 31,
    "thirty-two": 32,
    "thirty-three": 33,
    "thirty-four": 34,
}
TEXT = (".py", ".md", ".json", ".toml", ".txt", ".yml")  # the text files gate (6) reads
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


def shouting(text: str) -> list[str]:
    """Every run of three or more all-caps words in a text, code spans aside."""
    words = [word.strip('.,;:()[]"!?*') for word in re.sub(r"`[^`]*`", " ", text).split()]
    marked = " ".join(word if CAPS.fullmatch(word) else "\n" for word in words)  # a break between runs
    return [run.group(0) for run in re.finditer(r"\S+(?: \S+){2,}", marked)]


def prose(path: Path) -> list[str]:
    """A markdown file's lines outside its fenced blocks, a fenced line blank."""
    lines, fenced = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        fenced ^= line.lstrip().startswith("```")
        lines.append("" if fenced or line.lstrip().startswith("```") else line)
    return lines


def capitals(root: Path = ROOT) -> list[str]:
    """The departures of gate (4): a heading not in sentence case (a number and a dot before it allowed, its first two words not both in capitals), or a run of three or more all-caps words in the documents' prose or in the code's docstrings, comments and strings (a code token such as LAWFUL is one word)."""
    documents = sorted((root / "docs").glob("*.md")) + [root / name for name in ENTRY]
    lines = [(path.relative_to(root), line) for path in documents for line in prose(path)]
    heads = [(at, line) for at, line in lines if re.match(r"#+\s", line)]
    found = [
        f"{at}: a heading not in sentence case: {line}"
        for at, line in heads
        if not HEADING.match(line.lstrip("#").strip())
    ]
    found += [f"{at}: a run of capitals: {run}" for at, line in lines for run in shouting(line)]
    for path in [p for folder in CODE for p in sorted((root / folder).rglob("*.py"))]:
        source = path.read_text(encoding="utf-8")
        texts = [n.value for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Constant)]
        texts = [text for text in texts if isinstance(text, str)]
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        texts += [t.string for t in tokens if t.type == tokenize.COMMENT]
        found += [
            f"{path.relative_to(root)}: a run of capitals: {run}" for t in texts for run in shouting(t)
        ]
    return found


def module_count(root: Path = ROOT) -> list[str]:
    """The departure of gate (5): ENGINE.md's "The engine is N modules" against the Python files of src/tensor24/engine beside __init__.py."""
    text = (root / "docs" / "ENGINE.md").read_text(encoding="utf-8")
    stated = re.search(r"The engine is ([a-z-]+) modules", text)
    found = sorted(
        p.name for p in (root / "src" / "tensor24" / "engine").glob("*.py") if p.name != "__init__.py"
    )
    if stated is None or stated.group(1) not in WORDS:
        return ["docs/ENGINE.md: no sentence 'The engine is N modules' with N a counted word"]
    if WORDS[stated.group(1)] != len(found):
        return [
            f"docs/ENGINE.md: 'The engine is {stated.group(1)} modules'; the tree holds {len(found)}: {found}"
        ]
    return []


def ascii_letters(root: Path = ROOT) -> list[str]:
    """The departures of gate (6): every letter of every tracked or new text file is an ASCII letter (no Hebrew, Greek or Cyrillic letter in the prose, no directory exempt); a dash, a sign or a symbol is no letter and passes."""
    git = ["git", "ls-files", "--cached", "--others", "--exclude-standard"]
    listed = subprocess.check_output(git, cwd=root, text=True).splitlines()
    found = []
    for name in (n for n in listed if n.endswith(TEXT) and (root / n).is_file()):
        for number, line in enumerate((root / name).read_text(encoding="utf-8").splitlines(), 1):
            found += [f"{name}:{number}: {c!r}" for c in line if c.isalpha() and not c.isascii()]
    return found


def main() -> int:
    if "--history" in sys.argv:
        print(json.dumps(clauses(), indent=1))
        return 0
    departures = (
        undated_history() + numbers() + derived() + capitals() + module_count() + ascii_letters()
    )
    print("\n".join(departures[:40]) if departures else "the documents' six gates hold")
    return 1 if departures else 0


if __name__ == "__main__":
    sys.exit(main())
