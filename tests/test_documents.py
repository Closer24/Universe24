"""The documents gate (the owner's word of 2026-09-30): every markdown heading of the documents begins with a capital letter and is no run of capitals, and no run of three or more all-caps words stands in their prose or in the docstrings, comments and strings of src/, tools/ and tests/ (a code token such as LAWFUL is one word)."""

import ast
import importlib.util
import io
import re
import tokenize
from pathlib import Path

ROOT, ENTRY = Path(__file__).resolve().parents[1], ("README.md", "CHANGELOG.md")
DOCUMENTS = sorted((ROOT / "docs").glob("*.md")) + [ROOT / name for name in ENTRY]
CODE = [path for folder in ("src", "tools", "tests") for path in sorted((ROOT / folder).rglob("*.py"))]
CAPS = re.compile(r"[A-Z][A-Z0-9'-]+")
HEADING = re.compile(r"(\d+\.\s+)?[A-Z](?![A-Z0-9'-]*\s+[A-Z][A-Z0-9'-]+(\s|$))")


def shouting(text: str) -> list[str]:
    """Every run of three or more all-caps words in a text, code spans aside."""
    words = [word.strip('.,;:()[]"!?*') for word in re.sub(r"`[^`]*`", " ", text).split()]
    marked = " ".join(word if CAPS.fullmatch(word) else "\n" for word in words)  # a break between runs
    return [run.group(0) for run in re.finditer(r"\S+(?: \S+){2,}", marked)]


def prose(path: Path) -> list[str]:  # a markdown file's lines outside its fenced blocks
    lines, fenced = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        fenced ^= line.lstrip().startswith("```")
        lines.append("" if fenced or line.lstrip().startswith("```") else line)
    return lines


def test_every_heading_is_in_sentence_case_and_no_name_is_written_in_capitals():
    """(a) Every heading of the documents begins with a capital letter (a number and a dot before it allowed) and its first two words are not both in capitals; (b) no run of three or more all-caps words in the documents' prose, code spans and fenced blocks aside, or in the code's docstrings, comments and strings."""
    lines = [(path.relative_to(ROOT), line) for path in DOCUMENTS for line in prose(path)]
    heads = [(at, line) for at, line in lines if re.match(r"#+\s", line)]
    headings = [f"{at}: {line}" for at, line in heads if not HEADING.match(line.lstrip("#").strip())]
    assert not headings, headings
    loud, texts = [f"{at}: {run}" for at, line in lines for run in shouting(line)], []
    for path in CODE:  # every comment and string literal of the file, its docstrings among them
        source = path.read_text(encoding="utf-8")
        nodes = [n for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Constant)]
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        texts += [(path.relative_to(ROOT), n.value) for n in nodes if isinstance(n.value, str)]
        texts += [(path.relative_to(ROOT), t.string) for t in tokens if t.type == tokenize.COMMENT]
    loud += [f"{at}: {run}" for at, text in texts for run in shouting(text)]
    assert not loud, loud


def gates():  # the documents' three gates, loaded by path
    spec = importlib.util.spec_from_file_location(
        "documents_gates", ROOT / "tools" / "documents_gates.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_no_undated_history_clause_stands_in_the_law_or_the_engines_document():
    """Gate (1) of tools/documents_gates.py: every history clause of docs/ALGEBRA.md and docs/ENGINE.md is in tools/history_allowed.json, and the list only shrinks."""
    assert not gates().undated_history(ROOT), gates().undated_history(ROOT)[:20]


def test_every_shared_number_stands_in_its_one_form():
    """Gate (2): every number of tools/numbers.json stands in a canonical form where the table names one and in no forbidden form."""
    assert not gates().numbers(ROOT), gates().numbers(ROOT)[:20]


def test_every_derived_number_is_its_scripts_output():
    """Gate (3): every number the table derives is the output of its script under tools/derivations/, to the digits named."""
    assert not gates().derived(), gates().derived()[:20]
