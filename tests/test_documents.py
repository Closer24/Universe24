"""The documents gate (the owner's word of 2026-09-30): every markdown heading of the documents begins with a capital letter and is no run of capitals, and no run of three or more all-caps words stands in their prose or in the docstrings, comments and strings of src/, tools/ and tests/ (a code token such as LAWFUL is one word)."""

from __future__ import annotations

import ast
import io
import re
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ("README.md", "CONTRIBUTING.md", "AGENTS.md")
DOCUMENTS = sorted((ROOT / "docs").glob("*.md")) + [ROOT / name for name in ENTRY]
DOCUMENTS += sorted((ROOT / "skills").rglob("*.md"))
CODE = [path for folder in ("src", "tools", "tests") for path in sorted((ROOT / folder).rglob("*.py"))]
CAPS = re.compile(r"[A-Z][A-Z0-9'-]+")
HEADING = re.compile(r"(\d+\.\s+)?[A-Z](?![A-Z0-9'-]*\s+[A-Z][A-Z0-9'-]+(\s|$))")


def shouting(text: str) -> list[str]:
    """Every run of three or more all-caps words in a text, code spans aside."""
    found, run = [], []
    for word in re.sub(r"`[^`]*`", " ", text).split() + [""]:
        bare = word.strip('.,;:()[]"!?*')
        if CAPS.fullmatch(bare):
            run.append(bare)
            continue
        if len(run) >= 3:
            found.append(" ".join(run))
        run = []
    return found


def prose(path: Path) -> list[str]:
    """A markdown file's lines outside its fenced blocks."""
    lines, fenced = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        fenced ^= line.lstrip().startswith("```")
        lines.append("" if fenced or line.lstrip().startswith("```") else line)
    return lines


def written(path: Path) -> list[str]:
    """A Python file's comments and string literals (its docstrings among them)."""
    source = path.read_text(encoding="utf-8")
    nodes = [
        n
        for n in ast.walk(ast.parse(source))
        if isinstance(n, ast.Constant) and isinstance(n.value, str)
    ]
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    return [n.value for n in nodes] + [t.string for t in tokens if t.type == tokenize.COMMENT]


def test_every_heading_is_in_sentence_case_and_no_name_is_written_in_capitals():
    """(a) Every heading of the documents begins with a capital letter (a number and a dot before it allowed) and its first two words are not both in capitals; (b) no run of three or more all-caps words in the documents' prose, code spans and fenced blocks aside, or in the code's docstrings, comments and strings."""
    headings = [
        f"{path.relative_to(ROOT)}: {line}"
        for path in DOCUMENTS
        for line in prose(path)
        if re.match(r"#+\s", line) and not HEADING.match(line.lstrip("#").strip())
    ]
    assert not headings, headings
    loud = [
        f"{path.relative_to(ROOT)}: {run}"
        for path in DOCUMENTS
        for line in prose(path)
        for run in shouting(line)
    ]
    loud += [
        f"{path.relative_to(ROOT)}: {run}"
        for path in CODE
        for text in written(path)
        for run in shouting(text)
    ]
    assert not loud, loud
