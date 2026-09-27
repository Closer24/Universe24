"""The merge base a gate compares with: its ref (CHECK_BASE, else origin/main), resolved by name, and its tree unpacked for the gate to read (#1198, gate 7: no recorded baseline file)."""

from __future__ import annotations

import io
import os
import subprocess
import tarfile
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any


def base_ref() -> str:
    return os.environ.get("CHECK_BASE") or "origin/main"


def on_pull_request(environment: dict[str, str]) -> bool:
    """A check of the pull request's body runs on a pull request, or locally where PR_BODY is set; never on a push to main."""
    event = environment.get("GITHUB_EVENT_NAME")
    return event == "pull_request" or (event is None and "PR_BODY" in environment)


def resolved(root: Path, ref: str) -> str:
    """The commit `ref` names; a ref git cannot resolve fails by name, never passes silently."""
    try:
        return subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
            capture_output=True,
            text=True,
            cwd=root,
            check=True,
        ).stdout.strip()
    except OSError, subprocess.CalledProcessError:
        raise ValueError(
            f"the merge base {ref!r} cannot be resolved: fetch it or set CHECK_BASE"
        ) from None


def moved_since(root: Path, ref: str) -> dict[str, str]:
    """Each file git reads as moved since the merge base, its new path to its old one: a moved file keeps its old path's counts."""
    git = ["git", "-C", str(root)]
    base = subprocess.run(
        [*git, "merge-base", resolved(root, ref), "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    lines = subprocess.run(
        [*git, "diff", "-M", "--name-status", "--diff-filter=R", base],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    return {new: old for _, old, new in (line.split("\t") for line in lines)}


def carried(files: dict[str, Any], root: Path, ref: str) -> dict[str, Any]:
    """The merge base's counts per file, a moved file's under its new path."""
    moved = {old: new for new, old in moved_since(root, ref).items()}
    return {moved.get(rel, rel): counts for rel, counts in files.items()}


@contextmanager
def tree_at(root: Path, ref: str, folders: tuple[str, ...]) -> Iterator[Path]:
    """The given folders of the tree at `ref`, unpacked in a temporary directory for as long as the block runs."""
    commit = resolved(root, ref)
    present = subprocess.run(
        ["git", "ls-tree", "--name-only", commit, "--", *folders],
        capture_output=True,
        text=True,
        cwd=root,
        check=True,
    ).stdout.split()
    with tempfile.TemporaryDirectory() as directory:
        if present:
            archive = subprocess.run(
                ["git", "archive", "--format=tar", commit, "--", *present],
                capture_output=True,
                cwd=root,
                check=True,
            ).stdout
            with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
                tar.extractall(directory, filter="data")
        yield Path(directory)
