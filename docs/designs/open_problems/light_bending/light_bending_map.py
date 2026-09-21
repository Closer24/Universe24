"""Open problem (i), the bending of light under the age word: the numbers of
the read-only note (Far, the G2 session, 2026-09-21; the Boss's order of
14:42Z on the model owner's word "give it to Far"). A host derivation from
the engine's own flight lines (`direction_flight`, the one import), the
method of the physicist's clock_age_map.py; no run, no fit, no build.

(A) Nature's numbers at the Sun's limb: k = G M / (r c^2), Newton's 2 k,
    Einstein's 4 k.
(B) Series K's mass on the lattice (`examples/events/lensing/`: the fan of
    290 primitive directions with |a| + |b| + |c| <= 6, one row per
    direction per interval at M = 2^12, two at 2^13; the box 57 x 41 x 41,
    the mass at (28, 20, 20), the beam's heading along +x at y = 20 + b):
    the stationary presence P and age moment A at every Node from the
    lines (each row's dwell ages at each Link of its digital line), read on
    the beam's line and its two neighbours in y, at the impact distances
    b = 6 and 3.
(C) The deflection per Link and summed along the path, for a row whose
    direction turns by the transverse gradient of f x k_a (Fermat's law on
    the index n = 1 + f k_a, the rule of optical-v1 verb 2; the pace by
    verb 1): d theta = f (n_s / d_s) (A(y + 1) - A(y - 1)) / 2 per Link
    along x, summed over the path, against the continuum's 2 f k_a(b) with
    k_a(b) = (n_s / d_s) A(b), at f = 2 (Einstein's factor) and f = 1
    (Newton's), per unit of the suspension pair and at the pin pair
    [1, 4096] of the physicist's design (docs/designs/gr_rows/DESIGN.md
    section 4, the mass sixteen times the registered).
(D) The three candidates of the owner's hypothesis ("maybe it is attached
    only to light and not to the clock"): the age word for the rows only,
    for the clock only (the law as decided, record 394), for both; what
    each reads at the beam's Node and at a clock there.

Run from the repository root:

    PYTHONPATH=src python docs/designs/open_problems/light_bending/light_bending_map.py > docs/designs/open_problems/light_bending/light_bending_map.out
"""

from __future__ import annotations

import math
from collections import defaultdict

from event_universe.events.nature_beam import Q, direction_flight

HEADINGS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
SHAPE = (57, 41, 41)
CENTRE = (28, 20, 20)
LAMP_X, SCREEN_X = 2, 54
FAN_MANHATTAN = 6
PIN_PAIR = (1, 4096)
PIN_SCALE = 16  # the design's pin world: the mass sixteen times the registered


def fan(bound: int) -> list[tuple[int, int, int]]:
    """Series E's fan: every primitive direction with 0 < |a| + |b| + |c| <= bound."""
    found = []
    for a in range(-bound, bound + 1):
        for b in range(-bound, bound + 1):
            for c in range(-bound, bound + 1):
                if (a or b or c) and abs(a) + abs(b) + abs(c) <= bound:
                    if math.gcd(math.gcd(abs(a), abs(b)), abs(c)) == 1:
                        found.append((a, b, c))
    found.sort()
    return found


class Lines:
    """The engine's digital lines and flight constants of a direction table."""

    def __init__(self, table: list[tuple[int, int, int]]):
        self.table = table
        self.flight = direction_flight(tuple(table))
        self.index = {d: i for i, d in enumerate(table)}

    def age_of(self, d: tuple[int, int, int], made: int) -> int:
        """The first age at which the accumulator's count reaches `made` Links:
        (2 tau S_1 Q + T_D) // (2 T_D) >= made."""
        i = self.index[d]
        rate = 2 * int(self.flight.manhattan[i]) * Q
        wall = 2 * int(self.flight.resolution[i])
        start = int(self.flight.resolution[i])
        return max(0, -(-(made * wall - start) // rate))

    def dwell(self, d: tuple[int, int, int], made: int) -> list[int]:
        return list(range(self.age_of(d, made), self.age_of(d, made + 1)))

    def nodes(self, d: tuple[int, int, int], links: int):
        i = self.index[d]
        s1 = int(self.flight.manhattan[i])
        line = self.flight.lines[i, :s1]
        x = y = z = 0
        out = [((0, 0, 0), 0)]
        for made in range(1, links + 1):
            step = line[(made - 1) % s1]
            x += int(step[0])
            y += int(step[1])
            z += int(step[2])
            out.append(((x, y, z), made))
        return out


def field(lines: Lines, origin, directions, rows_per_direction: int, links: int):
    """The stationary presence and age moment per Node of one source releasing
    `rows_per_direction` rows per direction per interval: at each Link of
    each line the rows dwelling there (one per interval of the dwell) at
    their ages."""
    presence: dict = defaultdict(int)
    age_moment: dict = defaultdict(int)
    for d in directions:
        for (dx, dy, dz), made in lines.nodes(d, links):
            if made == 0:
                continue
            node = (origin[0] + dx, origin[1] + dy, origin[2] + dz)
            ages = lines.dwell(d, made)
            presence[node] += rows_per_direction * len(ages)
            age_moment[node] += rows_per_direction * sum(ages)
    return presence, age_moment


def inside(node) -> bool:
    return all(0 <= node[i] < SHAPE[i] for i in range(3))


print("A. NATURE AT THE SUN'S LIMB")
G, M_SUN, R_SUN, C_LIGHT = 6.674e-11, 1.989e30, 6.957e8, 2.998e8
k_limb = G * M_SUN / (R_SUN * C_LIGHT**2)
arcsec = 180 / math.pi * 3600
print(
    f"   k = G M / (r c^2) = {k_limb:.3e}; Newton's 2 k = {2 * k_limb * arcsec:.3f} arcsec; Einstein's 4 k = {4 * k_limb * arcsec:.3f} arcsec (Dyson, Eddington and Davidson 1920: 1.98 +- 0.16, 1.61 +- 0.40; VLBI gamma = 0.99992 +- 0.00012)"
)
print(
    "   the factor 2 over Newton: the time part (the clock's potential, g_00) and the space part (g_rr) of the weak isotropic metric, one each; Cassini fixes it to 2 x 10^-5"
)
print()

print(
    "B. SERIES K'S MASS ON THE LATTICE: THE PRESENCE P AND THE AGE MOMENT A ON THE BEAM'S LINE (host, from the flight lines)"
)
directions = fan(FAN_MANHATTAN)
table = HEADINGS + [d for d in directions if d not in HEADINGS]
lines = Lines(table)
LINKS = 90  # beyond the box's longest flight from the centre
fields = {}
for name, rows, b in (("mass", 1, 6), ("heavy", 2, 6), ("near", 1, 3)):
    P, A = field(lines, CENTRE, directions, rows, LINKS)
    fields[name] = (P, A, b)
    y0 = CENTRE[1] + b
    print(
        f"   {name}: M = {'2^13' if rows == 2 else '2^12'} ({rows} row per direction per interval), b = {b}; the beam's line y = {y0}, z = {CENTRE[2]}"
    )
    header = "     x:  " + " ".join(f"{x:4d}" for x in range(LAMP_X, SCREEN_X + 1, 4))
    print(header)
    for label, dy in (("A(y+1)", 1), ("A(y)  ", 0), ("A(y-1)", -1)):
        row = [A.get((x, y0 + dy, CENTRE[2]), 0) for x in range(LAMP_X, SCREEN_X + 1, 4)]
        print(f"     {label} " + " ".join(f"{v:4d}" for v in row))
    row = [P.get((x, y0, CENTRE[2]), 0) for x in range(LAMP_X, SCREEN_X + 1, 4)]
    print("     P(y)   " + " ".join(f"{v:4d}" for v in row))
    at_b = (CENTRE[0], y0, CENTRE[2])
    print(
        f"     at the mass's plane x = 28: P = {P.get(at_b, 0)}, A = {A.get(at_b, 0)} (the README's shell-mean estimate: P {1.10 * rows * (36 / b**2):.2f}, A {11.4 * rows * (6 / b):.1f})"
    )
    # the mean over the beam's nine pixels (y0 - 1 .. y0 + 1, z 19 .. 21) at the plane
    pixels = [(CENTRE[0], y0 + dy, CENTRE[2] + dz) for dy in (-1, 0, 1) for dz in (-1, 0, 1)]
    print(
        f"     the beam's nine Nodes at the plane, mean P {sum(P.get(p, 0) for p in pixels) / 9:.2f}, mean A {sum(A.get(p, 0) for p in pixels) / 9:.1f}"
    )
print(
    "   The fan's grain: a Node on one of the 290 lines reads that line's rows (about 2 per Link of dwell at the ages of the flight); a Node off every line reads 0; the shell mean is the continuum's M / r^2 and M / r (series E)."
)
print()

print(
    "C. THE DEFLECTION PER LINK AND SUMMED ALONG THE PATH (Fermat on n = 1 + f k_a: d theta = f (n_s / d_s) x (A(y+1) - A(y-1)) / 2 per Link in x)"
)
print(
    "   per unit of the pair (n_s / d_s = 1), the lattice's sum over x = 2 .. 54 of the transverse difference of A across the beam's line, against the continuum's 2 f A(b) with A(b) the shell mean at b:"
)
for name, (_P, A, b) in fields.items():
    y0 = CENTRE[1] + b
    grad_sum = 0
    per_link = []
    for x in range(LAMP_X, SCREEN_X + 1):
        g = (A.get((x, y0 + 1, CENTRE[2]), 0) - A.get((x, y0 - 1, CENTRE[2]), 0)) / 2
        per_link.append(g)
        grad_sum += g
    # the shell-mean continuum: A(r) = dwell q / (4 pi c r) with the registered constant k_a r = 36.1 at [1, 2] for q = 290 (one row per direction)
    rows = 2 if name == "heavy" else 1
    a_cont = 2 * 36.1 * rows / b  # the age moment per Node at [1, 1] (the [1, 2] value doubled)
    for f in (2, 1):
        lattice = f * grad_sum
        continuum = 2 * f * a_cont
        print(
            f"   {name} (b = {b}), f = {f}: the lattice's summed gradient {lattice:+.1f} per unit pair; the continuum 2 f A(b) = {continuum:.1f} (A(b) = {a_cont:.1f}); at the pin pair [1, 4096] and the mass x 16: {lattice * PIN_SCALE / PIN_PAIR[1]:+.4f} rad (lattice) against {continuum * PIN_SCALE / PIN_PAIR[1]:.4f} rad (continuum; the design's {0.178 if b == 6 and rows == 1 else 0.355:.3f})"
        )
    nonzero = [(LAMP_X + i, g) for i, g in enumerate(per_link) if g]
    print(
        f"      the Links where the transverse difference is not 0: {len(nonzero)} of {len(per_link)}; the largest {max(per_link):+.0f} at x = {LAMP_X + per_link.index(max(per_link))}, the smallest {min(per_link):+.0f} at x = {LAMP_X + per_link.index(min(per_link))} (the sign: A grows toward the mass, y decreasing, so the difference is negative and the turn is toward the mass)"
    )
print(
    "   The lattice's line sum is the grain's: the beam's line crosses the fan's lines at a few Nodes, where the difference is tens per Link, and reads 0 between them; the continuum's 2 f A(b) is what the shell means give. On the fan the turn is whole steps of THETA_G (2.4 degrees at the smallest), the design's dither over records (gr_rows/DESIGN.md section 4)."
)
print()

print(
    "D. THE THREE CANDIDATES OF THE OWNER'S HYPOTHESIS, WHAT EACH READS AT b = 6 (M = 2^12), THE CLOCK'S k AND THE ROW'S TURN"
)
P, A, b = fields["mass"]
at_b = (CENTRE[0], CENTRE[1] + b, CENTRE[2])
for pair_name, pair in (
    ("per unit pair", (1, 1)),
    ("the design's pin pair [1, 4096], the mass x 16", PIN_PAIR),
):
    scale = PIN_SCALE if pair[1] == 4096 else 1
    k_s = P.get(at_b, 0) * scale * pair[0] / pair[1]
    k_a = A.get(at_b, 0) * scale * pair[0] / pair[1]
    a_cont = 2 * 36.1 / b * scale * pair[0] / pair[1]
    print(
        f"   {pair_name}: at the beam's Node on the mass's plane the presence word gives k_s = {k_s:.4f}, the age word k_a = {k_a:.4f} (the shell mean's k_a(b) = {a_cont:.4f})"
    )
    print(
        f"      (A) the age word for the rows only (optical-v1's verbs on the rows, the clock counting the presence): the row turns by 2 f k_a(b) = {4 * a_cont:.4f} rad at f = 2 toward the mass and is delayed as the potential's logarithm; a clock at the same Node runs at 1 / (1 + k_s) = {1 / (1 + k_s):.4f}, the M / r^2 form that GPS and Galileo refute at two heights: two different fields from one stream for two readers, no one metric"
    )
    print(
        f"      (B) the age word for the clock only (the law as decided, record 394; the flight blind to the crowd): the row turns 0 (series K's 0.000 stands) and is not delayed; the clock runs at 1 / (1 + k_a) = {1 / (1 + a_cont):.4f}, the potential's form; the bending of light NOT reached, the disagreement with nature (the physicist's entry 2) stands"
    )
    print(
        f"      (C) the age word for both (clock-age-v1 and optical-v1 with the declared f): one index n = 1 + f k_a for the rows and the clock's 1 + k_a: the row turns by 2 f k_a(b) = {4 * a_cont:.4f} rad at f = 2 ({2 * a_cont:.4f} at f = 1, Newton's), is delayed by (f k_a(b) b / c) ln(4 r1 r2 / b^2), and the clock beside it runs at 1 / (1 + k_a): the time part of the metric is the clock's word, the space part is the second unit of f; the 2 is declared, not derived from the verbs"
    )
print()
print("E. WHAT IS DERIVED AND WHAT IS CONDITIONAL, for the owner's question")
print(
    "   derived on the GameBoard: the presence falls as M / r^2 and the age moment as M / r from the same rows (series E: k_s r^2 = 41.5, k_a r = 36.1; the fan's dilution as the shell), the push as minus the gradient of A (5.1), the clock at 1 / (1 + k_a) (5.2, first order), the bending's FORM M / b and its sign from any turn that reads a transverse gradient (the meeting's grain, optical-v1's index), the delay's logarithm from a pace that reads A along the path (optical-v1 verb 1)"
)
print(
    "   conditional: the factor 2 of Einstein over Newton (declared as f in optical-v1; a derivation would need the space part from the verbs, a row's Link that shortens beside a mass, which no verb of the six gives: the flight table is one speed and the Links are the lattice's), the identification k_a = G M / (r c^2) (the suspension pair sets the scale, nature fixes it by one clock), the field equation beyond the static case (A obeys the retarded scalar wave equation of a stream, 5.1; Einstein's nonlinear equation is not this, 5.5)"
)
