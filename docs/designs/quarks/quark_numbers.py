"""The integers of QUARKS.md from the engine's own pure tables and the
law's push form: no engine run, no new law; every number of the design is
recomputed here and printed to `quark_numbers.out` beside it.

1. The quark rows of the family table: the PDG masses as unit counts at
   the register's grain (one unit = the electron's content), the charges
   as the rational pairs per unit of content at the register's charge
   scale (the proton's 7344), the fraction-free column scale Lambda per
   set of flavours, and the content the W carries at every `become` of
   the weak force (the charge balance of BEAM_LAW note 36 (iii)).
2. The push between two quark bodies within the reach of the strong
   column (BEAM_LAW step 4, note 31): the pair table for uu, ud and dd at
   one Link, the face diagonal and two Links, the electric part alone and
   with the register's strong value, and the least strong value that
   binds each pair at one Link.
3. The shapes of a nucleon of three quark bodies (a line with the odd
   quark in the middle or at an end, a corner, the equilateral triangle
   of the face-diagonal sublattice): the push on every body at L = 3,
   the net push on the set, and a toy of the step rule with the contact
   rule over 3000 intervals (the strong design's toy, section 5 of its
   `nucleus_numbers.py`).
4. The deuteron of two lines at adjacent Nodes: the push on each of the
   six bodies and the sum over each triple against series I's deuteron.
5. The read mass of the bound set: the sum of the declared contents, its
   ratio to nature's proton, the dressed glue that would restore the
   register's 1836 and 1839, and the neutron-proton difference.
6. The tower: the column vector of the set as the exact rational sum,
   the stabiliser of each shape in the cube's group of 48 (the group
   that acts on the three events), and the step regime (the width S).

    python docs/designs/quarks/quark_numbers.py      # writes quark_numbers.out
"""

from __future__ import annotations

import itertools
import math
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "src"))

import numpy as np  # noqa: E402

from event_universe.core.integer import by_clock, rational_sum  # noqa: E402
from event_universe.events.nature_beam import direction_flight  # noqa: E402

Vector = tuple[int, int, int]
Pair = tuple[int, int]
OUT: list[str] = []
Q = 64
AGE_MAX = 12
LIFETIME = 3
# The register's charge scale (series I): the proton's whole charge, rho 4
# per unit on 1836 units.
PROTON_CHARGE = 7344
# The register's strong value per unit of the held strong content and its
# range (series I: `nuclear`, sigma 10000, lifetime 3).
SIGMA = 10000
# The register's nucleon contents in units of the electron's (series I).
PROTON_UNITS = 1836
NEUTRON_UNITS = 1839
WORD = (1 << 62) - 1
LAMBDA_BOUND = (1 << 31) - 1

# One source for every number of nature: PDG 2024 (S. Navas et al., Phys.
# Rev. D 110, 030001 (2024)): the light quarks in the MS-bar scheme at 2
# GeV, the charm and bottom at their own scale, the top from the direct
# measurements; the electron from the same tables (CODATA 2018).
ELECTRON_MEV = 0.51099895
PDG_MEV = {"u": 2.16, "d": 4.70, "s": 93.5, "c": 1273.0, "b": 4183.0, "t": 172570.0}
CHARGE_THIRDS = {"u": 2, "d": -1, "s": -1, "c": 2, "b": -1, "t": 2}
PROTON_MEV = 938.27208816
NEUTRON_MEV = 939.56542052


def say(text: str = "") -> None:
    OUT.append(text)


# -- 1. the rows --------------------------------------------------------------------


def unit_count(mev: float) -> int:
    """The content in units of the electron's, the nearest whole count
    (record 243: the unit of content is the smallest mass; the register's
    grain is one electron)."""
    return round(mev / ELECTRON_MEV)


def quark_rows() -> dict[str, dict[str, object]]:
    rows: dict[str, dict[str, object]] = {}
    for name, mev in PDG_MEV.items():
        units = unit_count(mev)
        whole = Fraction(CHARGE_THIRDS[name] * PROTON_CHARGE, 3)
        rho = whole / units
        rows[name] = {
            "mev": mev,
            "ratio": mev / ELECTRON_MEV,
            "units": units,
            "whole_charge": whole,
            "rho": (rho.numerator, rho.denominator),
        }
    return rows


def lcm(values: list[int]) -> int:
    out = 1
    for v in values:
        out = out * v // math.gcd(out, v)
    return out


def section_1() -> dict[str, dict[str, object]]:
    say("# 1. The quark rows of the family table (PDG 2024; one unit = the electron's content)")
    rows = quark_rows()
    say(
        "flavour | mass (MeV) | mass / m_e | units (nearest) | whole charge (e = 7344) | "
        "rho per unit of content (reduced pair)"
    )
    for name, row in rows.items():
        whole = row["whole_charge"]
        assert isinstance(whole, Fraction)
        say(
            f"{name} | {row['mev']} | {row['ratio']:.4f} | {row['units']} | "
            f"{whole.numerator}/{whole.denominator} = {float(whole):.0f} | {row['rho']}"
        )
    say(
        f"the proton's row for comparison: 1836 units, whole charge 7344, rho (4, 1); "
        f"m_p / m_e = {PROTON_MEV / ELECTRON_MEV:.5f}; m_n / m_e = {NEUTRON_MEV / ELECTRON_MEV:.5f}; "
        f"(m_n - m_p) / m_e = {(NEUTRON_MEV - PROTON_MEV) / ELECTRON_MEV:.4f}"
    )
    say(
        f"the sum of the quark masses of a proton u u d: {2 * PDG_MEV['u'] + PDG_MEV['d']:.2f} MeV = "
        f"{(2 * PDG_MEV['u'] + PDG_MEV['d']) / PROTON_MEV * 100:.2f} % of the proton; "
        f"of a neutron u d d: {PDG_MEV['u'] + 2 * PDG_MEV['d']:.2f} MeV = "
        f"{(PDG_MEV['u'] + 2 * PDG_MEV['d']) / NEUTRON_MEV * 100:.2f} % of the neutron"
    )
    say()
    say(
        "## The fraction-free column scale Lambda (the lcm of the charge denominators; refused above 2^31 - 1)"
    )
    order = ["u", "d", "s", "c", "b", "t"]
    for k in range(2, 7):
        names = order[:k]
        dens = [rows[n]["rho"][1] for n in names]  # type: ignore[index]
        scale = lcm([int(d) for d in dens])
        verdict = "admitted" if scale <= LAMBDA_BOUND else "REFUSED at load"
        say(f"{'+'.join(names)}: Lambda = {scale:,} ({verdict}; Lambda^2 = {scale * scale:.3e})")
    say()
    say(
        "## The transformations of the weak force at the quark level: the content R the W (or the beta) carries"
    )
    say(
        "(the charge balance of note 36 (iii): rho_into x (M - R) + c_W = rho_from x M, so R = M_from - M_into)"
    )
    for a, b in (("d", "u"), ("s", "u"), ("c", "s"), ("b", "c"), ("t", "b"), ("u", "d")):
        m_from, m_into = int(rows[a]["units"]), int(rows[b]["units"])  # type: ignore[arg-type]
        r = m_from - m_into
        c_w = CHARGE_THIRDS[a] - CHARGE_THIRDS[b]
        c_w_whole = Fraction(c_w * PROTON_CHARGE, 3)
        state = (
            "payable"
            if r >= 1
            else "REFUSED (R below 1: the body would have to gain content, which no become does)"
        )
        say(
            f"{a} -> {b} + W: R = {m_from} - {m_into} = {r} units; the W's whole charge {c_w_whole}; {state}"
        )
    say(
        "the register's neutron (series J): n 1839 -> p 1836 with the beta's content 3 = 1839 - 1836, "
        "the same balance at the nucleon level"
    )
    say()
    return rows


# -- 2. the fan geometry and the push form -----------------------------------------------


def primitive(v: Vector) -> bool:
    return math.gcd(math.gcd(abs(v[0]), abs(v[1])), abs(v[2])) == 1


def fan_manhattan(bound: int) -> list[Vector]:
    """Every primitive direction with |a| + |b| + |c| <= bound (290 at 6):
    the fan of series I."""
    found = []
    for a in range(-bound, bound + 1):
        for b in range(-bound, bound + 1):
            for c in range(-bound, bound + 1):
                v = (a, b, c)
                if v != (0, 0, 0) and abs(a) + abs(b) + abs(c) <= bound and primitive(v):
                    found.append(v)
    found.sort()
    return found


class Fan:
    """The positions of every direction's ray at every age, exact, from the
    engine's own flight (BEAM_LAW section 3, the walk of step 1: the Link a
    ray crosses at an age is `Flight.walk_step`, the position's accumulator
    rule of the no-tables law, record 155)."""

    def __init__(self, vectors: list[Vector], age_max: int = AGE_MAX) -> None:
        self.vectors = vectors
        flight = direction_flight(tuple(vectors))
        self.labels = [tuple(int(c) for c in flight.labels[i]) for i in range(len(vectors))]
        self.arrivals_at: dict[Vector, list[tuple[int, int]]] = defaultdict(list)
        for i in range(len(vectors)):
            pos = (0, 0, 0)
            for age in range(age_max):
                step = tuple(int(c) for c in flight.walk_step(np.array([i]), np.array([age]))[0])
                if any(step):
                    pos = (pos[0] + step[0], pos[1] + step[1], pos[2] + step[2])
                    self.arrivals_at[pos].append((i, age + 1))
        self._cache: dict[tuple[Vector, int | None], tuple[int, Vector]] = {}

    def delivery(self, node: Vector, lifetime: int | None = None) -> tuple[int, Vector]:
        """The arrivals at `node` with age <= lifetime (all if None): the
        count and the vector sum of the unit labels u_d (the label moment
        of one unit per direction per shell)."""
        key = (node, lifetime)
        if key not in self._cache:
            count = 0
            total = [0, 0, 0]
            for i, age in self.arrivals_at.get(node, ()):
                if lifetime is not None and age > lifetime:
                    continue
                count += 1
                u = self.labels[i]
                total = [total[k] + u[k] for k in range(3)]
            self._cache[key] = (count, (total[0], total[1], total[2]))
        return self._cache[key]


FAN = Fan(fan_manhattan(6))

# The families of the quark worlds: the charge per unit of content as a
# pair, the strong value per unit and the lifetime (the range) of the
# family's rays.
Family = dict[str, object]


def families(
    rows: dict[str, dict[str, object]], sigma: int | Pair = SIGMA, lifetime: int = LIFETIME
) -> dict[str, Family]:
    """The families of the quark worlds; `sigma` the glue's strong value per
    unit of content, an integer or a pair (the dressed world's [10000, 606]:
    606 units held carry the strong charge 10000, as one unit at 10000)."""
    pair = (sigma, 1) if isinstance(sigma, int) else sigma
    out: dict[str, Family] = {}
    for name, row in rows.items():
        out[name] = {"charge": row["rho"], "strong": (0, 1), "lifetime": None}
    out["glue"] = {"charge": (0, 1), "strong": pair, "lifetime": lifetime}
    out["p"] = {"charge": (4, 1), "strong": (0, 1), "lifetime": None}
    out["n"] = {"charge": (0, 1), "strong": (0, 1), "lifetime": None}
    out["nuclear"] = {"charge": (0, 1), "strong": pair, "lifetime": lifetime}
    return out


def event_charges(held: dict[str, int], fams: dict[str, Family]) -> tuple[int, Pair, Pair]:
    """A measured event's content M, electric charge Q and strong charge G
    from what it holds, the two charges as reduced pairs (`rational_sum`,
    BEAM_LAW note 31 (i))."""
    content = sum(held.values())
    charge = rational_sum([(fams[f]["charge"][0] * m, fams[f]["charge"][1]) for f, m in held.items()])  # type: ignore[index]
    strong = rational_sum([(fams[f]["strong"][0] * m, fams[f]["strong"][1]) for f, m in held.items()])  # type: ignore[index]
    return content, charge, strong


def push_form(
    moment: Vector, content: int, charge: Pair, strong: Pair, rho: Pair, sigma: Pair, age: int
) -> Vector:
    """BEAM_LAW step 4: the push of a free family's group with the label
    moment V on a reader of content M, electric charge Q = (E, D) and
    strong charge G = (S, T), the emitter's rho = (n, d) and sigma =
    (s, t): -M V + [E n / (D d)] V - [S s / (T t)] V, the gravity exact and
    each column the whole part off the reader's clock by its own pair."""
    push = [-moment[axis] * content for axis in range(3)]
    e, d_reader = charge
    n, d = rho
    if e and n:
        for axis in range(3):
            total = moment[axis] * e * n
            whole = by_clock(age, abs(total), d_reader * d)
            push[axis] += -whole if total < 0 else whole
    s_reader, t_reader = strong
    s, t = sigma
    if s_reader and s:
        for axis in range(3):
            total = moment[axis] * s_reader * s
            whole = by_clock(age, abs(total), t_reader * t)
            push[axis] -= -whole if total < 0 else whole
    return (push[0], push[1], push[2])


def push_between(
    reader: dict[str, int],
    emitter: dict[str, int],
    relative: Vector,
    fams: dict[str, Family],
    age: int = 0,
) -> tuple[Vector, dict[str, tuple[int, Vector]]]:
    """The push per interval on the reader from the emitter's rays, the
    reader at `relative` from the emitter, one row of the emitter's held
    amount per direction per interval (`release` [1, 1]), each family cut
    at its lifetime."""
    content, charge, strong = event_charges(reader, fams)
    total = [0, 0, 0]
    parts: dict[str, tuple[int, Vector]] = {}
    for family, amount in emitter.items():
        count, label_sum = FAN.delivery(relative, fams[family]["lifetime"])  # type: ignore[arg-type]
        moment = (amount * label_sum[0], amount * label_sum[1], amount * label_sum[2])
        part = push_form(
            moment, content, charge, strong, fams[family]["charge"], fams[family]["strong"], age
        )  # type: ignore[arg-type]
        parts[family] = (count, part)
        total = [a + b for a, b in zip(total, part, strict=True)]
    return (total[0], total[1], total[2]), parts


def quark(name: str, rows: dict[str, dict[str, object]], glue: int = 1) -> dict[str, int]:
    return {name: int(rows[name]["units"]), "glue": glue}  # type: ignore[arg-type]


def section_2(rows: dict[str, dict[str, object]]) -> None:
    say(
        "# 2. The push between two quark bodies (u: 4 units + 1 glue; d: 9 units + 1 glue; release [1, 1]; the 290 fan)"
    )
    fams = families(rows)
    for name in ("u", "d"):
        m, qc, gc = event_charges(quark(name, rows), fams)
        say(
            f"{name}: held {quark(name, rows)}: M {m}, Q {qc}, G {gc}; Q^2 {qc[0] ** 2:,}; G^2 + M^2 {gc[0] ** 2 + m * m:,}"
        )
    say(
        "the symmetric form within the reach: push on A from B = (Q_A Q_B - G_A G_B - M_A M_B) x U(r) per unit per direction"
    )
    say("(a negative x component on a reader at (r, 0, 0) is toward the emitter: attraction)")
    say()
    say("## The delivery U per unit per direction at L = 3 (the 290 fan): the label sum at the Node")
    for node in (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0),
        (0, 1, 1),
        (2, 0, 0),
        (0, 2, 0),
        (1, 1, 1),
        (2, 1, 0),
        (3, 0, 0),
    ):
        for lifetime in (1, 2, 3, None):
            count, total = FAN.delivery(node, lifetime)
            say(f"  {node} L {lifetime}: {count} lines, U {total}")
    say(
        "(the flight table breaks the tie of a direction's first step in axis order, x first: the six neighbours are not equivalent at one Link)"
    )
    say()
    say(
        "## The pair table: the push on the reader per interval, electric alone (sigma 0) and with sigma 10000; L = 3"
    )
    say("pair | Node | sigma 0: push (parts electric, gravity) | sigma 10000: push | strong part")
    for a, b in (("u", "u"), ("u", "d"), ("d", "d")):
        for node in ((1, 0, 0), (1, 1, 0), (2, 0, 0), (3, 0, 0)):
            p0, parts0 = push_between(quark(a, rows), quark(b, rows), node, families(rows, sigma=0))
            p1, parts1 = push_between(quark(a, rows), quark(b, rows), node, fams)
            say(f"{a}{b} | {node} | {p0} | {p1} | glue {parts1['glue'][1]}")
    say()
    say("## The least strong value that binds each pair at one Link: G^2 + M_A M_B > Q_A Q_B")
    for a, b in (("u", "u"), ("u", "d"), ("d", "d")):
        ma, qa, _ = event_charges(quark(a, rows), fams)
        mb, qb, _ = event_charges(quark(b, rows), fams)
        need = qa[0] * qb[0] - ma * mb
        least = math.isqrt(need) + 1 if need > 0 else 0
        say(
            f"{a}{b}: Q_A Q_B = {qa[0] * qb[0]:,}, M_A M_B = {ma * mb}; "
            f"the least whole sigma (one glue unit each): {least} ({'binds electrically already' if need <= 0 else 'needed'})"
        )
    say(
        f"for comparison the register's two protons at one Link need G > 7111 with G = 10000 declared; "
        f"the ratio G^2 / Q_u^2 for the quarks at sigma 10000 is {10**8 / 4896**2:.2f} (the nucleons' 1.85)"
    )
    say()


# -- 3. the shapes and the toy -----------------------------------------------------------------

Shape = dict[str, tuple[Vector, dict[str, int]]]


def line(names: str, rows: dict[str, dict[str, object]], glue: int = 1) -> Shape:
    return {f"{n}{i}": ((i, 0, 0), quark(n, rows, glue)) for i, n in enumerate(names)}


def corner(names: str, rows: dict[str, dict[str, object]], glue: int = 1) -> Shape:
    positions = ((0, 0, 0), (1, 0, 0), (1, 1, 0))
    return {f"{n}{i}": (positions[i], quark(n, rows, glue)) for i, n in enumerate(names)}


def triangle(names: str, rows: dict[str, dict[str, object]], glue: int = 1) -> Shape:
    positions = ((1, 1, 0), (0, 1, 1), (1, 0, 1))
    return {f"{n}{i}": (positions[i], quark(n, rows, glue)) for i, n in enumerate(names)}


def shape_pushes(shape: Shape, fams: dict[str, Family]) -> dict[str, Vector]:
    out: dict[str, Vector] = {}
    for name, (pos, held) in shape.items():
        total = [0, 0, 0]
        for other, (opos, oheld) in shape.items():
            if other == name:
                continue
            rel = (pos[0] - opos[0], pos[1] - opos[1], pos[2] - opos[2])
            push, _ = push_between(held, oheld, rel, fams)
            total = [a + b for a, b in zip(total, push, strict=True)]
        out[name] = (total[0], total[1], total[2])
    return out


def centroid(shape: Shape) -> tuple[Fraction, Fraction, Fraction]:
    n = len(shape)
    return tuple(Fraction(sum(pos[k] for pos, _ in shape.values()), n) for k in range(3))  # type: ignore[return-value]


def inward(shape: Shape, pushes: dict[str, Vector]) -> bool:
    """Every body's push has no component pointing away from the centroid."""
    c = centroid(shape)
    for name, (pos, _) in shape.items():
        for k in range(3):
            toward = c[k] - pos[k]
            if pushes[name][k] != 0 and (toward == 0 or pushes[name][k] * toward < 0):
                return False
    return True


def toy(
    shape: Shape,
    fams: dict[str, Family],
    width: int,
    ticks: int = 3000,
    kicks: dict[str, Vector] | None = None,
) -> dict[str, object]:
    """The strong design's cluster toy: the fan's steady delivery at the
    bodies' current separations, the step drive per axis (BEAM_LAW step 5:
    one Link at or beyond Q S M + |p| of drive) and the contact through
    the table under `measure` (note 31 (ix): the refused step hands the
    axis component to the occupant); bodies move in number order."""
    names = list(shape)
    pos = {n: list(shape[n][0]) for n in names}
    held = {n: shape[n][1] for n in names}
    content = {n: event_charges(held[n], fams)[0] for n in names}
    p = {n: list((kicks or {}).get(n, (0, 0, 0))) for n in names}
    drive = {n: [0, 0, 0] for n in names}
    steps = 0
    first_step: tuple[int, str] | None = None
    contacts = 0
    largest_handed = 0
    largest_label = 0
    largest_spread = 0.0
    escaped: tuple[int, str] | None = None
    for tick in range(1, ticks + 1):
        # The pushes of the interval from the current separations.
        for n in names:
            total = [0, 0, 0]
            for o in names:
                if o == n:
                    continue
                rel = (pos[n][0] - pos[o][0], pos[n][1] - pos[o][1], pos[n][2] - pos[o][2])
                push, _ = push_between(held[n], held[o], rel, fams)
                total = [a + b for a, b in zip(total, push, strict=True)]
            p[n] = [a + b for a, b in zip(p[n], total, strict=True)]
            largest_label = max(largest_label, max(abs(c) for c in p[n]))
        # The step drive per axis, in number order; the contact at an occupied Node.
        for n in names:
            for axis in range(3):
                d = Q * width * content[n] + abs(p[n][axis])
                drive[n][axis] += p[n][axis]
                sign = 0
                if drive[n][axis] >= d:
                    sign = 1
                    drive[n][axis] -= d
                elif drive[n][axis] <= -d:
                    sign = -1
                    drive[n][axis] += d
                if sign == 0:
                    continue
                target = list(pos[n])
                target[axis] += sign
                occupant = next((o for o in names if o != n and pos[o] == target), None)
                if occupant is None:
                    pos[n] = target
                    steps += 1
                    if first_step is None:
                        first_step = (tick, n)
                else:
                    contacts += 1
                    handed = p[n][axis]
                    largest_handed = max(largest_handed, abs(handed))
                    p[occupant][axis] += handed
                    p[n][axis] = 0
        spread = max(math.dist(pos[a], pos[b]) for a, b in itertools.combinations(names, 2))
        largest_spread = max(largest_spread, spread)
        if escaped is None:
            for n in names:
                if max(abs(c) for c in pos[n]) > 9:
                    escaped = (tick, n)
                    break
    return {
        "escaped": escaped,
        "steps": steps,
        "first_step": first_step,
        "contacts": contacts,
        "largest_handed": largest_handed,
        "largest_label": largest_label,
        "largest_spread": round(largest_spread, 2),
        "final": {n: tuple(pos[n]) for n in names},
    }


SHAPES = {
    "proton line u d u (the odd quark in the middle)": ("udu", line),
    "proton line u u d (the odd quark at an end)": ("uud", line),
    "proton corner u d u (d at the corner)": ("udu", corner),
    "proton corner d u u (d at an arm)": ("duu", corner),
    "proton triangle u u d (the face-diagonal sublattice, mutual sqrt 2)": ("uud", triangle),
    "neutron line d u d (the odd quark in the middle)": ("dud", line),
    "neutron line d d u (the odd quark at an end)": ("ddu", line),
    "neutron corner d u d (u at the corner)": ("dud", corner),
    "neutron triangle u d d": ("udd", triangle),
}


def section_3(rows: dict[str, dict[str, object]], width: int) -> None:
    say(
        f"# 3. The shapes of a nucleon of three quark bodies at L = 3 (sigma 10000; width S = 2^{width.bit_length() - 1})"
    )
    fams = families(rows)
    fams0 = families(rows, sigma=0)
    for title, (names, builder) in SHAPES.items():
        shape = builder(names, rows)
        pushes = shape_pushes(shape, fams)
        pushes0 = shape_pushes(shape, fams0)
        net = tuple(sum(pushes[n][k] for n in shape) for k in range(3))
        say(f"## {title}")
        for n, (pos, _) in shape.items():
            say(f"  {n} at {pos}: push {pushes[n]} (electric alone {pushes0[n]})")
        say(
            f"  inward on every body: {inward(shape, pushes)} (electric alone: {inward(shape, pushes0)}); "
            f"the net push on the set per interval (the third-law gap of the fans) {net}"
        )
        result = toy(shape, fams, width)
        say(f"  the toy over 3000 intervals: {result}")
    say("## The proton line u d u with the end quark u0 kicked outward (-x): turned back or free")
    for kick in (10**12, 10**13):
        shape = line("udu", rows)
        result = toy(shape, fams, width, kicks={"u0": (-kick, 0, 0)})
        say(f"  kick {kick:.0e}: {result}")
    say(
        "  (escaped: the first tick at which a body is beyond 9 Links of the origin, the face of series I's 21^3 board)"
    )
    say()


# -- 4. the deuteron of two lines -------------------------------------------------------------


def section_4(rows: dict[str, dict[str, object]], width: int) -> None:
    say("# 4. The deuteron of two lines at adjacent Nodes: u d u at y = 0 over d u d at y = 1, along x")
    fams = families(rows)
    shape: Shape = {}
    for i, n in enumerate("udu"):
        shape[f"p_{n}{i}"] = ((i, 0, 0), quark(n, rows))
    for i, n in enumerate("dud"):
        shape[f"n_{n}{i}"] = ((i, 1, 0), quark(n, rows))
    pushes = shape_pushes(shape, fams)
    for n, (pos, _) in shape.items():
        say(f"  {n} at {pos}: push {pushes[n]}")
    proton_sum = tuple(sum(pushes[n][k] for n in shape if n.startswith("p_")) for k in range(3))
    neutron_sum = tuple(sum(pushes[n][k] for n in shape if n.startswith("n_")) for k in range(3))
    say(f"  the sum over the proton's three (its push toward the neutron line, on y): {proton_sum}")
    say(f"  the sum over the neutron's three: {neutron_sum}")
    say(
        "  series I's deuteron at one Link: 310 967 280 640 on each nucleon toward the other (one Node each)"
    )
    across = []
    for i, (a, b) in enumerate(zip("udu", "dud", strict=True)):
        push, parts = push_between(quark(a, rows), quark(b, rows), (0, -1, 0), fams)
        across.append(push[1])
        say(
            f"  the pair across at x = {i}: {a} over {b}: push on the upper {push} (glue part {parts['glue'][1]})"
        )
    say(f"  inward on every body: {inward(shape, pushes)}")
    result = toy(shape, fams, width)
    say(f"  the toy over 3000 intervals: {result}")
    say()
    say("## The collinear deuteron: the line of six u d u d u d along x (the two triples end to end)")
    six = line("ududud", rows)
    pushes = shape_pushes(six, fams)
    for n, (pos, _) in six.items():
        say(f"  {n} at {pos}: push {pushes[n]}")
    left = tuple(sum(pushes[n][k] for n in list(six)[:3]) for k in range(3))
    right = tuple(sum(pushes[n][k] for n in list(six)[3:]) for k in range(3))
    say(f"  the sum over the first triple (toward the second, on x): {left}; over the second: {right}")
    say(f"  inward on every body: {inward(six, pushes)}")
    result = toy(six, fams, width)
    say(f"  the toy over 3000 intervals: {result}")
    say()
    say(
        "## Two lines at three Links apart (beyond the reach): the residual is the electric and gravity alone"
    )
    far: Shape = {}
    for i, n in enumerate("udu"):
        far[f"p_{n}{i}"] = ((i, 0, 0), quark(n, rows))
    for i, n in enumerate("dud"):
        far[f"n_{n}{i}"] = ((i, 3, 0), quark(n, rows))
    pushes = shape_pushes(far, fams)
    proton_sum = tuple(sum(pushes[n][k] for n in far if n.startswith("p_")) for k in range(3))
    say(
        f"  the sum over the proton's three: {proton_sum}; per body: {[pushes[n] for n in far if n.startswith('p_')]}"
    )
    say()


# -- 5. the read mass ------------------------------------------------------------------------------


def section_5(rows: dict[str, dict[str, object]]) -> None:
    say(
        "# 5. The read mass of the bound set: the exact sum of the declared contents (BEAM_LAW step 4: a read moves no content)"
    )
    mu, md = int(rows["u"]["units"]), int(rows["d"]["units"])  # type: ignore[arg-type]
    proton = 2 * mu + md + 3
    neutron = mu + 2 * md + 3
    say(
        f"  the proton u u d with one glue unit each: {mu} + {mu} + {md} + 3 = {proton} units; nature 1836.15: the ratio {PROTON_UNITS / proton:.1f}"
    )
    say(f"  the neutron u d d: {mu} + {md} + {md} + 3 = {neutron} units; nature 1838.68")
    say(
        f"  the law's ratio (read mass) / (sum of the parts' units) = 1 exactly; nature's proton: {(2 * PDG_MEV['u'] + PDG_MEV['d']) / PROTON_MEV * 100:.2f} % quark rest masses, the rest the binding"
    )
    say(
        f"  n - p in the law's units: {neutron - proton} (= M_d - M_u); the register's 1839 - 1836 = 3; nature {(NEUTRON_MEV - PROTON_MEV) / ELECTRON_MEV:.3f}"
    )
    say(
        "## The dressed glue: the held glue per quark that restores the register's 1836 and 1839 (an input moved, nothing derived)"
    )
    g_total_p = PROTON_UNITS - (2 * mu + md)
    g_total_n = NEUTRON_UNITS - (mu + 2 * md)
    say(
        f"  the proton's glue total {g_total_p} over three bodies: {g_total_p // 3}, {g_total_p // 3}, {g_total_p - 2 * (g_total_p // 3)}; the neutron's {g_total_n}: {g_total_n // 3}, {g_total_n // 3}, {g_total_n - 2 * (g_total_n // 3)}"
    )
    say(
        f"  the glue's share of the proton's read mass: {g_total_p / PROTON_UNITS * 100:.2f} % (nature's binding share about {100 - (2 * PDG_MEV['u'] + PDG_MEV['d']) / PROTON_MEV * 100:.1f} %), declared"
    )
    say(
        "  under binding-v1 (the give at the contact) the read mass of a bound set can only FALL by the paid content given; no rule raises it"
    )
    say()
    say(
        "## The dressed proton line u d u (the glue 606, 607, 606 held at the value [10000, 606]; width S = 2^30)"
    )
    dressed = families(rows, sigma=(10000, 606))
    shape: Shape = {
        "u0": ((0, 0, 0), quark("u", rows, 606)),
        "d1": ((1, 0, 0), quark("d", rows, 607)),
        "u2": ((2, 0, 0), quark("u", rows, 606)),
    }
    for n, (_, held) in shape.items():
        say(f"  {n}: held {held}: (M, Q, G) = {event_charges(held, dressed)}")
    pushes = shape_pushes(shape, dressed)
    for n, (pos, _) in shape.items():
        say(f"  {n} at {pos}: push {pushes[n]}")
    mass = sum(event_charges(h, dressed)[0] for _, h in shape.values())
    say(f"  the read mass {mass} = the register's proton 1836; inward: {inward(shape, pushes)}")
    say(f"  the toy over 3000 intervals at S = 2^30: {toy(shape, dressed, 1 << 30)}")
    say()


# -- 6. the tower, the group and the regime -----------------------------------------------------------


def signed_permutations() -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    """The cube's group of 48: a permutation of the axes and a sign per axis."""
    out = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            out.append((perm, signs))
    return out


def apply(g: tuple[tuple[int, int, int], tuple[int, int, int]], v: Vector) -> Vector:
    perm, signs = g
    return (signs[0] * v[perm[0]], signs[1] * v[perm[1]], signs[2] * v[perm[2]])


def stabiliser(points: list[Vector]) -> tuple[int, set[tuple[int, ...]]]:
    """The elements of the 48 that map the set of points to itself, and the
    permutations of the points they induce (the group acting on the events)."""
    count = 0
    induced: set[tuple[int, ...]] = set()
    as_set = set(points)
    for g in signed_permutations():
        images = [apply(g, v) for v in points]
        if set(images) == as_set:
            count += 1
            induced.add(tuple(points.index(w) for w in images))
    return count, induced


def section_6(rows: dict[str, dict[str, object]]) -> None:
    say("# 6. The tower, the group on the three events, the regime")
    fams = families(rows)
    say(
        "## The column vector of the set as the exact rational sum over its members (content, charge, strong)"
    )
    for title, names in (("proton u u d", "uud"), ("neutron u d d", "udd")):
        members = [event_charges(quark(n, rows), fams) for n in names]
        content = sum(m for m, _, _ in members)
        charge = rational_sum([q for _, q, _ in members])
        strong = rational_sum([g for _, _, g in members])
        say(f"  {title}: the members {members}; the set ({content}, {charge}, {strong})")
    say(
        "  the register's rows: the proton (1837, (7344, 1), (10000, 1)), the neutron (1840, (0, 1), (10000, 1))"
    )
    say(
        "  the charge composes exactly; the content and the strong charge compose to the declared sums, not to the register's rows"
    )
    say()
    say(
        "## The stabiliser of each shape in the cube's group of 48, and the group it induces on the three events"
    )
    shapes = {
        "the line centred at the origin": [(-1, 0, 0), (0, 0, 0), (1, 0, 0)],
        "the corner about its corner": [(1, 0, 0), (0, 0, 0), (0, 1, 0)],
        "the triangle of the face-diagonal sublattice": [(1, 1, 0), (0, 1, 1), (1, 0, 1)],
    }
    for title, points in shapes.items():
        count, induced = stabiliser(points)
        say(
            f"  {title}: {count} of the 48 keep the set; the induced permutations of the three events: {len(induced)} ({sorted(induced)})"
        )
    say(
        "  S_3 on three events is carried by the 48 only on the triangle; a line or a corner carries Z_2 (the middle fixed)"
    )
    say()
    say("## The regime of the step rule: W = Q S M per body against the push per interval")
    push_ud, _ = push_between(quark("u", rows), quark("d", rows), (1, 0, 0), fams)
    for label, m_body, width in (
        ("a u body of 5 units", 5, 1 << 37),
        ("a d body of 10 units", 10, 1 << 37),
        ("the register's proton", 1837, 1 << 28),
        ("a dressed u body of 610 units", 610, 1 << 30),
    ):
        w = Q * width * m_body
        f = abs(push_ud[0])
        attempt = math.sqrt(2 * w / f)
        say(
            f"  {label}: W = 64 x 2^{width.bit_length() - 1} x {m_body} = {w:.3e}; the u-d push at one Link {f:,}; the first attempt at about sqrt(2 W / F) = {attempt:.1f} intervals; W within 2^62: {w <= WORD}"
        )
    say(
        "## The parser's static column budget (note 31 (iii)): |E n| x Q x Nodes x the largest release within 2^62 - 1"
    )
    for reader, family in (("u", "d"), ("d", "u"), ("u", "glue")):
        _, q_r, g_r = event_charges(quark(reader, rows), fams)
        n = fams[family]["charge"][0] if family != "glue" else fams[family]["strong"][0]  # type: ignore[index]
        e = q_r[0] if family != "glue" else g_r[0]
        release = int(rows[family]["units"]) if family != "glue" else 1  # type: ignore[arg-type]
        budget = abs(e * n) * Q * 1 * release
        say(
            f"  reader {reader} reading {family}: |E n| = {abs(e * n):,}, x Q x 1 Node x release {release}: {budget:,} ({'within' if budget <= WORD else 'BEYOND'})"
        )
    say()


def main() -> None:
    rows = section_1()
    section_2(rows)
    section_3(rows, 1 << 37)
    section_4(rows, 1 << 37)
    section_5(rows)
    section_6(rows)
    text = "\n".join(OUT).rstrip("\n") + "\n"
    (HERE / "quark_numbers.out").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
