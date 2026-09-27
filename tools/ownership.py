"""One owner per area (#1198, gate 8): a pull request touching another owner's area fails without that owner's hand-over line in its body.

The map is `tools/owners.json`: per owner its sessions and its areas (a path, or a folder
ending in "/"); the longest area that holds a path names its owner, and a path in no area is
free. The author is the owner whose session link is the last one in the body (the body's
closing attribution). A hand-over is a line "HANDED BY <owner>: <files>", the files separated
by commas or spaces, a folder ending in "/" covering what it holds. CI passes the body as
PR_BODY; the check runs on a pull request, or locally with PR_BODY set, never on a push to main.

Usage: `PR_BODY="$(cat body.md)" python tools/ownership.py` prints every file touched without
its owner's hand-over.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from merge_base import base_ref, on_pull_request, resolved  # noqa: E402

OWNERS = ROOT / "tools" / "owners.json"
SESSION = re.compile(r"claude\.ai/code/(session_\w+)")
HANDED = re.compile(r"^\s*HANDED BY (?P<owner>[^:]+):(?P<files>.*)$")


def load_owners(path: Path = OWNERS) -> dict[str, dict[str, list[str]]]:
    owners: dict[str, dict[str, list[str]]] = json.loads(path.read_text(encoding="utf-8"))["owners"]
    return owners


def covers(area: str, path: str) -> bool:
    return path == area or (area.endswith("/") and path.startswith(area))


def owner_of(path: str, owners: dict[str, dict[str, list[str]]]) -> str | None:
    """The owner of the longest area holding `path`; None where the path is free."""
    held = [
        (len(area), name)
        for name, entry in owners.items()
        for area in entry["areas"]
        if covers(area, path)
    ]
    return max(held)[1] if held else None


def author(body: str, owners: dict[str, dict[str, list[str]]]) -> str | None:
    """The owner whose session link is the body's last one; None when the body names no owner's session."""
    links = SESSION.findall(body)
    if not links:
        return None
    return next((name for name, entry in owners.items() if links[-1] in entry["sessions"]), None)


def handed(body: str) -> dict[str, list[str]]:
    """Per owner, the files and folders its hand-over lines name."""
    found: dict[str, list[str]] = {}
    for line in body.splitlines():
        if match := HANDED.match(line):
            found.setdefault(match["owner"].strip(), []).extend(
                re.split(r"[,\s]+", match["files"].strip())
            )
    return found


def violations(changed: list[str], body: str, owners: dict[str, dict[str, list[str]]]) -> list[str]:
    """One line per changed file of another owner's area that no hand-over of that owner names."""
    writer = author(body, owners)
    given = handed(body)
    found = []
    for path in changed:
        owner = owner_of(path, owners)
        if owner is None or owner == writer:
            continue
        if any(covers(entry, path) for entry in given.get(owner, []) if entry):
            continue
        who = writer or "a body with no owner's session link"
        found.append(
            f"{path} is {owner}'s area and {who} touches it: add 'HANDED BY {owner}: {path}' to the body"
        )
    return found


def changed_files(root: Path, ref: str) -> list[str]:
    """The files the pull request changes against its merge base, untracked files included."""

    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args], capture_output=True, text=True, cwd=root, check=True
        ).stdout

    base = git("merge-base", resolved(root, ref), "HEAD").strip()
    return sorted(
        set(git("diff", "--name-only", base).splitlines())
        | set(git("ls-files", "--others", "--exclude-standard").splitlines())
    )


def main() -> None:
    """Print every file touched without its owner's hand-over; exit 1 when there is one."""
    if not on_pull_request(dict(os.environ)):
        print("the ownership check runs on a pull request, or with PR_BODY set")
        return
    found = violations(changed_files(ROOT, base_ref()), os.environ.get("PR_BODY", ""), load_owners())
    print("\n".join(found) or "every touched area is its author's or handed over")
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
