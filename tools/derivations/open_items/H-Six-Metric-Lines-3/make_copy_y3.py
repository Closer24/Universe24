"""The hand H-Six-Metric-Lines-3 (2026-10-26): a copy of src with the six metric lines written, read and run back, behind the flag Y3_METRIC=1 (`python make_copy_y3.py <src dir> <copy dir>`), or with the flag removed for David's patch (`python make_copy_y3.py <src dir> <stage src dir> --stage`). Every change is an exact replacement named here; a replacement that misses is refused by name. Integers only; no name of a row; no number beyond the law's own 1, 2, 3 and 6."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

FLAG = "Y3_METRIC"


def replacements(staged: bool) -> dict[str, list[tuple[str, str]]]:
    """The exact replacements per module, flagged (the head's path textually kept with the flag off) or staged (the one path)."""
    guard = "" if staged else "if METRIC:"
    found: dict[str, list[tuple[str, str]]] = {}

    # core/ports.py: the one place the flag is read (flagged copy alone)
    if not staged:
        found["core/ports.py"] = [
            (
                "from typing import Any\n\nAXES = 3",
                "import os\nfrom typing import Any\n\nMETRIC = (\n    os.environ.get(\"Y3_METRIC\") == \"1\"\n)  # the hand H-Six-Metric-Lines-3 (2026-10-26): the six metric lines written, read and run back (Y-S1 to Y-S3); off, every path the head's bit for bit\n\nAXES = 3",
            )
        ]

    # links.py: the Link's record carries the flux lines' odd part; the shears' parts; the count flux of a record on a Link
    links = [
        (
            "from event_universe.core.ports import AXES, PORT_SIDES, across, wrap",
            "from event_universe.core.ports import AXES, PORT_SIDES, across, wrap"
            if staged
            else "from event_universe.core.ports import AXES, METRIC, PORT_SIDES, across, wrap",
        ),
        (
            '    __slots__ = ("factor", "frame", "cosine", "sine", "odd")\n\n    def __init__(self, factor: Any, frame: Any, cosine: Any, sine: Any, odd: Any) -> None:\n        self.factor, self.frame, self.cosine, self.sine, self.odd = factor, frame, cosine, sine, odd',
            '    __slots__ = ("factor", "frame", "cosine", "sine", "odd", "flux")\n\n    def __init__(\n        self, factor: Any, frame: Any, cosine: Any, sine: Any, odd: Any, flux: Any = 0\n    ) -> None:\n        self.factor, self.frame, self.cosine, self.sine, self.odd = factor, frame, cosine, sine, odd\n        self.flux = flux  # the metric\'s flux line on the Link\'s axis summed over the two ends with the Port\'s sign, n_ij = V_a(i) + V_a(j) = -n_ji (Y-S2), read as the odd line is',
        ),
        (
            "def links_of(\n    factors: tuple[Any, ...], frames: list[Any], phases: list[tuple[Any, Any]], odd_lines: list[Any]\n) -> list[Link]:",
            "def links_of(\n    factors: tuple[Any, ...],\n    frames: list[Any],\n    phases: list[tuple[Any, Any]],\n    odd_lines: list[Any],\n    flux_lines: list[Any] | None = None,\n) -> list[Link]:",
        ),
        (
            "        _even, (n,), _f = link(port, odd=(odd_lines[axis],))\n        found.append(Link(factors[port], frames[port], phases[port][0], phases[port][1], n))",
            "        _even, (n,), _f = link(port, odd=(odd_lines[axis],))\n        v = 0 if flux_lines is None else link(port, odd=(flux_lines[axis],))[1][0]\n        found.append(Link(factors[port], frames[port], phases[port][0], phases[port][1], n, v))",
        ),
        (
            "def turned(xs: list[Any], at: Link, scale: Any, gamma: Any) -> list[Any]:",
            "def turned(xs: list[Any], at: Link, scale: Any, gamma: Any, rotation: Any = 0) -> list[Any]:",
        ),
        (
            "    wl = 4 * gamma\n    tc, ts, tw = wl * wl - at.odd * at.odd, 2 * wl * at.odd, wl * wl + at.odd * at.odd\n    found: list[Any] = []",
            "    wl = 4 * gamma\n    tc, ts, tw = wl * wl - at.odd * at.odd, 2 * wl * at.odd, wl * wl + at.odd * at.odd\n"
            + ("    " if staged else "    if METRIC:\n        ")
            + "# Y-S2: the flux lines' fold, the Link's odd part n_ij turned at the record's rest rotation K = omega_0 Gamma as a second tangent triple (W^2 - m^2, 2 W m, W^2 + m^2) with W = Gamma^2 and m = 3 K n (the sine 6 K n / Gamma^2 to first order, the fold form of The clock family on the Ports), the two triples multiplied exactly and rounded once per part with the pair's one rounding; a row whose rotation is 0 or a Link whose flux is 0 is turned as before, bit for bit\n"
            + ("    " if staged else "        ")
            + "m, w2 = 3 * rotation * at.flux, gamma * gamma\n"
            + ("    " if staged else "        ")
            + "fc, fs, fw = w2 * w2 - m * m, 2 * w2 * m, w2 * w2 + m * m\n"
            + ("    " if staged else "        ")
            + "tc, ts, tw = tc * fc - ts * fs, ts * fc + tc * fs, tw * fw\n    found: list[Any] = []",
        ),
        (
            "def tensor_parts(parts: list[Any]) -> tuple[Any, list[Any]]:",
            'def shear_parts(\n    rows: list[tuple[list[Any], int, list[list[int]]]], shape: tuple[int, ...]\n) -> list[Any]:\n    """The stress tensor\'s three off-diagonal parts on the axis pairs (a, a + 1): xy, yz, zx, the shears\' source (Y-S1): SUM over records of num x d_a.G.d_b, the Node\'s product of its two centred gradients, T_2g under the cube\'s 48 (the sign the product of the two axes\' signs), one Link\'s reach, the same act on every record as the diagonal parts (`stress_parts`); 0 at a Node where one body stands alone, the two-body tidal term between two."""\n    parts = [zeros(shape) for _ in range(AXES)]\n    for levels, num, g in rows:\n        d = [[gradient(x, a) for x in levels] for a in range(AXES)]\n        for a in range(AXES):\n            b = wrap(a + 1, AXES)\n            pairs = ((k, m) for k in range(len(levels)) for m in range(len(levels)) if g[k][m])\n            parts[a] = parts[a] + num * sum((g[k][m] * d[a][k] * d[b][m] for k, m in pairs), start=0)\n    return parts\n\n\ndef tensor_parts(parts: list[Any]) -> tuple[Any, list[Any]]:',
        ),
        (
            "def net_current(line: Line, axis: int) -> Any:",
            'def net_flux(g: list[list[int]], nows: list[Any], velocities: list[Any], axis: int) -> Any:\n    """A record\'s count flux on an axis at every Node (Y-S1, Y-S3): u.G.D_a N, the record\'s own velocity against the centred gradient of its levels at the start through the axis\'s two Links (the momentum density, the continuum\'s T_0a; summed over the board the lattice momentum of The lattice momentum, SUM_i F(i, i + a) with F_ij = u_i N_j - N_i u_j), odd under the axis\'s inversion (T_1u), one Link\'s reach, no division; the flux lines\' source."""\n    d = [gradient(n, axis) for n in nows]\n    pairs = [(k, m) for k in range(len(nows)) for m in range(len(nows)) if g[k][m]]\n    return sum((g[k][m] * velocities[k] * d[m] for k, m in pairs), start=0)\n\n\ndef net_current(line: Line, axis: int) -> Any:',
        ),
    ]
    found["links.py"] = links

    # node.py: the record's rest rotation to the unit; the arrivals turned with it
    found["node.py"] = [
        (
            "        self.lattices: dict[tuple[int, int, tuple[int, ...]], int] = {}\n",
            "        self.lattices: dict[tuple[int, int, tuple[int, ...]], int] = {}\n        self.rotations: dict[tuple[int, int], int] = {}\n",
        ),
        (
            '    def turned_arrival(self, arrivals: list[Any], port: int, turn: list[Link] | None) -> list[Any]:\n        """The arrivals of a row\'s lines at one Port, read in the Node\'s frame (the row\'s conjugation where the frame sign is -1, gram.conjugated) and turned plane by plane by the Link\'s record (links.turned); a row of one line is turned by the identity; `turn` None is the identity for every shape."""\n        if turn is None or len(arrivals) == 1:\n            return arrivals\n        at = turn[port]\n        return turned(gram.conjugated(len(arrivals), arrivals, at.frame), at, self.X, self.gamma)\n\n    def arrivals(self, at: list[Any], r: rule3.Rule, turn: list[Link] | None) -> list[Any]:\n        """The Links\' part of Rule3\'s total for a row\'s lines at every Node, SUM_j R_j m_j, the arrivals at each Port turned as the row\'s shape turns them."""\n        totals: list[Any] = [0] * len(at)\n        for port, reach in enumerate(r.reaches):\n            found = self.turned_arrival([across(a, port) for a in at], port, turn)',
            '    def rotation_of(self, pair: tuple[int, int]) -> int:\n        """The record\'s rest rotation to the unit, K = omega_0 Gamma with cos omega_0 = num / den (Y-S2, The clock family on the Ports): the count along the law\'s orbit at the step 1 / Gamma at which the orbit\'s cosine first falls to num / den (gram.cosine_count, a search by comparisons and no root), found once per pair."""\n        if pair not in self.rotations:\n            self.rotations[pair] = gram.cosine_count(self, pair[0], pair[1])\n        return self.rotations[pair]\n\n    def turned_arrival(\n        self, arrivals: list[Any], port: int, turn: list[Link] | None, rotation: Any = 0\n    ) -> list[Any]:\n        """The arrivals of a row\'s lines at one Port, read in the Node\'s frame (the row\'s conjugation where the frame sign is -1, gram.conjugated) and turned plane by plane by the Link\'s record (links.turned) at the row\'s rest rotation `rotation` (Y-S2); a row of one line is turned by the identity; `turn` None is the identity for every shape."""\n        if turn is None or len(arrivals) == 1:\n            return arrivals\n        at = turn[port]\n        return turned(\n            gram.conjugated(len(arrivals), arrivals, at.frame), at, self.X, self.gamma, rotation\n        )\n\n    def arrivals(\n        self, at: list[Any], r: rule3.Rule, turn: list[Link] | None, rotation: Any = 0\n    ) -> list[Any]:\n        """The Links\' part of Rule3\'s total for a row\'s lines at every Node, SUM_j R_j m_j, the arrivals at each Port turned as the row\'s shape turns them, at the row\'s rest rotation."""\n        totals: list[Any] = [0] * len(at)\n        for port, reach in enumerate(r.reaches):\n            found = self.turned_arrival([across(a, port) for a in at], port, turn, rotation)',
        ),
    ]

    # interval.py: the shears read, the Links carry the flux lines, the arrow at a still Node, the flux source in and out, the nine lines written by position
    interval = [
        (
            "from event_universe.core.ports import AXES, PORTS, across",
            "from event_universe.core.ports import AXES, PORTS, across"
            if staged
            else "from event_universe.core.ports import AXES, " + "METRIC, PORTS, across",
        ),
        (
            "from event_universe.links import links_of, stress_parts, tensor_parts",
            "from event_universe.links import links_of, net_flux, shear_parts, stress_parts, tensor_parts",
        ),
        (
            "        stress = stress_parts(\n            [\n                ([self.at(line) for line in r.lines], r.pair[0], gram.gram(r.shape))\n                for r in self.records\n                if r.pair\n            ],\n            node.shape,\n        )\n        self.trace, self.traceless = tensor_parts(stress)",
            "        sources = [\n            ([self.at(line) for line in r.lines], r.pair[0], gram.gram(r.shape))\n            for r in self.records\n            if r.pair\n        ]\n        self.trace, self.traceless = tensor_parts(stress_parts(sources, node.shape))\n        self.shear = shear_parts(sources, node.shape)  # Y-S1: the shears' source, the records' d_a.G.d_b",
        ),
        (
            "        self.links = links_of(self.factors, self.frames, self.phases, self.odd)",
            "        self.links = links_of(\n            self.factors,\n            self.frames,\n            self.phases,\n            self.odd,\n            [self.at(line) for line in self.carrier.lines[1 + AXES : 1 + 2 * AXES]]"
            + ("" if staged else " if METRIC else None")
            + ",\n        )  # Y-S2: the metric's flux lines along the six Links, the Link's odd part read from the start's levels in either direction",
        ),
        (
            "            turn = self.links if r.gap else None\n            k = self.where[id(r)]\n            self.walls[k] = rule.wall\n            self.starts[k] = [self.at(line) for line in self.lines(r)]\n            arrivals = node.arrivals(self.starts[k], rule, turn)",
            "            turn = self.links if r.gap else None\n            k = self.where[id(r)]\n            self.walls[k] = rule.wall\n            self.starts[k] = [self.at(line) for line in self.lines(r)]\n            rotation = node.rotation_of(r.pair) if r.gap"
            + ("" if staged else " and METRIC")
            + " else 0  # Y-S2: the row's rest rotation; the row at the gap 0 is turned by nothing\n            arrivals = node.arrivals(self.starts[k], rule, turn, rotation)",
        ),
        (
            "        d = 2 * node.w * self.x_now\n        w_side = self.mean_wall()\n        charge = zeros(node.shape)\n        for r in self.riders:\n            k = self.where[id(r)]\n            ws, ds, g = self.scales[k] * w_side, self.scales[k] * d, gram.gram(r.shape)\n            p_side = [ws * (line.now - line.before) + line.rem - half(ws) for line in self.rows[k]]\n            p_other = [\n                p + self.direction * self.x_now * f for p, f in zip(p_side, self.force[k], strict=True)\n            ]\n            if r is self.potential:\n                line = self.rows[k][0]\n                q, line.wr = carried_division(charge, line.wwall, line.wr, self.direction)\n                p_other[0] = p_other[0] + self.direction * node.w * self.x_now * q\n            u_in = [paces.odd_rounded(2 * p + 1, ds) for p in p_side]\n            u_out = [paces.odd_rounded(2 * p + 1, ds) for p in p_other]\n            if r.gap:\n                gj = gram.matmul(g, gram.rotation(r.shape))\n                charge = (\n                    charge + gram.form(gj, self.starts[k], u_in) + gram.form(gj, self.starts[k], u_out)\n                )",
            "        d = 2 * node.w * self.x_now\n        w_side = self.mean_wall()\n        charge = zeros(node.shape)\n        self.flux = [zeros(node.shape) for _ in range(AXES)]  # Y-S1: the flux lines' source\n        for r in self.riders:\n            k = self.where[id(r)]\n            ws, ds, g = self.scales[k] * w_side, self.scales[k] * d, gram.gram(r.shape)\n            p_side = [ws * (line.now - line.before) + line.rem - half(ws) for line in self.rows[k]]\n            p_other = [\n                p + self.direction * self.x_now * f for p, f in zip(p_side, self.force[k], strict=True)\n            ]\n            if r is self.potential:\n                line = self.rows[k][0]\n                q, line.wr = carried_division(charge, line.wwall, line.wr, self.direction)\n                p_other[0] = p_other[0] + self.direction * node.w * self.x_now * q\n            u_in = [paces.odd_rounded(2 * p + 1, ds) for p in p_side]\n            u_out = [paces.odd_rounded(2 * p + 1, ds) for p in p_other]\n            if r.gap:\n                gj = gram.matmul(g, gram.rotation(r.shape))\n                charge = (\n                    charge + gram.form(gj, self.starts[k], u_in) + gram.form(gj, self.starts[k], u_out)\n                )\n            if r in self.records:  # Y-S3: the count's flux on each axis, the record's own velocities in and out against the centred gradient of its levels at the start, u_in.G.D_a N + u_out.G.D_a N (the momentum density, T_1u), one Link's reach and the same integers in either direction: no neighbour's velocity or `before` is read\n                for u in (u_in, u_out):\n                    for a in range(AXES):\n                        self.flux[a] = self.flux[a] + r.pair[0] * net_flux(g, self.starts[k], u, a)",
        ),
        (
            "        numerators += [self.traceless[a] * p02 for a in range(AXES)] + [None] * (\n            carrier.shape - 1 - AXES\n        )",
            "        numerators += [\n            part * p02 for part in (*self.traceless, *self.flux, *self.shear)\n        ]  # the nine axis lines by the position of their reading (Y-S1): the tensions traceless, the flux lines, the shears, at the one wall"
            if staged
            else "        if METRIC:  # the nine axis lines by the position of their reading (Y-S1): the tensions traceless, the flux lines, the shears, at the one wall\n            numerators += [part * p02 for part in (*self.traceless, *self.flux, *self.shear)]\n        else:\n            numerators += [self.traceless[a] * p02 for a in range(AXES)] + [None] * (\n                carrier.shape - 1 - AXES\n            )",
        ),
    ]
    found["interval.py"] = interval

    # rows.py: the carrier's comment names its ten lines
    found["rows.py"] = [
        (
            "CARRIER = 10  # the shape of the row that carries the wall (the metric's row): its time line and three axis lines",
            "CARRIER = 10  # the shape of the row that carries the wall (the metric's row): its time line, the three tensions, the three flux lines and the three shears (Y-S1)",
        )
    ]
    return found


def apply(src: Path, out: Path, staged: bool) -> None:
    """The copy made and every replacement applied once, or refused by name."""
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(src, out)
    for name, pairs in replacements(staged).items():
        path = out / "event_universe" / name
        text = path.read_text(encoding="utf-8")
        for old, new in pairs:
            if text.count(old) != 1:
                raise ValueError(f"{name}: the text to replace stands {text.count(old)} times: {old[:60]!r}")
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")
        print("replaced", name, len(pairs))


if __name__ == "__main__":
    apply(Path(sys.argv[1]), Path(sys.argv[2]), "--stage" in sys.argv)
