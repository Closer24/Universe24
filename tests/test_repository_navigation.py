"""Keep the monorepo's AI entry points navigable without starting a world."""

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest


def local_links(document):
    text = re.sub(r"```.*?```", "", document.read_text(encoding="utf-8"), flags=re.S)
    for target in re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", text):
        url = urlsplit(target)
        if not url.scheme and not url.netloc:
            path = document.parent / unquote(url.path) if url.path else document
            yield path.resolve(), unquote(url.fragment)


def heading_ids(document):
    seen = set()
    for heading in re.findall(r"^#{1,6}\s+(.+)$", document.read_text(encoding="utf-8"), re.M):
        base = re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
        slug, suffix = base, 0
        while slug in seen:
            suffix += 1
            slug = f"{base}-{suffix}"
        seen.add(slug)
    return seen


def broken_links(document, root):
    failures = []
    for path, fragment in local_links(document):
        if not path.is_relative_to(root) or not path.exists():
            failures.append(str(path))
        elif fragment and path.suffix == ".md" and fragment not in heading_ids(path):
            failures.append(f"{path}#{fragment}")
    return failures


def test_repository_documents_and_skill_routes_are_navigable():
    root = Path(__file__).resolve().parents[1]
    documents = [*root.glob("*.md"), *(root / "docs").rglob("*.md")]
    documents.extend((root / "skills").rglob("*.md"))
    for document in documents:
        assert not broken_links(document, root), (document, broken_links(document, root))
    boss = root / "skills/boss-orchestrator/SKILL.md"
    routes = {path for path, _ in local_links(boss)}
    shared = root / "skills/workflow.md"
    for skill in (root / "skills").glob("*/SKILL.md"):
        assert skill == boss or skill in routes, f"Unrouted Skill: {skill}"
        assert shared in {path for path, _ in local_links(skill)}, skill


@pytest.mark.parametrize(
    "target,valid",
    [
        ("owner.md#one-owner", True),
        ("missing.md", False),
        ("owner.md#absent", False),
        ("#entry", True),
        ("#absent", False),
    ],
)
def test_navigation_detects_missing_files_and_headings(tmp_path, target, valid):
    (tmp_path / "owner.md").write_text("# One owner\n", encoding="utf-8")
    entry = tmp_path / "entry.md"
    entry.write_text(f"# Entry\n[Contract]({target})\n", encoding="utf-8")
    assert (not broken_links(entry, tmp_path)) is valid
