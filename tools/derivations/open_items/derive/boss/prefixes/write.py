"""The shipped worlds' first rounds, for tests/test_the_tensor24_worlds.py (the Boss's code writer, 2026-10-31, on the
pruner's finding that only our bang's run was guarded by a test, and the sixth code reader's minor 4): every example
folder but our bang's, its own three files run out and back by the run tool's own function, main.ran, for PREFIX rounds,
the click world to its first click round so that the test pins its clicks; each record's end line written as the run
wrote it, with the world's name, its count of click lines and their digest, the no case's PREFIX rounds and the
world's own digest at them, to tests/tensor24_prefixes.jsonl; no digest is typed
anywhere.

Clock: n/a: the worlds' own files, run as the run tool runs them.
Algebra: n/a: the record's end line holds the digest of the state after the rounds and the run back's exactness.
Board: each world's own board.
Clicks: the click world's first click round read off its record over a run of REACH rounds, a fixed window and no
search; with no click in it, the click world runs PREFIX rounds as the others do.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/prefixes/write.py; it writes tests/tensor24_prefixes.jsonl.
"""

import hashlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT.joinpath("src")))

from tensor24 import main  # noqa: E402
from tensor24.runner.files import NAMES  # noqa: E402

PREFIX = 4  # the rounds each world runs out and back, a few seconds each, and every no case's rounds
BANG = "tensor24"  # our bang's folder, which the run test runs whole
CLICKS = "tensor24-click"  # the world whose first click the test pins
REACH = 200  # the window of rounds in which the click world's first click is read


def ran(world, rounds, scratch):
    """The world's own three files run out and back for the rounds: the record's end line, its count of click lines and
    their digest, SHA-256 of the click lines' text as the run wrote them, a line feed between two."""
    *paths, setting = [ROOT.joinpath("examples", world, f"{name}.json") for name in NAMES]
    held = json.loads(setting.read_text(encoding="utf-8"))
    held["ticks"] = rounds
    short, record = Path(scratch).joinpath(f"{world}.json"), Path(scratch).joinpath(f"{world}.jsonl")
    short.write_text(json.dumps(held), encoding="utf-8")
    found = main.ran([*paths, short], record)
    assert not found, found
    text = record.read_text(encoding="utf-8").splitlines()
    end, clicks = json.loads(text[-1]), [x for x in text if json.loads(x)["kind"] == "click"]
    assert end["exact"] == 1, end
    return end, clicks, hashlib.sha256("\n".join(clicks).encode("utf-8")).hexdigest()


def write():
    worlds = sorted(f.name for f in ROOT.joinpath("examples").glob("*/") if f.name != BANG)
    written = []
    with tempfile.TemporaryDirectory() as scratch:
        for world in worlds:
            rounds = PREFIX
            if world == CLICKS:
                _, clicks, _ = ran(world, REACH, scratch)
                rounds = min([json.loads(x)["round"] for x in clicks] or [PREFIX])
            end, clicks, lines = ran(world, rounds, scratch)
            no, _, _ = ran(world, PREFIX, scratch)
            written.append(
                json.dumps(
                    {
                        "world": world,
                        "clicks": len(clicks),
                        "lines": lines,
                        "no": PREFIX,
                        "own": no["digest"],
                        **end,
                    }
                )
            )
            print(written[-1], flush=True)
    ROOT.joinpath("tests", "tensor24_prefixes.jsonl").write_text(
        "\n".join(written) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    write()
