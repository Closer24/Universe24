"""pm1's flagged COPY of the engine (engine-5.0-test af06713db, src/event_universe), written by this script and never by hand:
the copy is src/event_universe under tools/derivations/pm1/src_pm1/ with ONE module flag, readings.WEIGHT, and one helper,
readings.weight_square: the weight every count of the Node is read at (the share's wall 4 sq G^2, the take's fall 2 sq G^2,
the lay's target unit 4 sq G^2). WEIGHT "default" (the flag absent) is David's path bit for bit: the standing and the meeting at
the vacuum's weight (sq = Gamma^2), the take's fall and the lay's amplitude at the frame's weight (sq = p_i^2, the Link pace).
WEIGHT "link": every read at the frame's weight, sq = p_i^2 ((Gamma / p_i)^2 = X / Gamma to the unit: the carrier's unit, PM-S1).
WEIGHT "vacuum": every read at the vacuum's weight, sq = Gamma^2. WEIGHT "clock": every read at the clock's weight, sq = p_0^2.
Every replacement must match the engine's text exactly once, else the script refuses. Run: python make_copy.py"""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '..', '..', 'src', 'event_universe')
DST = os.path.join(HERE, 'src_pm1', 'event_universe')

if os.path.exists(os.path.join(HERE, 'src_pm1')):
    shutil.rmtree(os.path.join(HERE, 'src_pm1'))
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns('__pycache__'))

edits = {
    'readings.py': [
        ('from event_universe.rows import CARRIER, Line, zeros\n',
         'from event_universe.rows import CARRIER, Line, zeros\n\n'
         'WEIGHT = "default"  # pm1\'s flag (2026-10-25): the weight every count is read at; "default" David\'s path bit for bit\n\n\n'
         'def weight_square(node: Node, pace: Any, content: Any, vacuum: bool) -> Any:\n'
         '    """pm1: the square under the weight 4 sq G^2 of a count: the engine\'s (Gamma^2 where the read is the vacuum\'s, else the Link pace squared), or under the flag one square for every read alike: the Link pace\'s (the carrier\'s unit, (Gamma / p_i)^2 = X / Gamma), the vacuum\'s, or the clock\'s."""\n'
         '    if WEIGHT == "default":\n'
         '        return (node.gamma * node.gamma) if vacuum else pace * pace\n'
         '    if WEIGHT == "link":\n'
         '        return pace * pace\n'
         '    if WEIGHT == "vacuum":\n'
         '        return node.gamma * node.gamma + 0 * pace\n'
         '    p0 = paces.clock_of(node.gamma, content)\n'
         '    return p0 * p0\n'),
        ('    sq = (node.gamma * node.gamma) if vacuum else pace * pace\n',
         '    sq = weight_square(node, pace, node.start_content, vacuum)  # pm1\n'),
    ],
    'take.py': [
        ('    weight = 2 * pace * pace * node.G * node.G + (1 if pace == 0 else 0)\n',
         '    sq = int(readings.weight_square(node, pace, int(np.asarray(node.start_content)[at]), False))  # pm1\n'
         '    weight = 2 * sq * node.G * node.G + (1 if sq == 0 else 0)\n'),
        ('    target = node.units[s] * 4 * pc * pc * node.G * node.G\n',
         '    target = node.units[s] * 4 * int(readings.weight_square(node, pc, int(np.asarray(c)[at]), False)) * node.G * node.G  # pm1\n'),
        ('from event_universe.core import paces, rule3\n',
         'from event_universe import readings  # pm1\nfrom event_universe.core import paces, rule3\n'),
    ],
}
for name, pairs in edits.items():
    path = os.path.join(DST, name)
    text = open(path).read()
    for old, new in pairs:
        if text.count(old) != 1:
            print('REFUSED', name, repr(old[:60]), text.count(old)); sys.exit(1)
        text = text.replace(old, new)
    open(path, 'w').write(text)
print('copy written', DST, 'edits', sum(len(p) for p in edits.values()))
