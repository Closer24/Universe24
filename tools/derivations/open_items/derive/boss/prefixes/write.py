"""The shipped worlds' first rounds, for tests/test_the_tensor24_worlds.py (the Boss's code writer, 2026-10-31, on the
pruner's finding that only our bang's run was guarded by a test): every example folder but our bang's, its own three
files at PREFIX rounds, run out and back by the run tool's own function, main.ran, and its record's end line written as
the run wrote it, with the world's name, to tests/tensor24_prefixes.jsonl; no digest is typed anywhere.

Clock: n/a: the worlds' own files, run as the run tool runs them.
Algebra: n/a: the record's end line holds the digest of the state after the rounds and the run back's exactness.
Board: each world's own board.
Clicks: n/a: the end line alone is kept.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/prefixes/write.py; it writes tests/tensor24_prefixes.jsonl.
"""

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT.joinpath("src")))

from tensor24 import main  # noqa: E402
from tensor24.runner.files import NAMES  # noqa: E402

PREFIX = 4  # the rounds each world runs out and back, a few seconds each
BANG = "tensor24"  # our bang's folder, which the run test runs whole


def write():
    worlds = sorted(f.name for f in ROOT.joinpath("examples").glob("*/") if f.name != BANG)
    lines = []
    with tempfile.TemporaryDirectory() as scratch:
        for world in worlds:
            *paths, setting = [ROOT.joinpath("examples", world, f"{name}.json") for name in NAMES]
            held = json.loads(setting.read_text(encoding="utf-8"))
            held["ticks"] = PREFIX
            short, record = Path(scratch).joinpath(f"{world}.json"), Path(scratch).joinpath(f"{world}.jsonl")
            short.write_text(json.dumps(held), encoding="utf-8")
            found = main.ran([*paths, short], record)
            assert not found, found
            end = json.loads(record.read_text(encoding="utf-8").splitlines()[-1])
            assert end["exact"] == 1, end
            lines.append(json.dumps({"world": world, **end}))
            print(lines[-1], flush=True)
    ROOT.joinpath("tests", "tensor24_prefixes.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    write()
