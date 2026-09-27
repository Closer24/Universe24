"""Host-only expiry of explicitly owned generated artifacts, with writer leases."""

import argparse
import hashlib
import json
import math
import os
import shutil
import stat
import sys
import time
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from uuid import uuid4

REGISTRY = ".event-universe-retention"
MAX_AGE_SECONDS = 86400
_PROTECTED = {
    ".git",
    ".agents",
    ".codex",
    ".venv",
    "venv",
    "node_modules",
    "src",
    "tests",
    "examples",
    "config",
    "configs",
    "configurations",
    "skills",
    "docs",
    "site-packages",
    REGISTRY,
}
_SOURCE_FILES = {"agents.md", "readme.md", "pyproject.toml", "manifest.in", ".gitignore", ".env"}


def _link(path: Path) -> bool:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    )


def _lexical_path(path: Path) -> Path:
    candidate = path if path.is_absolute() else Path.cwd() / path
    current = Path(candidate.anchor)
    for part in candidate.parts[1:]:
        current /= part
        if _link(current):
            raise ValueError(f"retention refuses a symlink or reparse path: {current}")
    return candidate.resolve()


def validate_output_path(path: Path) -> None:
    """Validate a prospective output before creating it or scanning its parent."""
    resolved = _lexical_path(Path(path))
    if resolved == Path(resolved.anchor):
        raise ValueError("a filesystem root cannot be an artifact output")
    if any(part.casefold() in _PROTECTED for part in resolved.parts):
        raise ValueError("source, configuration and environment directories are protected")
    if resolved.name.casefold() in _SOURCE_FILES or resolved.suffix.casefold() in {".py", ".toml"}:
        raise ValueError("source and original configuration files are protected")
    if (resolved / ".git").exists() or (resolved / "pyproject.toml").exists():
        raise ValueError("a source checkout cannot be an artifact output")


def _root(path: Path) -> Path:
    resolved = _lexical_path(Path(path))
    if resolved == Path(resolved.anchor):
        raise ValueError("a filesystem root cannot own a retention registry")
    if any(part.casefold() in _PROTECTED for part in resolved.parts):
        raise ValueError("retention does not scan source or configuration directories")
    return resolved


def _tree(path: Path) -> Iterator[Path]:
    """Inspect without following links; reject protected content in owned directories."""
    if _link(path):
        raise ValueError(f"retention refuses linked content: {path}")
    if path.name.casefold() == REGISTRY:
        raise ValueError("a nested managed output cannot be recursively removed")
    if path.name.casefold() in _PROTECTED or path.name.casefold() in _SOURCE_FILES:
        raise ValueError(f"retention refuses protected content: {path}")
    if path.suffix.casefold() in {".py", ".toml"}:
        raise ValueError(f"retention refuses source content: {path}")
    yield path
    if path.is_dir():
        for child in path.iterdir():
            yield from _tree(child)


def _target(root: Path, value: Path) -> Path:
    if ".." in value.parts:
        raise ValueError("retention targets cannot contain parent traversal")
    lexical = value if value.is_absolute() else root / value
    validate_output_path(lexical)
    resolved = _lexical_path(lexical)
    if resolved == root or not resolved.is_relative_to(root):
        raise ValueError("retention target must be strictly inside its registry root")
    if any(part.casefold() == REGISTRY for part in resolved.relative_to(root).parts):
        raise ValueError("retention cannot register its own registry")
    return resolved


def _identity(path: Path) -> tuple[int, int, bool]:
    info = path.lstat()
    if not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)) or _link(path):
        raise ValueError("only ordinary generated files and directories can be registered")
    return info.st_dev, info.st_ino, stat.S_ISDIR(info.st_mode)


class _Lock:
    def __init__(self, path: Path) -> None:
        if _link(path):
            raise ValueError("retention lock cannot be a link")
        self.stream = path.open("a+b")
        if self.stream.seek(0, os.SEEK_END) == 0:
            self.stream.write(b"\0")
            self.stream.flush()
        self.stream.seek(0)
        self.held = False
        try:
            if sys.platform == "win32":
                import msvcrt

                msvcrt.locking(self.stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.held = True
        except OSError:
            self.stream.close()

    def close(self) -> None:
        """Release the lock if held and close its file."""
        if self.held:
            self.stream.seek(0)
            if sys.platform == "win32":
                import msvcrt

                msvcrt.locking(self.stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.stream.fileno(), fcntl.LOCK_UN)
            self.held = False
            self.stream.close()


def _catalog_lock(path: Path) -> _Lock:
    """Wait briefly for another host transaction; writer probes remain nonblocking."""
    deadline = time.monotonic() + 5
    while True:
        lock = _Lock(path)
        if lock.held:
            return lock
        if time.monotonic() >= deadline:
            raise RuntimeError("retention registry remained busy for five seconds")
        time.sleep(0.01)


def _number(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and value >= 0
    )


def _read(path: Path) -> dict[str, Any]:
    if _link(path):
        raise ValueError("retention record cannot be a link")
    entry = json.loads(path.read_text(encoding="utf-8"))
    if (
        not isinstance(entry, dict)
        or entry.get("record_form") != 1
        or entry.get("id") != path.stem
        or not _number(entry.get("started_at"))
        or not isinstance(entry.get("targets"), list)
        or not isinstance(entry.get("keep_alive_with", []), list)
        or (entry.get("finished_at") is not None and not _number(entry["finished_at"]))
    ):
        raise ValueError("invalid retention record")
    for target in entry["targets"]:
        if (
            not isinstance(target, dict)
            or not isinstance(target.get("path"), str)
            or Path(target["path"]).is_absolute()
            or ".." in Path(target["path"]).parts
            or type(target.get("device")) is not int
            or type(target.get("inode")) is not int
            or type(target.get("directory")) is not bool
        ):
            raise ValueError("invalid retention target record")
    for dependency in entry.get("keep_alive_with", []):
        if (
            not isinstance(dependency, str)
            or Path(dependency).is_absolute()
            or ".." in Path(dependency).parts
        ):
            raise ValueError("invalid retention dependency record")
    return entry


def _write(path: Path, entry: dict[str, Any]) -> None:
    temporary = path.with_name(f".{uuid4().hex}.tmp")
    try:
        temporary.write_text(json.dumps(entry, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


@contextmanager
def _catalog(root: Path) -> Iterator[Path]:
    """Serialize overlapping parent and child registries in ancestor order."""
    locks = []
    registry = root / REGISTRY
    try:
        for parent in (*reversed(root.parents), root):
            candidate = parent / REGISTRY
            if _link(candidate):
                raise ValueError("retention registry cannot be a link")
            if parent == root:
                candidate.mkdir(exist_ok=True)
            elif not candidate.is_dir():
                continue
            lock = _catalog_lock(candidate / "registry.lock")
            locks.append(lock)
            if parent != root:
                for path in candidate.glob("*.json"):
                    entry = _read(path)
                    for item in entry["targets"]:
                        owned = _target(parent, Path(item["path"]))
                        if root == owned or root.is_relative_to(owned):
                            raise ValueError("a parent registry already owns this output directory")
        yield registry
    finally:
        for lock in reversed(locks):
            lock.close()


def _same(path: Path, item: dict[str, Any]) -> bool:
    return _identity(path) == (item["device"], item["inode"], item["directory"])


def _quarantine(registry: Path, token: object) -> Path:
    if (
        not isinstance(token, str)
        or len(token) != 32
        or any(character not in "0123456789abcdef" for character in token)
    ):
        raise ValueError("invalid artifact quarantine identity")
    path = registry / f".deleting-{token}"
    _lexical_path(path)
    return path


def _overlap(a: Path, b: Path) -> bool:
    return a == b or a.is_relative_to(b) or b.is_relative_to(a)


def _register(
    root: Path,
    paths: Sequence[Path],
    finished_at: float | None,
    keep_alive_with: Sequence[Path] = (),
    expected_identities: Sequence[tuple[int, int, bool]] | None = None,
) -> tuple[Path, _Lock]:
    targets = [_target(root, Path(path)) for path in paths]
    dependencies = [_target(root, Path(path)) for path in keep_alive_with]
    if expected_identities is not None and (
        len(expected_identities) != len(targets)
        or any(
            len(identity) != 3
            or type(identity[0]) is not int
            or type(identity[1]) is not int
            or type(identity[2]) is not bool
            for identity in expected_identities
        )
    ):
        raise ValueError("expected artifact identities must match the target list")
    if not targets or any(_overlap(a, b) for i, a in enumerate(targets) for b in targets[i + 1 :]):
        raise ValueError("register distinct, non-overlapping artifact paths")
    for target in targets:
        if not target.exists():
            raise ValueError("create the owned empty output directory or file before leasing it")
        list(_tree(target))
    with _catalog(root) as registry:
        identifier = uuid4().hex
        path = registry / f"{identifier}.json"
        lock = _Lock(registry / f"{identifier}.lock")
        if not lock.held:
            raise RuntimeError("could not acquire artifact writer lease")
        prior_locks = []
        try:
            changes = []
            for old_path in registry.glob("*.json"):
                entry = _read(old_path)
                retained = [
                    item
                    for item in entry["targets"]
                    if not any(_overlap(_target(root, Path(item["path"])), p) for p in targets)
                ]
                if len(retained) == len(entry["targets"]):
                    continue
                if any(
                    item.get("quarantine") is not None
                    and _quarantine(registry, item["quarantine"]).exists()
                    for item in entry["targets"]
                    if item not in retained
                ):
                    raise RuntimeError("previous cleanup of this artifact must finish before reuse")
                old_lock = _Lock(old_path.with_suffix(".lock"))
                if not old_lock.held:
                    raise RuntimeError("artifact path already has an active writer")
                prior_locks.append(old_lock)
                changes.append((old_path, {**entry, "targets": retained}))
            encoded = []
            for index, target in enumerate(targets):
                device, inode, directory = _identity(target)
                if expected_identities is not None and (device, inode, directory) != tuple(
                    expected_identities[index]
                ):
                    raise ValueError("artifact differs from the verified adoption generation")
                encoded.append(
                    {
                        "path": target.relative_to(root).as_posix(),
                        "device": device,
                        "inode": inode,
                        "directory": directory,
                    }
                )
            started = time.time() if finished_at is None else finished_at
            entry = {
                "record_form": 1,
                "id": identifier,
                "started_at": started,
                "finished_at": finished_at,
                "expires_at": None if finished_at is None else finished_at + MAX_AGE_SECONDS,
                "targets": encoded,
                "keep_alive_with": [p.relative_to(root).as_posix() for p in dependencies],
            }
            _write(path, entry)
            for old_path, updated in changes:
                _write(old_path, updated)
            return path, lock
        except BaseException:
            lock.close()
            path.unlink(missing_ok=True)
            path.with_suffix(".lock").unlink(missing_ok=True)
            raise
        finally:
            for old_lock in prior_locks:
                old_lock.close()


class ArtifactLease:
    """Acquire at construction; keep all writers alive until finish or context exit."""

    def __init__(
        self, root: Path, paths: Sequence[Path], *, keep_alive_with: Sequence[Path] = ()
    ) -> None:
        self.root = _root(root)
        self.path, self._lock = _register(self.root, paths, None, keep_alive_with)
        self._closed = False

    def __enter__(self) -> ArtifactLease:
        return self

    def __exit__(self, *exc: object) -> None:
        self.finish()

    def finish(self) -> None:
        """Finish the lease once: record its targets in the catalog and release its lock."""
        if self._closed:
            return
        try:
            with _catalog(self.root):
                entry = _read(self.path)
                for item in entry["targets"]:
                    target = _target(self.root, Path(item["path"]))
                    if target.exists() and not _same(target, item):
                        raise ValueError("artifact path was replaced during its writer lease")
                finished = time.time()
                _write(
                    self.path,
                    {**entry, "finished_at": finished, "expires_at": finished + MAX_AGE_SECONDS},
                )
        finally:
            self._closed = True
            self._lock.close()

    def close(self) -> None:
        """Finish the lease (the alias the writers call)."""
        self.finish()


def adopt_artifacts(
    root: Path,
    paths: Sequence[Path],
    finished_at: float,
    *,
    expected_identities: Sequence[tuple[int, int, bool]] | None = None,
) -> None:
    """Explicitly enroll verified existing generated outputs, never infer ownership."""
    if not _number(finished_at):
        raise ValueError("finished_at must be a finite nonnegative timestamp")
    _, lock = _register(_root(root), paths, finished_at, expected_identities=expected_identities)
    lock.close()


def _registries(root: Path) -> Iterator[Path]:
    if not root.is_dir():
        return
    if _link(root):
        raise ValueError("cleanup root cannot be a linked directory")
    registry = root / REGISTRY
    if registry.exists():
        if _link(registry):
            raise ValueError("retention registry cannot be a link")
        yield root
    for child in root.iterdir():
        if child.name.casefold() == REGISTRY or child.name.casefold() in _PROTECTED or _link(child):
            continue
        if child.is_dir() and not (child / ".git").exists() and not (child / "pyproject.toml").exists():
            yield from _registries(child)


def _active_dependency(root: Path, entry: dict[str, Any], current: Path) -> bool:
    """Probe while the owner catalog serializes descendant registry mutations."""
    for value in entry.get("keep_alive_with", []):
        dependency = _target(root, Path(value))
        for parent in dependency.parents:
            if not parent.is_relative_to(root):
                break
            registry = parent / REGISTRY
            if _link(registry):
                raise ValueError("retention dependency registry cannot be a link")
            if not registry.is_dir():
                continue
            for path in registry.glob("*.json"):
                if path == current:
                    continue
                candidate = _read(path)
                owns_dependency = any(
                    dependency == (target := _target(parent, Path(item["path"])))
                    or dependency.is_relative_to(target)
                    for item in candidate["targets"]
                )
                if owns_dependency:
                    lock = _Lock(path.with_suffix(".lock"))
                    if not lock.held:
                        return True
                    lock.close()
    return False


def cleanup_expired(
    root: Path,
    *,
    now: float | None = None,
    max_age_seconds: float = MAX_AGE_SECONDS,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Delete expired registered generations only; active locks always take priority."""
    current = time.time() if now is None else now
    if not _number(current) or not _number(max_age_seconds) or max_age_seconds <= 0:
        raise ValueError("retention time and positive maximum age must be finite")
    report: dict[str, Any] = {"deleted": [], "skipped": [], "errors": [], "next_expiry": None}
    for owner in list(_registries(_root(root))):
        try:
            with _catalog(owner) as registry:
                for path in registry.glob("*.json"):
                    lock = _Lock(path.with_suffix(".lock"))
                    if not lock.held:
                        report["skipped"].append({"path": str(path), "reason": "active writer"})
                        continue
                    try:
                        entry = _read(path)
                        if _active_dependency(owner, entry, path):
                            report["skipped"].append(
                                {"path": str(path), "reason": "active dependency writer"}
                            )
                            continue
                        targets = []
                        latest = entry["started_at"]
                        for item in entry["targets"]:
                            target = _target(owner, Path(item["path"]))
                            original = target
                            if item.get("quarantine") is not None:
                                quarantine = _quarantine(registry, item["quarantine"])
                                if quarantine.exists():
                                    target = quarantine
                                elif not target.exists() or not _same(target, item):
                                    # The old generation was already removed; a replacement is unowned.
                                    continue
                            if not target.exists():
                                continue
                            if not _same(target, item):
                                raise ValueError("registered path now identifies a different generation")
                            contents = list(_tree(target))
                            latest = max(latest, *(p.stat().st_mtime for p in contents))
                            targets.append((original, target, item))
                        completed = entry["finished_at"]
                        expiry = max(latest, completed or latest) + max_age_seconds
                        if current < expiry:
                            report["next_expiry"] = min(report["next_expiry"] or expiry, expiry)
                            continue
                        for original, target, item in targets:
                            # Pin the generation by renaming it away from a reusable output path.
                            _target(owner, Path(item["path"]))
                            if not _same(target, item):
                                raise ValueError("artifact generation changed before cleanup")
                            if not dry_run:
                                if target == original:
                                    item["quarantine"] = item.get("quarantine") or uuid4().hex
                                    quarantine = _quarantine(registry, item["quarantine"])
                                    if quarantine.exists():
                                        raise ValueError("artifact quarantine already exists")
                                    # Persist intent first, so a process crash cannot orphan renamed data.
                                    _write(path, entry)
                                    target.rename(quarantine)
                                    target = quarantine
                                if not _same(target, item):
                                    if not original.exists() and not _link(original):
                                        target.rename(original)
                                        item.pop("quarantine", None)
                                        _write(path, entry)
                                    raise ValueError(
                                        "replacement preserved: artifact changed during rename"
                                    )
                                list(_tree(target))
                                if item["directory"]:
                                    shutil.rmtree(target)
                                else:
                                    target.unlink()
                            report["deleted"].append(str(original))
                        if not dry_run:
                            path.unlink()
                    except (OSError, ValueError, TypeError, KeyError) as error:
                        report["errors"].append({"path": str(path), "error": str(error)})
                    finally:
                        lock.close()
                        if not path.exists():
                            path.with_suffix(".lock").unlink(missing_ok=True)
        except (OSError, ValueError, RuntimeError) as error:
            report["errors"].append({"path": str(owner), "error": str(error)})
    return report


def watcher_lock(roots: Sequence[Path]) -> _Lock:
    """Only one watcher owns a normalized root set; the lock lasts until close."""
    normalized = sorted({_root(root) for root in roots}, key=lambda path: str(path).casefold())
    if not normalized:
        raise ValueError("a retention watcher requires at least one root")
    first = normalized[0]
    first.mkdir(parents=True, exist_ok=True)
    identity = "\n".join(
        str(path).casefold() if sys.platform == "win32" else str(path) for path in normalized
    )
    token = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:24]
    with _catalog(first) as registry:
        return _Lock(registry / f"watch-{token}.lock")


def main() -> None:
    """Command line: remove expired registered simulator artifacts under the given roots."""
    parser = argparse.ArgumentParser(description="Remove expired registered simulator artifacts.")
    parser.add_argument("--root", type=Path, action="append", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-age-hours", type=float, default=24)
    parser.add_argument("--watch", action="store_true")
    args = parser.parse_args()
    watcher = None
    try:
        if args.watch:
            watcher = watcher_lock(args.root)
            if not watcher.held:
                return
        while True:
            reports = [
                cleanup_expired(root, max_age_seconds=args.max_age_hours * 3600, dry_run=args.dry_run)
                for root in args.root
            ]
            print(json.dumps(reports), flush=True)
            if not args.watch:
                if any(report["errors"] for report in reports):
                    parser.exit(1)
                return
            deadlines = [r["next_expiry"] for r in reports if r["next_expiry"] is not None]
            wait = min(60.0, max(0.1, min(deadlines) - time.time())) if deadlines else 60.0
            time.sleep(wait)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Retention cleanup failed: {error}\n")
    except KeyboardInterrupt:
        return
    finally:
        if watcher is not None:
            watcher.close()


if __name__ == "__main__":
    main()
