"""bh1's flagged COPY of the engine (engine-5.0-test d752d586f, the symmetric ride), written from the copy under e5src/ by exact text
replacements, each named below; the engine's own files are never touched. The flag is the module bh1_flag.FORM (no file key, no
environment switch): None is the engine bit for bit; "horizon" reads a Link with a frozen end at the wall (the factor 0, the same from
both ends); "identity" leaves a frozen Node's state unchanged (no rotate, no write, no swap; its clock stands); "write" refuses the
carrier's write at a frozen Node (the numerator 0 there, the step the letter's free line); the forms compose ("horizon+identity",
"horizon+write"). Run: python make_e5flag.py  (writes e5flag/ beside e5src/; refuses where a replacement does not match exactly once).
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "e5src", "event_universe")
DST = os.path.join(HERE, "e5flag", "event_universe")

FLAG = '''"""bh1's flag (2026-10-25): the form of the frozen Node under test in this COPY of the engine; FORM None is the engine bit for bit (every mask all False, every call the engine's own)."""
from __future__ import annotations

from typing import Any

import numpy as np

FORM: str | None = None  # None | "horizon" | "identity" | "write" | "horizon+identity" | "horizon+write"


def horizon() -> bool:
    """A Link with a frozen end is read at the wall (the horizon widened to the frozen Node's six Links)."""
    return FORM is not None and "horizon" in FORM


def identity() -> bool:
    """A frozen Node's state stands: no act changes it (the frozen mask kept in the frame as the turned mask is)."""
    return FORM is not None and "identity" in FORM


def write_stops() -> bool:
    """The carrier's write is refused at a frozen Node (the numerator 0 there); the step is the letter's."""
    return FORM is not None and "write" in FORM


def mask(found: Any, shape: tuple[int, ...]) -> Any:
    """The frozen mask under a form; all False without one (the engine's path)."""
    return np.asarray(found, dtype=bool) if FORM is not None else np.zeros(shape, dtype=bool)


def swap(node: Any, held: Any, frozen: Any) -> Any:
    """The swap at the top with its trigger off at the frozen Nodes under the identity form; node.swap bit for bit otherwise (its body repeated here with the one mask)."""
    if not identity():
        return node.swap(held)
    from event_universe import readings
    from event_universe.rows import CARRIER

    k = node.rows_.index(node.row(CARRIER))
    x0, x1, x2 = held[k][0].before, held[k][0].now, node.row(CARRIER).lines[0].now
    peak = np.vectorize(
        lambda a, b, c: (int(a) <= int(b) and int(c) <= int(b) and (int(a) < int(b) or int(c) < int(b))),
        otypes=[bool],
    )
    xf = readings.floor(node)
    below = np.vectorize(lambda a, c: int(a) < xf or int(c) < xf, otypes=[bool])
    top = (peak(x0, x1, x2) | below(x0, x2)) & ~np.asarray(frozen, dtype=bool)
    node.turned = top
    if top.any():
        node.counts["turns"] += int(top.sum())
        node.turns.append((node.interval, int(top.sum())))
        node.exchange(top, held)
    return top
'''

REPLACEMENTS = {
    "interval.py": [
        # 1. the flag's import
        (
            "from event_universe.rows import CARRIER, PLANE, " + "POTENTIAL, TRACE, Line, Row, zeros\n",
            "from event_universe.rows import CARRIER, PLANE, " + "POTENTIAL, TRACE, Line, Row, zeros\nfrom event_universe import bh1_flag  # bh1: the frozen Node's form under test\n",
        ),
        # 2. the frozen mask and the still mask at the interval's start (backward from the frame under the identity form, as `turned` is)
        (
            '            self.top = frame["turned"]\n        self.held = [[line.copy() for line in row] for row in node.rows()]\n',
            '            self.top = frame["turned"]\n        self.frozen: Any = np.zeros(node.shape, dtype=bool)  # bh1: the frozen mask (the Link pace 0 at the start content), forward read in `readings`, backward from the frame under the identity form (as `turned` is) and from the content otherwise\n        if direction == -1 and bh1_flag.identity():\n            self.frozen = frame["frozen"]\n        self.still = self.top | self.frozen  # bh1: the Nodes whose state the acts leave unchanged (the turned by the exchange, the frozen by the identity)\n        self.held = [[line.copy() for line in row] for row in node.rows()]\n',
        ),
        # 3. the start level read at a still Node from its now slot
        (
            "        return line.now if self.direction == 1 else np.where(self.top, line.now, line.before)\n",
            "        return line.now if self.direction == 1 else np.where(self.still, line.now, line.before)  # bh1: still, not top\n",
        ),
        # 4. the acts' ends: the restore backward at every still Node
        (
            "        return self.top, None if self.kept is None else self.kept[self.where[id(row)]]\n",
            "        return self.still, None if self.kept is None else self.kept[self.where[id(row)]]  # bh1: still, not top\n",
        ),
        # 5. the readings: the frozen mask from the start content, the clock standing at a frozen Node under the identity, the factors with the mask
        (
            "        self.p0 = paces.clock_of(node.gamma, self.c)\n        node.proper = node.proper + self.direction * self.p0\n        self.factors = node.link_factors([self.at(line) for line in self.carrier.lines[1 : 1 + AXES]])\n",
            "        self.p0 = paces.clock_of(node.gamma, self.c)\n        if self.direction == 1 or not bh1_flag.identity():  # bh1: the frozen mask from the start content (forward always; backward where no frame is needed)\n            self.frozen = bh1_flag.mask(np.asarray(paces.link_pace_of(node.gamma, self.c), dtype=object) == 0, node.shape)\n            self.still = (self.top | self.frozen) if bh1_flag.identity() else self.top\n        node.proper = node.proper + self.direction * (np.where(self.frozen, 0, self.p0) if bh1_flag.identity() else self.p0)  # bh1: the frozen Node's clock stands under the identity form\n        self.factors = node.link_factors([self.at(line) for line in self.carrier.lines[1 : 1 + AXES]], self.frozen)  # bh1: the frozen mask to the factors\n",
        ),
        # 6. the carrier's write refused at the frozen Nodes under the write form
        (
            "        self.out[k] = node.carried(\n            self.rows[k],\n            node.rule_of(carrier, self.c, self.factors),\n",
            "        if bh1_flag.write_stops():  # bh1: the write refused at the frozen Nodes (the numerator 0 there; the step the letter's free line)\n            numerators = [None if n is None else np.where(self.frozen, 0, n) for n in numerators]\n        self.out[k] = node.carried(\n            self.rows[k],\n            node.rule_of(carrier, self.c, self.factors),\n",
        ),
        # 7. the riders' restore backward at every still Node
        (
            "                node.restore(new, self.kept[k], self.top)\n",
            "                node.restore(new, self.kept[k], self.still)  # bh1: still, not top\n",
        ),
        # 8. the swap's trigger masked, the frozen mask in the frame
        (
            '        top = node.swap(self.held)\n        log_from = len(node.log)\n        node.click(self.plane_starts, self.held)\n        node.stack.append({"turned": top, "counters": counters, "log_from": log_from})\n',
            '        top = bh1_flag.swap(node, self.held, self.frozen)  # bh1: no swap at a frozen Node under the identity form\n        log_from = len(node.log)\n        node.click(self.plane_starts, self.held)\n        node.stack.append({"turned": top, "frozen": self.frozen, "counters": counters, "log_from": log_from})  # bh1: the frozen mask kept beside the turned\n',
        ),
        # 9. the identity forward: every line at a frozen Node set back to the held pre-state
        (
            "    node.set_rows(interval.out)\n    if direction == -1:\n        node.interval -= 1\n        return\n    interval.close()\n",
            "    node.set_rows(interval.out)\n    if direction == 1 and bh1_flag.identity() and interval.frozen.any():  # bh1: the identity at the frozen Nodes, every line set back to the held pre-state\n        for lines, h in zip(node.rows(), interval.held, strict=True):\n            node.restore(lines, h, interval.frozen)\n    if direction == -1:\n        node.interval -= 1\n        return\n    interval.close()\n",
        ),
    ],
    "readings.py": [
        (
            "from event_universe.rows import CARRIER, Line, zeros\n",
            "from event_universe.rows import CARRIER, Line, zeros\nfrom event_universe import bh1_flag  # bh1\n",
        ),
        (
            "def link_factors(node: Node, axis_levels: list[Any] | None = None) -> tuple[Any, ...]:\n",
            "def link_factors(node: Node, axis_levels: list[Any] | None = None, frozen: Any = None) -> tuple[Any, ...]:  # bh1: the frozen mask\n",
        ),
        (
            "        t = paces.rounded(summed, 2)\n        factor = np.vectorize(\n",
            "        t = paces.rounded(summed, 2)\n        if frozen is not None and bh1_flag.horizon():  # bh1: a Link with a frozen end is read at the wall (the tension Gamma there, the factor 0, the same from both ends)\n            (ends,), _o, _ff = link(port, even=(np.asarray(frozen, dtype=object) * 1,))\n            t = np.where(np.asarray(ends, dtype=object) > 0, node.gamma, t)\n        factor = np.vectorize(\n",
        ),
    ],
    "node.py": [
        (
            '    def link_factors(self, axis_levels: list[Any] | None = None) -> tuple[Any, ...]:\n        """The Link factor at each Port (readings.link_factors)."""\n        return readings.link_factors(self, axis_levels)\n',
            '    def link_factors(self, axis_levels: list[Any] | None = None, frozen: Any = None) -> tuple[Any, ...]:  # bh1: the frozen mask through\n        """The Link factor at each Port (readings.link_factors)."""\n        return readings.link_factors(self, axis_levels, frozen)\n',
        ),
    ],
    "close.py": [
        (
            "from event_universe.rows import PLANE, POTENTIAL, Line\n",
            "from event_universe.rows import PLANE, POTENTIAL, Line\nfrom event_universe import bh1_flag  # bh1\n",
        ),
        (
            "    c = node.start_content\n    factors = node.link_factors()\n",
            "    c = node.start_content\n    pace0 = paces.link_pace_of(node.gamma, c)  # bh1: the frozen mask before the factors\n    frozen0 = np.asarray(pace0, dtype=object) == 0 if np.ndim(pace0) else np.zeros(node.shape, dtype=bool)\n    factors = node.link_factors(None, bh1_flag.mask(frozen0, node.shape))  # bh1: the frozen Links at the wall under the horizon form\n",
        ),
    ],
    "run.py": [
        (
            "from event_universe.rows import CARRIER, PLANE, " + "POTENTIAL, zeros\n",
            "from event_universe.rows import CARRIER, PLANE, " + "POTENTIAL, zeros\nfrom event_universe import bh1_flag  # bh1\n",
        ),
        (
            "    pace = paces.link_pace_of(node.gamma, content)\n    factors = node.link_factors()\n",
            "    pace = paces.link_pace_of(node.gamma, content)\n    factors = node.link_factors(None, bh1_flag.mask(np.asarray(pace, dtype=object) == 0, node.shape))  # bh1: the frozen Links counted among the held\n",
        ),
    ],
}


def main() -> None:
    if os.path.exists(os.path.dirname(DST)):
        shutil.rmtree(os.path.dirname(DST))
    shutil.copytree(os.path.dirname(SRC), os.path.dirname(DST), ignore=shutil.ignore_patterns("__pycache__"))
    count = 0
    for name, pairs in REPLACEMENTS.items():
        path = os.path.join(DST, name)
        text = open(path, encoding="utf-8").read()
        for old, new in pairs:
            if text.count(old) != 1:
                sys.exit("REFUSED: %s: the text occurs %d times, not once:\n%s" % (name, text.count(old), old))
            text = text.replace(old, new)
            count += 1
        open(path, "w", encoding="utf-8").write(text)
    open(os.path.join(DST, "bh1_flag.py"), "w", encoding="utf-8").write(FLAG)
    print("e5flag written:", count, "replacements in", len(REPLACEMENTS), "files, plus bh1_flag.py")


if __name__ == "__main__":
    main()
