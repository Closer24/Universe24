"""rw1's fold without the flag, the engine as RW-S1 would have it, for the patch rw1.patch: the same five sites as make_copy_rw1.py with the former spelling struck. Writes to /dev/shm/tmp/rw1/src_rw1_clean."""
import os
import shutil
import sys

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "..", "src", "event_universe")
root = sys.argv[1] if len(sys.argv) > 1 else "/dev/shm/tmp/rw1/src_rw1_clean"
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, old, new):
    text = open(path).read()
    assert text.count(old) == 1, ("the replacement site is not unique", path, old[:60])
    open(path, "w").write(text.replace(old, new))


rule3 = os.path.join(dst, "core", "rule3.py")
replace(
    rule3,
    '''    """The one carried division of the law (ALGEBRA.md #the-four-acts, #the-direction): u = sigma total + r, the quotient sigma (u div w) and the remainder u mod w kept in [0, w) for a total of either sign; +1 forward, -1 the same act back, exact: from the quotient and the remainder the forward act wrote, the level and the remainder before it."""
    total = direction * total + remainder
    quotient = total // wall
    return direction * quotient, total - wall * quotient
''',
    '''    """The one carried division of the law (ALGEBRA.md #the-four-acts, #the-direction): u = total + r, the quotient u div w and the remainder u mod w kept in [0, w) for a total of either sign; the act at -1 is the act at +1 conjugated by the one rule's mirror (RW-S1: the remainder mirrored in, w - 1 - r, the forward division, the remainder mirrored out, the quotient as it falls), exact: from the quotient and the remainder the forward act wrote, the level and the remainder before it; the former spelling sigma total + r with the quotient sigma (u div w), the same integers, kept by name."""
    carried = total + (remainder if direction == 1 else wall - 1 - remainder)
    quotient = carried // wall
    rest = carried - wall * quotient
    return quotient, rest if direction == 1 else wall - 1 - rest
''',
)

nodepy = os.path.join(dst, "node.py")
replace(
    nodepy,
    '''        """Rule3's step of one row at every Node, the one function of a line: for each line the total S now - w before + SUM_j R_j m_j (+ the line's flux where the row carries its write inside the division), one carried division at the wall w per line. Backward the same act on the before slots with the division's direction -1."""
        at = starts or [line.now if direction == 1 else line.before for line in lines]
        fluxes: list[Any] = flux or [0] * len(lines)
        totals = [
            r.self_coefficient * a - (r.wall * line.before if direction == 1 else 0) + f + m
            for line, a, f, m in zip(lines, at, fluxes, self.arrivals(at, r, turn), strict=True)
        ]
        found = []
        for line, a, t in zip(lines, at, totals, strict=True):
            if direction == 1:
                self.max_transient = max(self.max_transient, bits_of(t))
            quotient, rem = carried_division(t, r.wall, line.rem, direction)
            if direction == 1:
                found.append(Line(quotient, line.now, rem, line.wall, line.wr, line.wwall))
            else:
                found.append(Line(a, quotient - line.now, rem, line.wall, line.wr, line.wwall))
        return found
''',
    '''        """Rule3's step of one row at every Node, the one function of a line in either direction (RW-S1): the line's two slots one pair read reversed by the direction, (a, y) = (now, before) forward and (before, now) backward, the total S a - w y + SUM_j R_j m_j (+ the line's flux where the row carries its write inside the division), one carried division at the wall w per line, the new line the pair (quotient, a) reversed by the direction; the former spelling (the total without w y backward and y taken off the quotient after), the same integers, kept by name."""
        pairs = [(line.now, line.before)[::direction] for line in lines]
        at = starts or [a for a, _y in pairs]
        fluxes: list[Any] = flux or [0] * len(lines)
        totals = [
            r.self_coefficient * a - r.wall * y + f + m
            for (_a, y), a, f, m in zip(pairs, at, fluxes, self.arrivals(at, r, turn), strict=True)
        ]
        found = []
        for line, a, t in zip(lines, at, totals, strict=True):
            if direction == 1:
                self.max_transient = max(self.max_transient, bits_of(t))
            quotient, rem = carried_division(t, r.wall, line.rem, direction)
            found.append(Line(*(quotient, a)[::direction], rem, line.wall, line.wr, line.wwall))
        return found
''',
)
replace(
    nodepy,
    '''        """The Node's act on one row in the direction: Rule3's rotate of the row then its lines' writes (forward); the writes undone then the rotate inverted (backward). Returns the row at the start, the stepped levels before the write, and the row as the act leaves it; backward at the turned Nodes `top` the row is set to `kept`, the pre-state the exchange returned."""
        if direction == 1:
            stepped = self.rotate(lines, r, turn, 1, flux, None)
            levels = [line.now for line in stepped]
            for line, n in zip(stepped, numerators, strict=True):
                if n is not None:
                    self.write(line, n, 1)
            return lines, levels, stepped
        starts = None if kept is None else [np.where(top, line.now, line.before) for line in lines]
        for line, n in zip(lines, numerators, strict=True):
            if n is not None:
                self.write(line, n, -1)
        levels = [line.now for line in lines]
        start = self.rotate(lines, r, turn, -1, flux, starts)
        if kept is not None:
            self.restore(start, kept, top)
        return start, levels, start
''',
    '''        """The Node's act on one row in the direction, one path (RW-S1): Rule3's rotate and the lines' writes taken in the direction's order, the rotate first forward and the write first backward, each at the direction, the stepped levels read between the two; backward at the turned Nodes `top` the row is set to `kept`, the pre-state the exchange returned (`kept` None forward). Returns the row at the start (the row given forward, the row made backward), the stepped levels before the write, and the row as the act leaves it; the former two paths, the same integers, kept by name."""
        starts = None if kept is None else [np.where(top, line.now, line.before) for line in lines]
        row = [lines]

        def rotate() -> None:
            row[0] = self.rotate(row[0], r, turn, direction, flux, starts)

        def write() -> None:
            for line, n in zip(row[0], numerators, strict=True):
                if n is not None:
                    self.write(line, n, direction)

        first, second = (rotate, write)[::direction]
        first()
        levels = [line.now for line in row[0]]
        second()
        if kept is not None:
            self.restore(row[0], kept, top)
        return (lines, row[0])[::direction][0], levels, row[0]
''',
)

ivl = os.path.join(dst, "interval.py")
replace(
    ivl,
    '''                new.append(
                    Line(a + v, a, rem, ws, line.wr, line.wwall)
                    if self.direction == 1
                    else Line(a, a - v, rem, ws, line.wr, line.wwall)
                )
''',
    '''                new.append(
                    Line(*(a + self.direction * v, a)[:: self.direction], rem, ws, line.wr, line.wwall)
                )
''',
)
replace(
    ivl,
    '''        self.node, self.direction = node, direction
        if direction == 1:
            node.interval += 1
''',
    '''        self.node, self.direction = node, direction
        node.interval += direction
        if direction == 1:
''',
)
replace(
    ivl,
    '''    if direction == -1:
        node.interval -= 1
        return
''',
    '''    if direction == -1:
        return
''',
)
replace(
    ivl,
    "the kick and the division are the same acts at -1 and the interval is counted down.",
    "the kick and the division are the same acts at -1 and the interval is counted by the direction at the Interval's making (RW-S1).",
)
print(root)
