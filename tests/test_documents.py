"""The document lock: only the three, the skills, the entry files and the rendered pages exist; each of the three stays under its cap with no history marker; the rendered pages equal the render and every cited path exists."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tests.worlds import load_file

ROOT = Path(__file__).resolve().parents[1]
RENDER = load_file("render_documents", ROOT / "tools" / "render_documents.py")
THE_THREE = ("docs/ALGEBRA.md", "docs/ENGINE.md", "docs/HIGHLIGHTS.md")
ENTRY_FILES = ("README.md", "AGENTS.md", "CONTRIBUTING.md")
ALLOWED_FOLDERS = ("skills/", "paper/", "docs/generated/")  # the skills, the paper, the rendered pages
CAPS = {
    "docs/ALGEBRA.md": 718,
    "docs/ENGINE.md": 200,
    "docs/HIGHLIGHTS.md": 100,
}  # lines, each of the three
SKIPPED = set(".git .venv venv node_modules __pycache__ .pytest_cache artifacts runs".split())
HISTORY_MARKERS = (
    re.compile(r"\bsuperseded\b", re.IGNORECASE),
    re.compile(r"\bpreviously\b", re.IGNORECASE),
    re.compile(r"\bHISTORY\b"),
    re.compile(r"\brecords? [0-9]{3,4}\b"),
    re.compile(r"\bwas replaced\b", re.IGNORECASE),
)


def markdown_files(root: Path) -> list[str]:
    """Every markdown file of the tree as a posix path from the root; the git and environment folders left out."""
    return sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*.md")
        if not (set(path.relative_to(root).parts[:-1]) & SKIPPED)
    )


def unexpected_documents(root: Path) -> list[str]:
    """Every markdown file that is none of the three, the entry files, a skill's page or a rendered page."""
    allowed = set(THE_THREE) | set(ENTRY_FILES)
    return [
        rel for rel in markdown_files(root) if rel not in allowed and not rel.startswith(ALLOWED_FOLDERS)
    ]


def lines_over_the_cap(root: Path, caps: dict[str, int]) -> list[str]:
    """Every capped document longer than its cap, with both counts."""
    found = []
    for rel, cap in caps.items():
        if not (root / rel).exists():
            continue
        lines = len((root / rel).read_text(encoding="utf-8").splitlines())
        if lines > cap:
            found.append(f"{rel}: {lines} lines, the cap {cap}")
    return found


def history_markers(root: Path, documents: tuple[str, ...]) -> list[str]:
    """Every history marker in the documents, with its line."""
    found = []
    for rel in documents:
        path = root / rel
        if not path.exists():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for marker in HISTORY_MARKERS:
                match = marker.search(line)
                if match:
                    found.append(f"{rel}:{number} {match.group(0)!r}")
                    break
    return found


def test_a_only_the_three_the_skills_the_entry_files_and_the_rendered_pages_exist():
    assert unexpected_documents(ROOT) == []


@pytest.mark.parametrize("document", THE_THREE)
def test_b_each_of_the_three_stays_under_its_line_cap(document: str):
    assert lines_over_the_cap(ROOT, {document: CAPS[document]}) == []


@pytest.mark.parametrize("document", THE_THREE)
def test_c_the_three_hold_no_history_marker(document: str):
    assert history_markers(ROOT, (document,)) == []


def test_d_the_rendered_pages_equal_the_tree_and_every_cited_path_exists():
    """docs/generated/ is what tools/render_documents.py renders from the tree now; every path a document or a skill cites in backticks exists; a decision line naming an absent path says so."""
    assert RENDER.stale_pages(ROOT) == []
    assert RENDER.missing_paths(ROOT) == []
    assert RENDER.unmarked_decisions(ROOT) == []


def tree(tmp_path: Path, files: dict[str, str]) -> Path:
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return tmp_path


def test_each_gate_fails_on_a_small_tree(tmp_path):
    root = tree(
        tmp_path,
        {
            "docs/ALGEBRA.md": "# The law\n",
            "docs/ENGINE.md": "# The engine\n" + "a line\n" * 10,
            "docs/HIGHLIGHTS.md": "# The decisions\n",
            "README.md": "# Entry\n",
            "skills/workflow.md": "# The workflow\n",
            "docs/generated/FILES.md": "# Rendered\n",
        },
    )
    assert unexpected_documents(root) == []
    assert lines_over_the_cap(root, {"docs/ENGINE.md": 11, "docs/ABSENT.md": 5}) == []
    assert lines_over_the_cap(root, {"docs/ENGINE.md": 10}) == ["docs/ENGINE.md: 11 lines, the cap 10"]
    assert history_markers(root, ("docs/ENGINE.md",)) == []
    tree(
        root,
        {
            "docs/OLD_PLAN.md": "# An old plan\n",
            "docs/ENGINE.md": "# The engine\nThis was replaced in record 2251.\nHISTORY: the old law.\n"
            "The well was superseded; previously a seed.\n",
        },
    )
    assert unexpected_documents(root) == ["docs/OLD_PLAN.md"]
    assert history_markers(root, ("docs/ENGINE.md",)) == [
        "docs/ENGINE.md:2 'record 2251'",
        "docs/ENGINE.md:3 'HISTORY'",
        "docs/ENGINE.md:4 'superseded'",
    ]


def test_the_render_check_reads_paths_as_the_documents_cite_them(tmp_path):
    root = tree(
        tmp_path,
        {
            "docs/HIGHLIGHTS.md": "- **A.** `core/rule3.py` and `law/step.json`.\n"
            "- **B.** `core/node.py` waits, ahead of the tree.\n- **C.** `core/node.py` waits.\n",
            "law/step.json": "{}\n",
            "src/event_universe/core/rule3.py": "",
        },
    )
    cited = (
        "`origin/main`, `feature/...`, `x.py:12-14`, `word`, `a/b`, `tools/run.py --list`, `python a/b`"
    )
    assert RENDER.cited_paths(cited) == ["x.py", "a/b", "tools/run.py"]
    assert RENDER.resolves(root, "rule3.py") and RENDER.resolves(root, "runs/out.json")
    assert not RENDER.resolves(root, "core/node.py")
    assert RENDER.unmarked_decisions(root) == [
        "docs/HIGHLIGHTS.md:3 names core/node.py and does not say 'ahead of the tree'"
    ]
