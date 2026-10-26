"""rw1's flagged copy of the engine: src/event_universe copied whole to /dev/shm/tmp/rw1/src_rw1/event_universe (never in the worktree), one fold behind one environment flag, empty for the head bit for bit.
RW1_FORM "1" (the read is the write at -1): (a) rule3.carried_division: the backward act spelled as the forward act conjugated by the one rule's mirror, the remainder mirrored in, the forward division, the remainder mirrored out, the quotient as it falls (the theorem: carried_division(t, w, r, -1) == (q, w - 1 - r') where (q, r') = carried_division(t, w, w - 1 - r, 1)); (b) node.rotate: the two slots read as one pair reversed by the direction, (a, y) = (now, before)[::direction], the total S a - w y + f + m in the letter's own form in both directions, the new line the pair (q, a)[::direction]; (c) node.act: one path, the rotate and the write in the direction's order, the levels read between the two acts; (d) interval.division: the riding line's new pair (a + direction v, a)[::direction]; (e) the interval counted by the direction at one place."""
import os
import shutil
import sys

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "..", "src", "event_universe")
root = sys.argv[1] if len(sys.argv) > 1 else "/dev/shm/tmp/rw1/src_rw1"
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, old, new):
    text = open(path).read()
    assert text.count(old) == 1, ("the replacement site is not unique", path, old[:60])
    open(path, "w").write(text.replace(old, new))


FLAG = 'RW1_FORM = os.environ.get("RW1_FORM", "")  # rw1\'s flag: empty is the head bit for bit\n'

rule3 = os.path.join(dst, "core", "rule3.py")
replace(rule3, "from typing import Any, NamedTuple\n", "import os\nfrom typing import Any, NamedTuple\n\n" + FLAG)
replace(
    rule3,
    """    total = direction * total + remainder
    quotient = total // wall
    return direction * quotient, total - wall * quotient
""",
    """    if RW1_FORM == "1":  # rw1: the act at -1 is the act at +1 conjugated by the one rule's mirror
        carried = remainder if direction == 1 else wall - 1 - remainder
        carried = total + carried
        quotient = carried // wall
        rest = carried - wall * quotient
        return quotient, rest if direction == 1 else wall - 1 - rest
    total = direction * total + remainder
    quotient = total // wall
    return direction * quotient, total - wall * quotient
""",
)

nodepy = os.path.join(dst, "node.py")
replace(nodepy, "import hashlib\n", "import hashlib\nimport os\n")
replace(nodepy, "from event_universe import close, gram, interval, readings, seed, take\n", "from event_universe import close, gram, interval, readings, seed, take\n\n" + FLAG)
replace(
    nodepy,
    """        at = starts or [line.now if direction == 1 else line.before for line in lines]
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
""",
    """        if RW1_FORM == "1":  # rw1: the two slots one pair read reversed by the direction
            pairs = [(line.now, line.before)[::direction] for line in lines]
            at = starts or [a for a, _y in pairs]
            fluxes = flux or [0] * len(lines)
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
""",
)
replace(
    nodepy,
    """        if direction == 1:
            stepped = self.rotate(lines, r, turn, 1, flux, None)
            levels = [line.now for line in stepped]
            for line, n in zip(stepped, numerators, strict=True):
                if n is not None:
                    self.write(line, n, 1)
            return lines, levels, stepped
        starts = None if kept is None else [np.where(top, line.now, line.before) for line in lines]
""",
    """        if RW1_FORM == "1":  # rw1: one path, the two acts in the direction's order
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
        if direction == 1:
            stepped = self.rotate(lines, r, turn, 1, flux, None)
            levels = [line.now for line in stepped]
            for line, n in zip(stepped, numerators, strict=True):
                if n is not None:
                    self.write(line, n, 1)
            return lines, levels, stepped
        starts = None if kept is None else [np.where(top, line.now, line.before) for line in lines]
""",
)

ivl = os.path.join(dst, "interval.py")
replace(ivl, "from typing import TYPE_CHECKING, Any\n", "import os\nfrom typing import TYPE_CHECKING, Any\n\n" + FLAG)
replace(
    ivl,
    """                new.append(
                    Line(a + v, a, rem, ws, line.wr, line.wwall)
                    if self.direction == 1
                    else Line(a, a - v, rem, ws, line.wr, line.wwall)
                )
""",
    """                if RW1_FORM == "1":  # rw1: the new pair read reversed by the direction
                    new.append(Line(*(a + self.direction * v, a)[:: self.direction], rem, ws, line.wr, line.wwall))
                else:
                    new.append(
                        Line(a + v, a, rem, ws, line.wr, line.wwall)
                        if self.direction == 1
                        else Line(a, a - v, rem, ws, line.wr, line.wwall)
                    )
""",
)
replace(
    ivl,
    """        self.node, self.direction = node, direction
        if direction == 1:
            node.interval += 1
""",
    """        self.node, self.direction = node, direction
        if RW1_FORM == "1":  # rw1: the interval counted by the direction at one place
            node.interval += direction
        if direction == 1:
            if RW1_FORM != "1":
                node.interval += 1
""",
)
replace(
    ivl,
    """    if direction == -1:
        node.interval -= 1
        return
""",
    """    if direction == -1:
        if RW1_FORM != "1":
            node.interval -= 1
        return
""",
)
print(root)
