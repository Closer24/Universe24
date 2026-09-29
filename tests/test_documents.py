"""The document lock: only the three, the skills and the entry files exist; each of the three stays under its cap with no history marker; every path a document or a skill cites in backticks exists in the tree."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
THE_THREE = ("docs/ALGEBRA.md", "docs/ENGINE.md", "docs/HIGHLIGHTS.md")
ENTRY_FILES = ("README.md", "AGENTS.md", "CONTRIBUTING.md")
ALLOWED_FOLDERS = ("skills/", "paper/")  # the skills' pages and the paper's own folder
CAPS = {
    "docs/ALGEBRA.md": 880,
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
SUFFIXES = (".py", ".md", ".json", ".yml", ".txt", ".svg", ".toml", ".cff")
# a git ref or a run's folder, no path of the tree
REFS = ("origin/", "feature/", "exp/", "artifacts/", "runs/")
CITED = re.compile(r"`([^`\n]+)`")


def markdown_files(root: Path) -> list[str]:
    """Every markdown file of the tree as a posix path from the root; the git and environment folders left out."""
    return sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*.md")
        if not (set(path.relative_to(root).parts[:-1]) & SKIPPED)
    )


def unexpected_documents(root: Path) -> list[str]:
    """Every markdown file that is none of the three, the entry files or a skill's page."""
    allowed = set(THE_THREE) | set(ENTRY_FILES)
    return [
        rel for rel in markdown_files(root) if rel not in allowed and not rel.startswith(ALLOWED_FOLDERS)
    ]


def lines_over_the_cap(root: Path, caps: dict[str, int]) -> list[str]:
    """Every capped document longer than its cap, with both counts."""
    lines = {
        rel: len((root / rel).read_text(encoding="utf-8").splitlines())
        for rel in caps
        if (root / rel).exists()
    }
    return [
        f"{rel}: {count} lines, the cap {caps[rel]}" for rel, count in lines.items() if count > caps[rel]
    ]


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


def cited_paths(text: str) -> list[str]:
    """Every backticked token that reads as a path: a command's first word, its line numbers dropped."""
    found = []
    for token in CITED.findall(text):
        token = re.sub(r":\d+(?:-\d+)?$", "", token.split()[0]) if token.strip() else ""
        if re.fullmatch(r"[\w./-]+", token) and ("/" in token or token.endswith(SUFFIXES)):
            if "..." not in token and not token.startswith(REFS):
                found.append(token)
    return found


def missing_paths(root: Path) -> list[str]:
    """Every cited path of the three, the entry files and the skills that the tree lacks, as document:line path."""
    skills, found = sorted(p.relative_to(root).as_posix() for p in (root / "skills").rglob("*.md")), []
    for rel in (*THE_THREE, *ENTRY_FILES, *skills):
        if not (root / rel).exists():
            continue
        for number, line in enumerate((root / rel).read_text(encoding="utf-8").splitlines(), 1):
            for token in cited_paths(line):
                as_written, in_package = (
                    (root / token).exists(),
                    (root / "src/event_universe" / token).exists(),
                )
                if not (as_written or in_package or ("/" not in token and any(root.rglob(token)))):
                    found.append(f"{rel}:{number} {token}")
    return found


def test_a_only_the_three_the_skills_and_the_entry_files_exist():
    assert unexpected_documents(ROOT) == []


@pytest.mark.parametrize("document", THE_THREE)
def test_b_each_of_the_three_stays_under_its_line_cap(document: str):
    assert lines_over_the_cap(ROOT, {document: CAPS[document]}) == []


@pytest.mark.parametrize("document", THE_THREE)
def test_c_the_three_hold_no_history_marker(document: str):
    assert history_markers(ROOT, (document,)) == []


def test_d_every_path_a_document_or_a_skill_cites_exists():
    assert missing_paths(ROOT) == []


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
            "skills/workflow.md": "# The workflow, see `docs/ENGINE.md` and `origin/main`\n",
        },
    )
    assert unexpected_documents(root) == []
    assert lines_over_the_cap(root, {"docs/ENGINE.md": 11, "docs/ABSENT.md": 5}) == []
    assert lines_over_the_cap(root, {"docs/ENGINE.md": 10}) == ["docs/ENGINE.md: 11 lines, the cap 10"]
    assert history_markers(root, ("docs/ENGINE.md",)) == [] and missing_paths(root) == []
    assert cited_paths("`x.py:3-4`, `word`, `a/b`, `python a/b`, `core/...`") == ["x.py", "a/b"]
    tree(
        root,
        {
            "docs/OLD_PLAN.md": "# An old plan\n",
            "docs/ENGINE.md": "# The engine\nThis was replaced in record 2251.\nHISTORY: the old law.\n"
            "The well was superseded; previously a seed.\n",
            "skills/x.md": "see `core/node.py` and `law/step.json`\n",
        },
    )
    assert unexpected_documents(root) == ["docs/OLD_PLAN.md"]
    assert history_markers(root, ("docs/ENGINE.md",)) == [
        "docs/ENGINE.md:2 'record 2251'",
        "docs/ENGINE.md:3 'HISTORY'",
        "docs/ENGINE.md:4 'superseded'",
    ]
    assert missing_paths(root) == ["skills/x.md:1 core/node.py", "skills/x.md:1 law/step.json"]
