"""KEY4's reference: node-all 9d75a4904's own runs on its own files (tree_all, taken by git archive and read-only: its
src and the five shipped worlds), for p_key4.py to compare against. It reads node-all's chosen key only as node-all's
loader reads it, and writes no key for the comparison to use.

L  each world's load, no round: the file's key K, every side's edge dial D (the set of them), D over K by Rule3's carry
   (kappa div senses, with its remainder), every side's tooth at its birth (the set) and the teeth's count.
A  the click world's three files, 200 rounds (SCALE1's window) by the engine's act, its click lines by the runner's own
   clicked() with the edges' partners as run.py reads them, its end digest by the runner's digest(); written line by
   line to click_all.jsonl, with the end digest and the digest of the end state's counts (a, b, r, rd) alone.
C  the decoder's guards on the click world's first-click record (1 round, by main.ran) and on two mutants of it, one
   train card's key moved by senses, another odd key: the metric's (a train no click line names) and the giver's;
   written to decode/ so that p_key4.py reads the same files with the copy's decoder.
R  every shipped world's records by the run tool's own main.ran (worlds4.py: node-all's write.py procedure, our bang
   whole), each read by node-all's decoder, to records_all.jsonl, and the lines write.py would write, to
   prefixes_all.jsonl, against node-all's own tests/tensor24_prefixes.jsonl.
Whole numbers; Rule3's carry the one division; paths by joinpath.

Run: python -I p_key4_all.py <tree_all> <out folder>, Python 3.14.
"""

import json
import sys
import tempfile
from pathlib import Path

TREE, OUT = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(TREE.joinpath("src")))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import tensor24  # noqa: E402
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.decoder import records as decoding  # noqa: E402
from tensor24.main import ENGINE as engine  # noqa: E402
from tensor24.runner import run as runner  # noqa: E402
from tensor24.runner.files import NAMES, sites_of, star  # noqa: E402
from tensor24.runner.load import load  # noqa: E402

import worlds4  # noqa: E402

assert Path(tensor24.__file__).resolve().is_relative_to(TREE.resolve()), tensor24.__file__
WINDOW = 200  # rounds, SCALE1's window, as KEY2 and KEY3
examples = TREE.joinpath("examples")
OUT.mkdir(parents=True, exist_ok=True)


def say(line):
    print(line, flush=True)


def files(world):
    return [json.loads(examples.joinpath(world, f"{n}.json").read_text(encoding="utf-8")) for n in NAMES]


say(f"the tree: {TREE.name}, tensor24 from {Path(tensor24.__file__).resolve().relative_to(TREE.resolve())}")
# L: each world's load
for world in sorted(f.name for f in examples.glob("*/")):
    u, p, st = files(world)
    shape = p["shape"]
    made = engine.made(star(len(shape)))
    senses, _ = carry(len(star(len(shape))), len(shape), 0)
    loaded, found = load(u, st, sites_of(shape), *made)
    assert not found, found
    _, _, key = loaded.click
    k = loaded.state[-1]
    dials, born = sorted(set(key.ravel().tolist())), sorted(set(k.ravel().tolist()))
    scale, rest = carry(dials[0], u["chosen"]["key"], 0)
    say(f"L {world}: the file's key K {u['chosen']['key']}; the edge dial D {dials} on {key.shape[0]} sides; D over K"
        f" {scale} (remainder {rest}), kappa = senses x that = {senses * scale}; every tooth born at {born}"
        f" ({k.size} teeth); D's remainder by senses {sorted(set(carry(key, senses, 0)[1].ravel().tolist()))}")

# A: the click world, 200 rounds
u, p, st = files("tensor24-click")
shape = p["shape"]
loaded, found = load(u, st, sites_of(shape), *engine.made(star(len(shape))))
assert not found, found
layout = engine.layout(u, shape, loaded)
s = engine.state(*loaded.state)
partners = runner.joined(layout.click, len(loaded.trains))
events, read_ = [], s
for at in range(1, WINDOW + 1):
    end, clicks = engine.act(layout, read_)
    events += runner.clicked(at, read_, end, clicks, partners, layout.nb)
    read_ = end
summary = {
    "rounds": WINDOW,
    "lines": len(events),
    "end": runner.digest(runner.stated(read_)),
    "counts": runner.digest(json.dumps([x.tolist() for x in read_[:-1]])),
}
OUT.joinpath("click_all.jsonl").write_text(
    "".join(json.dumps(e) + "\n" for e in events) + json.dumps(summary) + "\n", encoding="utf-8"
)
say(f"A, node-all: the click world's files, {WINDOW} rounds: click lines {summary['lines']}; end digest"
    f" {summary['end'][:16]}; the end's counts (a, b, r, rd) digest {summary['counts'][:16]}")

# C: the decoder on the first-click record and two mutants of it
decode = OUT.joinpath("decode")
decode.mkdir(parents=True, exist_ok=True)
held = json.loads(examples.joinpath("tensor24-click", "setting.json").read_text(encoding="utf-8"))
held["ticks"] = 1
short = decode.joinpath("setting.json")
short.write_text(json.dumps(held), encoding="utf-8")
first = decode.joinpath("click1.jsonl")
paths = [examples.joinpath("tensor24-click", f"{n}.json") for n in NAMES[:2]]
assert main.ran([*paths, short], first) == []
lines = first.read_text(encoding="utf-8").splitlines()
header = json.loads(lines[0])
senses, _ = carry(len(star(len(shape))), len(shape), 0)
named = {t["index"]: t["label"] for t in header["trains"]}
clicking = sorted({json.loads(x)["train"] for x in lines[1:-1] if json.loads(x)["kind"] == "click"})
for index in (1, 3):  # the metric's card and the giver's, as the file names them
    moved = dict(header)
    moved["trains"] = [{**t, "key": t["key"] + senses} if t["index"] == index else t for t in header["trains"]]
    decode.joinpath(f"click1.card{index}.jsonl").write_text(
        "\n".join([json.dumps(moved), *lines[1:]]) + "\n", encoding="utf-8"
    )
say(f"C: the first-click record: {len(lines) - 2} click lines, of the trains {[named[t] for t in clicking]}; the header's"
    f" dial {header['dial']}, birth {header['birth']}, the cards' keys {[t['key'] for t in header['trains']]}")
for name in ("click1.jsonl", "click1.card1.jsonl", "click1.card3.jsonl"):
    held_record, cause = decoding.read(str(decode.joinpath(name)))
    say(f"C, node-all's decoder: {name}: read {int(held_record is not None)}; cause: {cause or 'none'}")

# R: every world's records by the run tool, and the lines write.py would write
with tempfile.TemporaryDirectory(dir=OUT) as scratch:
    rows = worlds4.records(examples, scratch)
OUT.joinpath("records_all.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
OUT.joinpath("prefixes_all.jsonl").write_text("\n".join(worlds4.pinned(rows)) + "\n", encoding="utf-8")
for r in rows:
    say(f"R, node-all: {r['world']} ({r['run']}): {r['rounds']} rounds, click lines {r['clicks']} ({r['lines'][:16]}),"
        f" end digest {r['end']['digest'][:16]}, run back exact {r['end']['exact']}, the cards' keys {sorted(set(r['keys']))},"
        f" dial {r['dial']}, birth {r['birth']}; the decoder reads it: {r['cause'] or 'no cause'}")
pins = TREE.joinpath("tests", "tensor24_prefixes.jsonl").read_text(encoding="utf-8")
say(f"R: the lines write.py would write equal node-all's tests/tensor24_prefixes.jsonl byte for byte:"
    f" {int(OUT.joinpath('prefixes_all.jsonl').read_text(encoding='utf-8') == pins)}")
