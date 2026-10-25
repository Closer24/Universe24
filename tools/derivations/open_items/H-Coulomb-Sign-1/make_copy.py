"""cl1's flagged COPY of the engine's seed module (src/event_universe/seed.py on engine-5.0-test 5e94fd4b6), written by this script
and never by hand: lay_cl1.py is seed.py with the `at` lay of a plane with a gap gaining two fields, `sense` and `charge`; nothing else moves.
Every replacement below must match the engine's text exactly once, else the script refuses. Run: python make_copy.py (writes lay_cl1.py beside it).

The fields: `sense` absent lays the conjugate pair (both senses, the engine's path bit for bit: the body neutral, W 0 at every Node);
`sense` -1 or 1 lays ONE record of that sense at the amplitude fitted to the quanta (W = sense re_now^2 s div den at every Node of the packet:
the row's charge, the default |W|). `charge` absent keeps the row's |W|; `charge` "T div 2" lays im_before = sense (T div 2) envelope_i div (SUM envelope re_now_i)
so that the body's Wronskian summed over its packet is T div 2 to the floor for every row (MS-S1 read for a seed packet: the deviation from ms2's
one-Node form (A, B) named in cl1_REPORT.md). The driver run_cl1.py binds lay_cl1.lay_world in place of seed.lay_world; src is never edited."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "src", "event_universe", "seed.py")
DST = os.path.join(HERE, "lay_cl1.py")

text = open(SRC, encoding="utf-8").read()
replacements = []

# 0. the head: the copy named
replacements.append((
    '"""The seed as the world file lays it:',
    '"""cl1\'s FLAGGED COPY (2026-10-25) of the engine\'s seed module: the `at` lay of a plane with a gap gains `sense` and `charge` (make_copy.py names every delta); src/event_universe/seed.py is untouched.\nThe seed as the world file lays it:'))
# 1. the import: half for T div 2
replacements.append((
    "from event_universe.core.rule3 import quotient\n",
    "from event_universe.core.rule3 import half, quotient\n"))
# 2. lay_world: the packet carries the two fields
replacements.append((
    '                packets.append((node.records().index(row), at, int(lay.get("width", 0)), n))',
    '                packets.append((node.records().index(row), at, int(lay.get("width", 0)), n, lay.get("sense"), lay.get("charge")))  # cl1: the two fields gained'))
replacements.append((
    "    for rec, at, h, n in packets:\n        lay_packet(node, rec, at, h, n)",
    "    for rec, at, h, n, sense, charge in packets:\n        lay_packet(node, rec, at, h, n, sense, charge)"))
# 3. lay_packet: one record of the named sense, or the conjugate pair (the engine's path) where the field is absent
replacements.append((
    "def lay_packet(node: Node, rec: int, at: tuple[int, ...], h: int, n: int) -> None:",
    "def lay_packet(node: Node, rec: int, at: tuple[int, ...], h: int, n: int, sense: Any = None, charge: Any = None) -> None:"))
replacements.append((
    "    for sense in (-1, 1):\n        re, im = rest_record(node, row, envelope, w0, amplitude, sense)\n        node.lay(rec, Ellipsis, (re.now, re.before, im.now, im.before))",
    "    senses = (-1, 1) if sense is None else (int(sense),)  # cl1: the field absent is the engine's conjugate pair\n"
    "    if sense is not None and int(sense) not in (-1, 1):\n        raise ValueError('a sense is -1 or 1')\n"
    "    if charge not in (None, 'T div 2'):\n        raise ValueError('a charge is the row\\'s (absent) or \"T div 2\"')\n"
    "    for s_ in senses:\n        re, im = rest_record(node, row, envelope, w0, amplitude, s_)\n"
    "        if charge == 'T div 2':  # cl1: MS-S1 for the seed's packet, W summed over the packet T div 2 to the floor\n"
    "            total = int(sum(int(x) for x in envelope.reshape(-1)))\n"
    "            im.before = np.where(re.now > 0, s_ * quotient(half(node.T) * envelope, np.where(re.now > 0, total * re.now, 1)), 0)\n"
    "        node.lay(rec, Ellipsis, (re.now, re.before, im.now, im.before))"))
# 4. the lay's log carries the fields
replacements.append((
    '            "quanta": n,\n            "amplitude": amplitude,',
    '            "quanta": n,\n            "sense": sense,\n            "charge": charge,\n            "amplitude": amplitude,'))

for old, new in replacements:
    if text.count(old) != 1:
        raise SystemExit(f"replacement matches {text.count(old)} times, refused:\n{old}")
    text = text.replace(old, new)
open(DST, "w", encoding="utf-8").write(text)
print("written", DST, len(replacements), "replacements")
