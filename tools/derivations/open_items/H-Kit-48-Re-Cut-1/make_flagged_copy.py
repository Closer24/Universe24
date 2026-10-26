"""The flagged copy of the engine's src, written by exact text replacements and never by hand, no toy: a hand's id, a flag name (an environment variable the copy reads; empty, the copy is the head's path bit for bit) and a JSON list of replacements in, each {"file": "<path under src>", "old": "<exact text>", "new": "<exact text>"}; the copy of <src> written under /dev/shm/tmp/<id>/src_<id>, every replacement refused unless its old text occurs exactly once in the copy's file (nothing written on a refusal); then, unless `check off` is given, the check that the copy with the flag empty runs the hole 60 and the chiral 60 (tests/worlds/world_hole.json and world_nature.json beside the src, or the worlds named) bit for bit with the head: both run by `python -m event_universe.run <world> <out> back 20` under nice 19, the record hashed with the rows' milliseconds struck (the one field that is not the state), the head's record cached under /dev/shm/tmp/<id>/head_<world>.json and reused. The flag's own path is the hand's to run with the flag set.

Usage: python make_flagged_copy.py <id> <FLAG_NAME> <replacements.json> src <worktree>/src [check off] [worlds a.json,b.json] [python <interpreter>]
Prints the replacements applied by file, the copy's path, then per world EQUAL or APART with the two hashes; exit 0 only when every world is EQUAL.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def arg_after(argv: list[str], key: str, default: str | None) -> str | None:
    return argv[argv.index(key) + 1] if key in argv else default


def record_hash(path: Path) -> str:
    """The record's hash with the rows' milliseconds struck."""
    with open(path, encoding="utf-8") as f:
        rec = json.load(f)
    for row in rec.get("rows", []):
        row.pop("milliseconds", None)
    return hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()


def run_record(python: str, src: Path, flag: str, world: Path, out: Path) -> None:
    env = dict(os.environ, PYTHONPATH=str(src), TMPDIR="/dev/shm/tmp")
    env[flag] = ""
    cmd = ["nice", "-n", "19", python, "-m", "event_universe.run", str(world), str(out), "back", "20"]
    subprocess.run(cmd, check=True, env=env, cwd=str(src.parent), stdout=subprocess.DEVNULL)


def main(argv: list[str]) -> int:
    hand, flag, replacements_path = argv[1], argv[2], Path(argv[3])
    src = Path(arg_after(argv, "src", "")).resolve()
    if not src.is_dir() or not (src / "event_universe").is_dir():
        raise SystemExit(f"src is not the engine's src: {src}")
    python = arg_after(argv, "python", sys.executable)
    root = Path("/dev/shm/tmp") / hand
    root.mkdir(parents=True, exist_ok=True)
    copy = root / f"src_{hand}"
    with open(replacements_path, encoding="utf-8") as f:
        replacements = json.load(f)
    # every replacement read against the head's text first: refused before anything is written
    texts: dict[str, str] = {}
    for k, r in enumerate(replacements):
        file, old, new = r["file"], r["old"], r["new"]
        if file not in texts:
            texts[file] = (src / file).read_text(encoding="utf-8")
        n = texts[file].count(old)
        if n != 1:
            raise SystemExit(f"replacement {k} refused: its old text occurs {n} times in {file} (exactly once required); nothing written")
        texts[file] = texts[file].replace(old, new, 1)
        print(json.dumps({"replacement": k, "file": file, "old_bytes": len(old), "new_bytes": len(new)}))
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(src, copy, ignore=shutil.ignore_patterns("__pycache__"))
    for file, text in texts.items():
        (copy / file).write_text(text, encoding="utf-8")
    print(json.dumps({"copy": str(copy), "flag": flag, "files changed": sorted(texts)}))
    if arg_after(argv, "check", "on") == "off":
        return 0
    worlds_arg = arg_after(argv, "worlds", None)
    worlds = (
        [Path(w) for w in worlds_arg.split(",")]
        if worlds_arg
        else [src.parent / "tests" / "worlds" / "world_hole.json", src.parent / "tests" / "worlds" / "world_nature.json"]
    )
    apart = 0
    for world in worlds:
        head_out = root / f"head_{world.stem}.json"
        if not head_out.exists():
            run_record(python, src, flag, world, head_out)
        copy_out = root / f"copy_{hand}_{world.stem}.json"
        run_record(python, copy, flag, world, copy_out)
        h, c = record_hash(head_out), record_hash(copy_out)
        verdict = "EQUAL" if h == c else "APART"
        apart += verdict == "APART"
        print(json.dumps({"world": str(world), "verdict": verdict, "head": h, "copy": c, "head record": str(head_out), "copy record": str(copy_out)}))
    print(f"worlds bit for bit with the head: {len(worlds) - apart} of {len(worlds)}")
    return 1 if apart else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
