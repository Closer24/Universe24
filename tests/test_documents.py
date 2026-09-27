"""THE DOCUMENT LOCK (the model owner's decision through the Boss, 2026-09-26 22:01Z; the short
procedure, point 12): the project keeps three current documents (the law, the engine, the
decisions), the skills and the entry files, and nothing else; each of the three stays under a
line cap set when its condensed version lands; none of the three carries a history marker. One
test, selected on every pull request. A gate the tree fails today is marked xfail strict with
its reason; it turns green when the deletion or the condensed document lands and then loses its
mark. Three small trees show each gate fails."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
THE_THREE = ("docs/ALGEBRA.md", "docs/ENGINE.md", "docs/HIGHLIGHTS.md")
ENTRY_FILES = ("README.md", "AGENTS.md", "CONTRIBUTING.md")
ALLOWED_FOLDERS = ("skills/",)
# the line cap of each of the three, set when its condensed version lands; None until then
CAPS: dict[str, int | None] = {
    "docs/ALGEBRA.md": 718,
    "docs/ENGINE.md": 200,
    "docs/HIGHLIGHTS.md": 100,
}
HISTORY_MARKERS = (
    re.compile(r"\bsuperseded\b", re.IGNORECASE),
    re.compile(r"\bpreviously\b", re.IGNORECASE),
    re.compile(r"\bHISTORY\b"),
    re.compile(r"\brecords? [0-9]{3,4}\b"),
    re.compile(r"\bwas replaced\b", re.IGNORECASE),
)


def markdown_files(root: Path) -> list[str]:
    """Every markdown file of the tree, as a posix path relative to the root; the git and
    virtual environment folders left out."""
    skipped = {".git", ".venv", "venv", "node_modules", "__pycache__", "artifacts", "runs"}
    return sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*.md")
        if not (set(path.relative_to(root).parts[:-1]) & skipped)
    )


def unexpected_documents(root: Path) -> list[str]:
    """Every markdown file that is none of the three, the entry files or a skill's page."""
    allowed = set(THE_THREE) | set(ENTRY_FILES)
    return [
        rel for rel in markdown_files(root) if rel not in allowed and not rel.startswith(ALLOWED_FOLDERS)
    ]


def lines_over_the_cap(root: Path, caps: dict[str, int | None]) -> list[str]:
    """Every capped document longer than its cap, with both counts."""
    found = []
    for rel, cap in caps.items():
        if cap is None or not (root / rel).exists():
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


# (a) ONLY THE ALLOWED DOCUMENTS EXIST: switched on in the deletion pull request


@pytest.mark.xfail(
    strict=True,
    reason="the deletion of every other document waits for the newcomer test and the Boss's "
    "deletion pull request; until then the tree holds the old documents",
)
def test_a_only_the_three_the_skills_and_the_entry_files_exist():
    """Point 12: the tree holds the three, the skills and the entry files, and no other
    markdown file."""
    assert unexpected_documents(ROOT) == []


# (b) EACH OF THE THREE STAYS UNDER ITS CAP


@pytest.mark.parametrize("document", THE_THREE)
def test_b_each_of_the_three_stays_under_its_line_cap(document: str):
    """Point 12: a condensed document never grows past the cap written here."""
    if CAPS[document] is None:
        pytest.xfail(f"{document}: no condensed version has landed; its cap is set with it")
    assert lines_over_the_cap(ROOT, {document: CAPS[document]}) == []


# (c) THE THREE HOLD NO HISTORY MARKER


@pytest.mark.parametrize("document", THE_THREE)
def test_c_the_three_hold_no_history_marker(document: str):
    """Point 12: no superseded, previously, HISTORY, record NNNN or was replaced in the
    three; the day's log and git keep the history."""
    if CAPS[document] is None:
        pytest.xfail(f"{document}: the condensed version, without its history, has not landed")
    assert history_markers(ROOT, (document,)) == []


# THE SMALL TREES: each gate fails where it should


def tree(tmp_path: Path, files: dict[str, str]) -> Path:
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return tmp_path


def test_an_extra_document_fails_the_allowed_list(tmp_path):
    root = tree(
        tmp_path,
        {
            "docs/ALGEBRA.md": "# The law\n",
            "docs/ENGINE.md": "# The engine\n",
            "docs/HIGHLIGHTS.md": "# The decisions\n",
            "README.md": "# Entry\n",
            "skills/workflow.md": "# The workflow\n",
            "skills/boss-orchestrator/SKILL.md": "# The Boss\n",
        },
    )
    assert unexpected_documents(root) == []
    tree(root, {"docs/OLD_PLAN.md": "# An old plan\n", "notes/README.md": "# Notes\n"})
    assert unexpected_documents(root) == ["docs/OLD_PLAN.md", "notes/README.md"]


def test_a_document_over_its_cap_fails(tmp_path):
    root = tree(tmp_path, {"docs/ENGINE.md": "# The engine\n" + "a line\n" * 10})
    assert lines_over_the_cap(root, {"docs/ENGINE.md": 11}) == []
    assert lines_over_the_cap(root, {"docs/ENGINE.md": 10}) == ["docs/ENGINE.md: 11 lines, the cap 10"]
    assert lines_over_the_cap(root, {"docs/ENGINE.md": None, "docs/ABSENT.md": 5}) == []


def test_a_history_marker_fails(tmp_path):
    root = tree(tmp_path, {"docs/ENGINE.md": "# The engine\nThe loop steps the lattice.\n"})
    assert history_markers(root, ("docs/ENGINE.md",)) == []
    tree(
        root,
        {
            "docs/ENGINE.md": "# The engine\nThis was replaced in record 2251.\nHISTORY: the old law.\n"
            "The well was superseded; previously a seed.\n"
        },
    )
    assert history_markers(root, ("docs/ENGINE.md",)) == [
        "docs/ENGINE.md:2 'record 2251'",
        "docs/ENGINE.md:3 'HISTORY'",
        "docs/ENGINE.md:4 'superseded'",
    ]
