"""ws1's rebuild of cl1's flagged lay (tools/derivations/open_items/cl1/make_copy.py: the same 7 exact text replacements of seed.py, here
against ws1's instrumented copy src_ws1/event_universe/seed.py, whose text is the engine's), written as lay_ws1.py; src never edited.
Run: python make_lay_ws1.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src_ws1", "event_universe", "seed.py")
DST = os.path.join(HERE, "lay_ws1.py")
text = open(SRC, encoding="utf-8").read()
replacements = [
    ('"""The seed as the world file lays it:',
     '"""ws1\'s rebuild of cl1\'s FLAGGED COPY of the engine\'s seed module (make_lay_ws1.py names every delta; src untouched).\nThe seed as the world file lays it:'),
    ("from event_universe.core.rule3 import quotient\n", "from event_universe.core.rule3 import half, quotient\n"),
    ('                packets.append((node.records().index(row), at, int(lay.get("width", 0)), n))',
     '                packets.append((node.records().index(row), at, int(lay.get("width", 0)), n, lay.get("sense"), lay.get("charge")))  # cl1: the two fields gained'),
    ("    for rec, at, h, n in packets:\n        lay_packet(node, rec, at, h, n)",
     "    for rec, at, h, n, sense, charge in packets:\n        lay_packet(node, rec, at, h, n, sense, charge)"),
    ("def lay_packet(node: Node, rec: int, at: tuple[int, ...], h: int, n: int) -> None:",
     "def lay_packet(node: Node, rec: int, at: tuple[int, ...], h: int, n: int, sense: Any = None, charge: Any = None) -> None:"),
    ("    for sense in (-1, 1):\n        re, im = rest_record(node, row, envelope, w0, amplitude, sense)\n        node.lay(rec, Ellipsis, (re.now, re.before, im.now, im.before))",
     "    senses = (-1, 1) if sense is None else (int(sense),)  # cl1: the field absent is the engine's conjugate pair\n"
     "    if sense is not None and int(sense) not in (-1, 1):\n        raise ValueError('a sense is -1 or 1')\n"
     "    if charge not in (None, 'T div 2'):\n        raise ValueError('a charge is the row\\'s (absent) or \"T div 2\"')\n"
     "    for s_ in senses:\n        re, im = rest_record(node, row, envelope, w0, amplitude, s_)\n"
     "        if charge == 'T div 2':  # cl1: MS-S1 for the seed's packet, W summed over the packet T div 2 to the floor\n"
     "            total = int(sum(int(x) for x in envelope.reshape(-1)))\n"
     "            im.before = np.where(re.now > 0, s_ * quotient(half(node.T) * envelope, np.where(re.now > 0, total * re.now, 1)), 0)\n"
     "        node.lay(rec, Ellipsis, (re.now, re.before, im.now, im.before))"),
    ('            "quanta": n,\n            "amplitude": amplitude,',
     '            "quanta": n,\n            "sense": sense,\n            "charge": charge,\n            "amplitude": amplitude,'),
]
for old, new in replacements:
    if text.count(old) != 1:
        raise SystemExit(f"replacement matches {text.count(old)} times, refused:\n{old}")
    text = text.replace(old, new)
open(DST, "w", encoding="utf-8").write(text)
print("written", DST, len(replacements), "replacements")
