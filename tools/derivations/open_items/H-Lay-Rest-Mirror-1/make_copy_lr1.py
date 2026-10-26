"""lr1's flagged copy of src/ (no edit under src/): src_lr1 beside this script, three text replacements, each read from the environment at run time so the same copy runs unflagged bit for bit. LR1_PICK=1: the pick's digit centred, |2 r + 1 - W| (David's mend, 6406297069), the origin where the centred digit is 1 (r at the half or its mirror). LR1_LAY=1: the lay's rest under the 48, every line's remainder re-born after the world's lays at the half of its wall where its level is at or above 0 and at the half's mirror W - 1 - half where its level is below 0 (the wave lay's gauge made one act for every row alike). Usage: make_copy_lr1.py <worktree>"""
import os
import shutil
import sys

root = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
dst = os.path.join(here, "src_lr1")
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(os.path.join(root, "src"), dst)


def edit(rel, old, new):
    p = os.path.join(dst, rel)
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == 1, (rel, old)
    open(p, "w", encoding="utf-8").write(s.replace(old, new))


edit(
    "event_universe/node.py",
    '''    def digit_of(self, rem: int, values: int) -> tuple[int, int]:
        """One line's digit at a Node: its remainder on the lattice and the count of values the lattice holds."""
        return rem, values''',
    '''    def digit_of(self, rem: int, values: int, wall: int = 0) -> tuple[int, int]:
        """One line's digit at a Node: its remainder on the lattice and the count of values the lattice holds; flagged (LR1_PICK), the remainder's distance from the centre of its wall, |2 r + 1 - W|, the same for r and its mirror W - 1 - r (the one rule's (v) read exactly, odd walls and even alike)."""
        import os as _os
        if _os.environ.get("LR1_PICK") == "1":
            return abs(rem + rem + 1 - wall), values
        return rem, values''',
)
edit(
    "event_universe/take.py",
    '''            rem, values = node.digit_of(int(line.rem[n]), quotient(at_node(line.wall, n), f))
            origin = origin and rem in (w_half, mirrored(w_half, node.w, 1))''',
    '''            rem, values = node.digit_of(int(line.rem[n]), quotient(at_node(line.wall, n), f), int(at_node(line.wall, n)))
            origin = origin and (rem == 1 if __import__("os").environ.get("LR1_PICK") == "1" else rem in (w_half, mirrored(w_half, node.w, 1)))''',
)
edit(
    "event_universe/seed.py",
    '''    for rec, at, h, n, vector, sense, wave, top in packets:
        lay_packet(node, rec, at, h, n, vector, sense, wave, top)
''',
    '''    for rec, at, h, n, vector, sense, wave, top in packets:
        lay_packet(node, rec, at, h, n, vector, sense, wave, top)
    if __import__("os").environ.get("LR1_LAY") == "1":
        rest_by_sign(node)


def rest_by_sign(node: Node) -> None:
    """lr1's lay rule (LR-S1): after the world's lays every line's remainder is re-born at the half of its wall where the line's level is at or above 0 and at the half's mirror W - 1 - half where below 0 (now or before), one act for every row alike (the wave lay's gauge, every lay); the ones' complement commutes with the negation of a line, so a negated lay's rest is the lay's rest mirrored, and the reflected file lays the C P image on every line with a level."""
    from event_universe.core.rule3 import mirrored as _mirrored
    for r in node.rows_:
        for line in r.lines:
            if line.rem is None or line.wall is None:
                continue
            hw = zeros(node.shape) + half(line.wall)
            negated = np.vectorize(lambda a, b: int(a) < 0 or int(b) < 0, otypes=[bool])(line.now, line.before)
            line.rem = np.where(negated, _mirrored(hw, line.wall, 1), hw)
''',
)
print("src_lr1 written at", dst)
