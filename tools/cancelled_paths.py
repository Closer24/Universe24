"""The one list of the ray law's cancelled paths (docs/CANCELLED_WORLDS.md; the model owner's
records 1875 and 2095, the Boss's records 2102 and 2133): read from that document's tables, so
the gate (tests/conftest.py), the change selector (tools/check.py) and the test
(tests/test_cancelled_paths.py) all read the same list. Nothing is deleted; a cancelled path
stays in the checkout until the owner deletes it."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCUMENT = ROOT / "docs" / "CANCELLED_WORLDS.md"
SECTIONS = {
    "folders": "## 2. ",
    "tests": "## 3. ",
    "modules": "## 4. ",
    "partial": "## 5. ",
    "documents": "## 6. ",
}
ROW = re.compile(r"^\| `([^`]+)` \|")


def cancelled_paths(section: str, document: Path = DOCUMENT) -> tuple[str, ...]:
    """The paths of one section's table, in the document's order: `folders` (world folders),
    `tests` (test files), `modules` (modules and tools cancelled whole), `partial` (modules
    cancelled in part, which stay imported) or `documents`."""
    heading = SECTIONS[section]
    paths: list[str] = []
    inside = False
    for line in document.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            inside = line.startswith(heading)
            continue
        if inside and (match := ROW.match(line)):
            paths.append(match.group(1))
    if not paths:
        raise ValueError(f"{document}: no table rows under the section {heading!r}")
    return tuple(paths)


def is_cancelled(path: str, document: Path = DOCUMENT) -> bool:
    """True for a path listed whole (a test, a module, a tool, a document) or under a cancelled
    world folder; a module cancelled in part is not cancelled."""
    whole = set(cancelled_paths("tests", document)) | set(cancelled_paths("modules", document))
    whole |= set(cancelled_paths("documents", document))
    if path in whole:
        return True
    return any(
        path == folder or path.startswith(folder + "/")
        for folder in cancelled_paths("folders", document)
    )
