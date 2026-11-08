"""Verify the directly tracked invariant-family evidence without running dynamics."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = Path("research/invariant_families_v1/evidence_manifest.json")
PREFIXES = (
    "research/invariant_families_v1/evidence/",
    "research/clock_selection/evidence/invariant_families_algebra/",
)
PINNED_MANIFEST_SHA256 = "80dcf5c01c0336c3e274d467cc1d70e92658c6d413937f659bcfe447d7aa51f1"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(data):
    return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode()


def permitted(value):
    if not isinstance(value, str) or "\\" in value:
        return False
    path = PurePosixPath(value)
    return (path.as_posix() == value and not path.is_absolute()
            and ".." not in path.parts
            and any(value.startswith(prefix) and value != prefix
                    for prefix in PREFIXES))


def inventory(root=ROOT):
    root = Path(root).resolve()
    result = []
    for prefix in PREFIXES:
        directory = root / prefix
        for parent in (directory, *directory.parents):
            if parent == root:
                break
            if parent.is_symlink():
                raise ValueError("Evidence prefix contains a symlink")
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*")):
            if path.is_symlink():
                raise ValueError("Evidence contains a symlink")
            if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            name = path.relative_to(root).as_posix()
            if not permitted(name):
                raise ValueError("Evidence path is outside the fixed namespace")
            raw = path.read_bytes()
            result.append({"path": name, "bytes": len(raw), "sha256": digest(raw)})
    return sorted(result, key=lambda item: item["path"])


def verify(*, root=ROOT, manifest=None,
           expected_manifest_sha256=PINNED_MANIFEST_SHA256):
    root = Path(root).resolve()
    manifest = root / MANIFEST if manifest is None else Path(manifest)
    raw = manifest.read_bytes()
    if digest(raw) != expected_manifest_sha256:
        raise ValueError("Pinned evidence manifest hash mismatch")
    data = json.loads(raw)
    if data.get("format") != "universe24-invariant-evidence-v1":
        raise ValueError("Invalid evidence manifest format")
    items = data.get("files")
    if not isinstance(items, list) or not items:
        raise ValueError("Evidence manifest must contain complete files")
    paths = [item.get("path") for item in items]
    if any(not permitted(path) for path in paths):
        raise ValueError("Manifest path is outside the fixed evidence namespaces")
    if len(paths) != len(set(paths)) or paths != sorted(paths):
        raise ValueError("Manifest paths must be unique and sorted")
    for item in items:
        path = root / item["path"]
        for parent in (path, *path.parents):
            if parent == root:
                break
            if parent.is_symlink():
                raise ValueError("Evidence path contains a symlink")
        if not path.resolve().is_relative_to(root):
            raise ValueError("Evidence path escapes the repository")
        if not path.is_file():
            raise ValueError("Missing evidence: " + item["path"])
        contents = path.read_bytes()
        if len(contents) != item.get("bytes") or digest(contents) != item.get("sha256"):
            raise ValueError("Evidence bytes differ: " + item["path"])
    if inventory(root) != items:
        raise ValueError("Complete evidence inventory differs from the frozen manifest")
    return {"format": "universe24-invariant-evidence-verification-v1",
            "manifest_sha256": digest(raw), "verified_files": len(items),
            "verified_bytes": sum(item["bytes"] for item in items),
            "read_only": True, "native_evolution_executed": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    print(json.dumps(verify(), indent=2))


if __name__ == "__main__":
    main()
