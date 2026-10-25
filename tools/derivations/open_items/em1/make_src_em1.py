"""em1's FLAGGED COPY of src/event_universe (2026-10-25), written by this script from the worktree's src by exact text replacements, never by hand.
The one delta: seed.lay_packet reads an optional field `senses` of the `at` lay (default [-1, 1], David's lay bit for bit: the two senses summed,
the im lines cancelling, W = 0 at every Node); `senses: [1]` lays one sense alone, a CHARGED packet (W > 0 at every Node of the envelope),
the probe world of W-S1's source (the charge current's divergence). Nothing else moves. Run: python make_src_em1.py (writes src_em1/)."""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "src", "event_universe")
DST = os.path.join(HERE, "src_em1", "event_universe")
if os.path.exists(os.path.join(HERE, "src_em1")):
    shutil.rmtree(os.path.join(HERE, "src_em1"))
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))
path = os.path.join(DST, "seed.py")
text = open(path).read()
replacements = [
    (
        '                packets.append((node.records().index(row), at, int(lay.get("width", 0)), n))',
        '                packets.append((node.records().index(row), at, int(lay.get("width", 0)), n, tuple(int(x) for x in lay.get("senses", (-1, 1)))))',
    ),
    (
        '    for rec, at, h, n in packets:\n        lay_packet(node, rec, at, h, n)',
        '    for rec, at, h, n, senses in packets:\n        lay_packet(node, rec, at, h, n, senses)',
    ),
    (
        'def lay_packet(node: Node, rec: int, at: tuple[int, ...], h: int, n: int) -> None:',
        'def lay_packet(node: Node, rec: int, at: tuple[int, ...], h: int, n: int, senses: tuple[int, ...] = (-1, 1)) -> None:',
    ),
    (
        '    for sense in (-1, 1):\n        re, im = rest_record(node, row, envelope, w0, amplitude, sense)\n        node.lay(rec, Ellipsis, (re.now, re.before, im.now, im.before))',
        '    for sense in senses:  # em1 flag: the senses laid; (-1, 1) is the former lay bit for bit\n        re, im = rest_record(node, row, envelope, w0, amplitude, sense)\n        node.lay(rec, Ellipsis, (re.now, re.before, im.now, im.before))',
    ),
]
for old, new in replacements:
    if text.count(old) != 1:
        sys.exit("refused: the text to replace is not found exactly once: " + old[:60])
    text = text.replace(old, new)
open(path, "w").write(text)
# the loader: the world key `senses` lives inside a lay, not among the world's four keys: no loader change needed.
print("written", DST)
