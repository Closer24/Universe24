"""The merge base a gate compares with: its ref (CHECK_BASE, else origin/main), resolved by name, and its tree unpacked for the gate to read (#1198, gate 7: no recorded baseline file); at a release, named by the version bump in pyproject.toml, the released branch's own head before the bump (`released`, the release clause of RELEASE_5_0_PLAN.md, 2026-10-26)."""

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

REBASED = Path(__file__).with_name(
    "check_base.txt"
)  # the commit the gates are re-based on, where one is named


def ancestor(root: Path, commit: str, ref: str) -> bool:
    """Whether `commit` is in the history of `ref` (git merge-base --is-ancestor); False where either cannot be resolved."""
    found = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", commit, ref],
        capture_output=True,
        text=True,
    )
    return found.returncode == 0


def version_at(root: Path, ref: str) -> str | None:
    """The version pyproject.toml names at a ref (its `version = "..."` line), None where the file or the line is absent."""
    found = subprocess.run(
        ["git", "-C", str(root), "show", f"{ref}:pyproject.toml"], capture_output=True, text=True
    )
    for line in found.stdout.splitlines():
        if line.startswith("version = "):
            return line.split('"')[1]
    return None


def released(root: Path, ref: str) -> str | None:
    """The release clause (RELEASE_5_0_PLAN.md, the Boss's 6416419697, 2026-10-26): where HEAD's pyproject.toml names a version the base ref does not, HEAD is the release or carries it, and the ratchets would compare two different engines (the released branch against the former release); their base is then the released branch's own head before the version bump, the parent of the newest commit that set the version line, printed once by name; None where the versions agree."""
    head, base = version_at(root, "HEAD"), version_at(root, ref)
    if head is None or head == base:
        return None
    bump = subprocess.run(
        ["git", "-C", str(root), "log", "-1", "--format=%H", "-G^version = ", "--", "pyproject.toml"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    if not bump or not ancestor(root, f"{bump}~1", "HEAD"):
        return None
    found = resolved(root, f"{bump}~1")
    print(
        f"the release {head} (the version bump {bump[:9]} from {base}): the ratchets' base is the released branch's own head before the bump, {found[:9]}",
        flush=True,
    )
    return found


def base_ref() -> str:
    """The ref the gates compare with: CHECK_BASE, else origin/main; where tools/check_base.txt names a commit in this history that the ref does not hold, that commit (the fold of 2026-10-25: the lean Node's tree is its own base, and every later change holds against it); at a release the released branch's own head before the version bump (`released`)."""
    ref = os.environ.get("CHECK_BASE") or "origin/main"
    root = Path(__file__).resolve().parents[1]
    if REBASED.is_file():
        named = [
            line.strip()
            for line in REBASED.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        if named and ancestor(root, named[0], "HEAD") and not ancestor(root, named[0], ref):
            ref = named[0]
    return released(root, ref) or ref


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
