"""Gravitational light bending on the GameBoard: the map of problem (1) of the seven
(the open-problems physicist, read-only, 2026-09-21; docs/designs/open_problems/light_bending/NOTE.md).

Integers only, the flight rule and the unit label transcribed from BEAM_LAW section 3
(no engine import; the Bresenham order "the axis furthest behind, the lowest axis first"
and the label `unit_label` copied line for line from nature_beam.py so that the lines and
the labels are the engine's). Nothing run, nothing registered.

(A) The stationary crowd of series K's mass (the fan of the 290 primitive directions with
    0 < |a| + |b| + |c| <= 6, one unit per direction per interval, series E's form): the
    presence P, the age moment A and the arrival flow V at every Node from the lines'
    dwells; the shell means over r = 4 .. 14 against series E's registered k_s r^2 = 41.5
    and k_a r = 36.1 at [1, 2] (A r = 72.2 at [1, 1]).
(B) One row of light on the heading (1, 0, 0) at the impact parameter b (series K's
    geometry: the lamp 26 Links before the mass, the screen 26 after): what it reads at
    every Node of its line under the presence word (P, and the flow V), under the age word
    (A, and the gradient of A across the line from the six neighbours), and the identity
    V = -(Q c^2) grad A of DERIVATIONS 5.1 checked on the lattice.
(C) One line of the fan: every fan line that crosses the row's line, its Link, its dwell,
    its age, its label's transverse part: the turn the row takes per crossing.
(D) The deflection per Link as a closed form and its sum along the path under each word,
    against nature's 4 G M / (b c^2) and Newton's 2 G M / (b c^2): the b exponent and the
    factor f; the delay likewise against Shapiro's logarithm.
(E) Series K re-read under each candidate: the registered worlds (suspension 0) and the
    pin world (the mass x 16, the pair [1, 4096]) at f = 1 and f = 2; the Sun.

Run from the repository root:

    python docs/designs/open_problems/light_bending/light_bending_map.py > docs/designs/open_problems/light_bending/light_bending_map.out
"""

from __future__ import annotations

import math
from collections import defaultdict
from fractions import Fraction

Q = 64  # the label's scale, the flight's grain
ZERO3 = (0, 0, 0)


def isqrt(n: int) -> int:
    return math.isqrt(n)


def primitive_fan(bound: int) -> list[tuple[int, int, int]]:
    """Series E's and K's fan: every primitive (a, b, c) with 0 < |a| + |b| + |c| <= bound."""
    found = []
    for a in range(-bound, bound + 1):
        for b in range(-bound, bound + 1):
            for c in range(-bound, bound + 1):
                if (a or b or c) and abs(a) + abs(b) + abs(c) <= bound:
                    if math.gcd(math.gcd(abs(a), abs(b)), abs(c)) == 1:
                        found.append((a, b, c))
    found.sort()
    return found


def unit_label(vector: tuple[int, int, int]) -> tuple[int, int, int]:
    """The engine's u_d: the integer vector nearest Q D / |D| (nature_beam.unit_label)."""
    n = sum(c * c for c in vector)
    if n == 0:
        return ZERO3
    found = []
    for a in vector:
        t = 2 * Q * abs(a)
        k = (isqrt(t * t // n) + 1) // 2
        found.append(k if a >= 0 else -k)
    return found[0], found[1], found[2]


def bresenham(vector: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    """The S_1 unit steps of one period of the digital line (nature_beam._bresenham)."""
    s1 = sum(abs(c) for c in vector)
    line: list[tuple[int, int, int]] = []
    position = [0, 0, 0]
    for j in range(s1):
        best = max(range(3), key=lambda i: (abs(vector[i]) * (j + 1) - s1 * abs(position[i]), -i))
        step = [0, 0, 0]
        step[best] = 1 if vector[best] > 0 else -1
        position[best] += step[best]
        line.append((step[0], step[1], step[2]))
    return line


class Line:
    """One direction's flight constants and digital line (BEAM_LAW section 3)."""

    def __init__(self, vector: tuple[int, int, int]):
        self.vector = vector
        self.s1 = sum(abs(c) for c in vector)
        self.t_d = isqrt(3 * sum(c * c for c in vector) * Q * Q)
        self.steps = bresenham(vector)
        self.label = unit_label(vector)

    def age_of(self, made: int) -> int:
        """The first age at which the flight's count reaches `made` Links:
        (2 tau S_1 Q + T_D) // (2 T_D) >= made."""
        rate, wall, start = 2 * self.s1 * Q, 2 * self.t_d, self.t_d
        return max(0, -(-(made * wall - start) // rate))

    def dwell(self, made: int) -> list[int]:
        return list(range(self.age_of(made), self.age_of(made + 1)))

    def nodes(self, links: int):
        x = y = z = 0
        out = [((0, 0, 0), 0)]
        for made in range(1, links + 1):
            sx, sy, sz = self.steps[(made - 1) % self.s1]
            x, y, z = x + sx, y + sy, z + sz
            out.append(((x, y, z), made))
        return out


def stationary(lines: list[Line], links: int):
    """The stationary state of one source releasing one unit per direction per interval:
    per Node the presence (rows dwelling), the age moment (sum of their ages), the arrival
    flow (sum of the labels of the rows that arrive per interval, one per line per Link),
    and the list of (line, Link) crossings."""
    presence: dict = defaultdict(int)
    age_moment: dict = defaultdict(int)
    flow: dict = defaultdict(lambda: [0, 0, 0])
    crossings: dict = defaultdict(list)
    for line in lines:
        for node, made in line.nodes(links):
            if made == 0:
                continue
            ages = line.dwell(made)
            presence[node] += len(ages)
            age_moment[node] += sum(ages)
            for i in range(3):
                flow[node][i] += line.label[i]
            crossings[node].append((line, made, ages))
    return presence, age_moment, flow, crossings


FAN = primitive_fan(6)
LINES = [Line(v) for v in FAN]
LINKS = 60
PRESENCE, AGE_MOMENT, FLOW, CROSSINGS = stationary(LINES, LINKS)
HEADING = Line((1, 0, 0))
T_H = HEADING.t_d  # 110
C_H = Fraction(Q, T_H)  # the heading's pace, 64 / 110 Links per interval
C_CONT = 1 / math.sqrt(3)
Q_RAYS = len(FAN)  # 290

print(
    f"THE FAN: {Q_RAYS} primitive directions within Manhattan 6; the heading's T_D = {T_H}, c_h = {Q}/{T_H} = {float(C_H):.4f}, 1 / sqrt 3 = {C_CONT:.4f}"
)
print()

# -- A. the shell means against series E --------------------------------------------------
print(
    "A. THE STATIONARY CROWD OF ONE SOURCE (GAMEBOARD, host arithmetic): shell means of P r^2 and A r over r = 4 .. 14"
)
print(
    "   the continuum: P = q / (4 pi r^2 c) (rows per Node, dwell 1 / c per Link), A = P r / c = 3 q / (4 pi r): P r^2 = q sqrt 3 / (4 pi), A r = 3 q / (4 pi)"
)
p_cont = Q_RAYS * math.sqrt(3) / (4 * math.pi)
a_cont = 3 * Q_RAYS / (4 * math.pi)
print(
    f"   q = {Q_RAYS}: P r^2 = {p_cont:.2f}, A r = {a_cont:.2f}; series E registered k_s r^2 = 41.5 (39.0 to 44.8) at [1, 1] and k_a r = 36.1 (33.1 to 39.2) at [1, 2], i.e. A r = 72.2"
)
shell_p, shell_a = [], []
SHELL_NODES: dict = defaultdict(list)
for x in range(-15, 16):
    for y in range(-15, 16):
        for z in range(-15, 16):
            r = round(math.sqrt(x * x + y * y + z * z))
            if 4 <= r <= 14 and abs(math.sqrt(x * x + y * y + z * z) - r) < 0.5:
                SHELL_NODES[r].append((x, y, z))
for r in range(4, 15):
    nodes = SHELL_NODES[r]
    hit = sum(1 for n in nodes if PRESENCE.get(n, 0))
    mp = sum(PRESENCE.get(n, 0) for n in nodes) / len(nodes)
    ma = sum(AGE_MOMENT.get(n, 0) for n in nodes) / len(nodes)
    shell_p.append(mp * r * r)
    shell_a.append(ma * r)
    print(
        f"   r = {r:2d}: {len(nodes):4d} Nodes, {hit:4d} on a line ({100 * hit / len(nodes):3.0f} %), P r^2 = {mp * r * r:6.2f}, A r = {ma * r:6.2f}, A / (P r) = {ma / (mp * r):.3f} (sqrt 3 = 1.732)"
    )
print(
    f"   the means over r = 4 .. 14: P r^2 = {sum(shell_p) / len(shell_p):.2f}, A r = {sum(shell_a) / len(shell_a):.2f} (the register's 41.5 and 72.2): the lines are the engine's, the shell means the register's"
)
print(
    "   the comb: beyond r = 6 most Nodes of a shell lie on no line; the shell mean is the continuum's 1 / r^2 and 1 / r, a single Node reads a line or nothing"
)
print()

# -- B. the row's line at b: what it reads under each word ---------------------------------
X_LAMP, X_SCREEN = (
    -26,
    26,
)  # relative to the mass at 0 (the lamp at x = 2, the mass at 28, the screen at 54)


def row_line(b: int):
    out = []
    for dx in range(X_LAMP, X_SCREEN + 1):
        node = (dx, b, 0)
        up, down = (dx, b + 1, 0), (dx, b - 1, 0)
        p = PRESENCE.get(node, 0)
        a = AGE_MOMENT.get(node, 0)
        v = FLOW.get(node, [0, 0, 0])
        grad_a_y = Fraction(AGE_MOMENT.get(up, 0) - AGE_MOMENT.get(down, 0), 2)
        grad_p_y = Fraction(PRESENCE.get(up, 0) - PRESENCE.get(down, 0), 2)
        out.append((dx, p, a, tuple(v), grad_a_y, grad_p_y))
    return out


def continuum(dx: int, b: int):
    r = math.sqrt(dx * dx + b * b)
    p = Q_RAYS / (4 * math.pi * r * r * C_CONT)
    a = 3 * Q_RAYS / (4 * math.pi * r)
    v = Q_RAYS * Q / (4 * math.pi * r * r)
    return r, p, a, v * dx / r, v * b / r, -a * b / (r * r), -2 * p * b / (r * r)


for b in (6, 3):
    print(
        f"B. THE ROW ON (1, 0, 0) AT b = {b}: what it reads at every Node of its line (GAMEBOARD, the crowd of one unit per direction per interval)"
    )
    print(
        "   dx | P (presence) | A (age moment) | V = (V_x, V_y) (the arrival flow, label units) | dA/dy across the line (the six neighbours) | -3 V_y / Q | continuum: P, A, V_y, dA/dy"
    )
    rows = row_line(b)
    sum_ratio, n_ratio = 0.0, 0
    for dx, p, a, v, ga, _gp in rows:
        if dx % 4 or abs(dx) > 26:
            continue
        r, pc, ac, vxc, vyc, gac, _ = continuum(dx, b)
        flow_route = -3 * v[1] / Q
        print(
            f"   {dx:3d} | {p:3d} | {a:4d} | ({v[0]:5d}, {v[1]:5d}) | {float(ga):7.2f} | {flow_route:7.2f} | {pc:5.2f}, {ac:6.2f}, {vyc:6.1f}, {gac:6.2f}"
        )
    for _dx, _p, _a, v, ga, _gp in rows:
        if ga != 0 and v[1] != 0:
            sum_ratio += float(-3 * v[1] / Q / ga)
            n_ratio += 1
    print(
        f"   the lattice's identity V = -(Q / 3) grad A (5.1 with c^2 = 1 / 3): the ratio (-3 V_y / Q) / (dA/dy) over the line's Nodes with both nonzero, mean {sum_ratio / n_ratio:.3f} (1.000 in the continuum; the ripple the digital lines')"
    )
    print()

# -- C. one line of the fan crossing the row's line ------------------------------------------
for b in (6, 3):
    print(
        f"C. ONE LINE OF THE FAN, EACH LINE THAT CROSSES THE ROW'S LINE AT b = {b} (dx from {X_LAMP} to {X_SCREEN}): the Link, the dwell, the ages, the label, its transverse part"
    )
    print(
        "   the row reads per crossing: presence = the dwell, age moment = the sum of the ages, flow = u_d once (the arrival); the turn per crossing under the age word: f (n / d) (T_D / Q^2) u_y radians toward -u_y (the design's verb 2)"
    )
    total_uy, total_a, count = 0, 0, 0
    listed = 0
    for dx in range(X_LAMP, X_SCREEN + 1):
        for line, made, ages in CROSSINGS.get((dx, b, 0), []):
            count += 1
            total_uy += line.label[1]
            total_a += sum(ages)
            if listed < 14 and abs(dx) <= 6:
                listed += 1
                print(
                    f"   dx = {dx:3d}: D = {line.vector}, Link {made:2d}, the ages {ages} (dwell {len(ages)}, the age moment {sum(ages)}), u_d = {line.label}, u_y = {line.label[1]:3d}, T_D = {line.t_d}"
                )
    print(
        f"   ... {count} crossings on the line at b = {b}; the sum of u_y over them {total_uy} (every one positive: away from the mass, the turn toward it); the sum of the age moments {total_a}"
    )
    print()

# -- D. the deflection per Link and its sum, under each word --------------------------------
print(
    "D. THE DEFLECTION PER LINK AND ITS SUM ALONG THE PATH, UNDER EACH WORD (derived; k = (n / d) x the count at the Node)"
)
print(
    "   closed forms (the continuum, one source of q rows per interval on the full fan, the path from x = -L to +L, L = 26):"
)
print("   the age word as light's index, n = 1 + f k_a, k_a = (n / d) A, A = 3 q / (4 pi r):")
print("     the turn per Link  d theta / dl = f grad_perp k_a = f k_a(b) b / (b^2 + x^2)^(3 / 2)")
print(
    "     the sum             theta = 2 f k_a(b) L / sqrt(L^2 + b^2)  ->  2 f k_a(b) as L -> infinity: the form M / b; f = 1 Newton's half, f = 2 Einstein's"
)
print(
    "     the delay per Link  f k_a(x) / c intervals per Link beyond the flight's;  the sum (f k_a(b) b / c) 2 asinh(L / b) = (f k_a(b) b / c) ln(4 L^2 / b^2) (1 + O(b^2 / L^2)): Shapiro's logarithm"
)
print("   the presence word as light's index, n = 1 + f k_s, k_s = (n / d) P, P = q / (4 pi c r^2):")
print(
    "     the turn per Link  f grad_perp k_s = 2 f k_s(b) b^2 / (b^2 + x^2)^2;  the sum -> pi f k_s(b): the form M / b^2, NOT nature's"
)
print("     the delay           (f k_s(b) b / c) x pi: the form M / b, NOT Shapiro's logarithm")
print(
    "   the flow's transverse part (the meeting's reading, the first moment): V_perp = q Q b / (4 pi r^3) = -(Q / 3) dA / dy exactly (5.1): the SAME integrand as the age word's turn; a grain constant in place of f (n / d)"
)
print()
N_PIN, D_PIN = 1, 4096
for b in (6, 3):
    rows = row_line(b)
    # the lattice sums at the pair [1, 1] per unit release; scaled below
    turn_grad = sum(
        float(ga) for _dx, _p, _a, _v, ga, _gp in rows
    )  # dA/dy summed per Link (radians per unit n/d, f = 1)
    turn_flow = sum(-3 * v[1] / Q for _dx, _p, _a, v, _ga, _gp in rows)
    turn_pres = sum(float(gp) for _dx, _p, _a, _v, _ga, gp in rows)
    delay_age = sum(a for _dx, _p, a, _v, _ga, _gp in rows) * float(
        1 / C_H
    )  # intervals per Link 1 / c_h times k_a per Link
    delay_pres = sum(p for _dx, p, _a, _v, _ga, _gp in rows) * float(1 / C_H)
    _r, _pc, a_b, _vx, _vy, _ga, _gp = continuum(0, b)
    p_b = Q_RAYS / (4 * math.pi * b * b * C_CONT)
    finite = 26 / math.sqrt(26 * 26 + b * b)
    print(
        f"   b = {b} (per unit of n / d, f = 1; the crowd of one unit per direction per interval; A(b) on the lattice {AGE_MOMENT.get((0, b, 0), 0)}, the continuum's {a_b:.1f}; P(b) {PRESENCE.get((0, b, 0), 0)}, the continuum's {p_b:.2f}):"
    )
    print(
        f"     the age word:      the lattice turn via the flow, sum 3 V_y / Q over the path {-turn_flow:8.2f} rad; the closed form 2 k_a(b) L / sqrt(L^2 + b^2) = {2 * a_b * finite:8.2f} (2 k_a(b) = {2 * a_b:.2f}); the neighbour difference -dA/dy summed {-turn_grad:8.2f} (not a field at this fan: the six neighbours lie on other lines or none)"
    )
    print(
        f"     the presence word: the neighbour difference -dP/dy summed {-turn_pres:8.2f} (the same comb); the closed form pi k_s(b) ~ {math.pi * p_b:8.2f}"
    )
    print(
        f"     the delay, the age word: sum A(x) / c_h = {delay_age:8.1f} interval per unit n / d; the closed form (k_a(b) b / c) 2 asinh(L / b) = {a_b * b / C_CONT * 2 * math.asinh(26 / b):8.1f}"
    )
    print(
        f"     the delay, the presence word: sum P(x) / c_h = {delay_pres:8.1f}; the closed form pi k_s(b) b / c x (finite) ~ {math.pi * p_b * b / C_CONT:8.1f}"
    )
print(
    "   the b exponent from 6 to 3, the one number that decides light's word in the continuum: the age word's deflection doubles (1 / b), the presence word's quadruples (1 / b^2)"
)
r6, r3 = row_line(6), row_line(3)
flow_ratio = sum(v[1] for *_, v, _ga, _gp in r3) / sum(v[1] for *_, v, _ga, _gp in r6)
print(
    f"     on the lattice at series K's fan the flow sums give {flow_ratio:.2f} from b = 6 to 3 (the register under the meeting: -2.30 at b = 3 against -1.79 at b = 6, DETECTOR; the offline flight -2.6 against -3.0): the beam lies in the mass's plane, section E"
)
print()

# -- E. series K re-read under each candidate --------------------------------------------
print("E. SERIES K RE-READ UNDER EACH CANDIDATE (the map; no run)")
print(
    "   the registered worlds declare suspension 0: k = 0 under every word, the register's 0.000 pixel and 0.00 interval stand byte for byte under every candidate"
)
print(
    "   the pin world (optical-v1's must-fix 7): the mass x 16 (16 units per direction per interval), the pair [1, 4096]; the lamp at (-26, b), the screen 26 Links past the mass; the turn read from the flow at every interval the row dwells (the design's verb 2), the delay from A at every such interval (verb 1)"
)
print(
    "   world | M | b | k_a(b) lattice (the design's shell-mean 0.0445, 0.0887, 0.0887) | the deflection, rad: f = 1 | f = 2 | the centroid's shift, pixels: f = 1 | f = 2 (DETECTOR if run; the bracket 0.5) | the delay, intervals: f = 1 | f = 2 (the mean age 89.40 registered; the bracket 1) | the lamp's clock rate under the age word, GAMEBOARD"
)


def path_sums(b: int):
    """The row on the heading from dx = -26 to 26 at y = b: the exact dwell per Node from
    the heading's accumulator (1 or 2 intervals), the turn per unit of f n / d as the sum
    over its intervals of (T_D / Q^2) V_y, the delay per unit of f n / d as the sum of A."""
    turn = Fraction(0)
    delay = 0
    for made, dx in enumerate(range(X_LAMP, X_SCREEN + 1)):
        dwell = len(HEADING.dwell(made + 1)) if made + 1 <= LINKS else 2
        v = FLOW.get((dx, b, 0), [0, 0, 0])
        turn += dwell * Fraction(T_H, Q * Q) * v[1]
        delay += dwell * AGE_MOMENT.get((dx, b, 0), 0)
    return turn, delay


for pair_d in (4096, 16384):
    print(f"   the pair [1, {pair_d}]:")
    for name, scale, b in (("mass", 16, 6), ("heavy", 32, 6), ("near", 16, 3)):
        turn_unit, delay_unit = path_sums(b)
        k_b = scale * AGE_MOMENT.get((0, b, 0), 0) * N_PIN / pair_d
        turn = scale * float(turn_unit) / pair_d
        delay = scale * delay_unit / pair_d
        a_lamp = AGE_MOMENT.get((X_LAMP, b, 0), 0) * scale
        rate_lamp = 1 / (1 + a_lamp * N_PIN / pair_d)
        print(
            f"   {name:5s} | 2^{int(math.log2(4096 * scale))} | {b} | {k_b:.4f} | {turn:.4f} | {2 * turn:.4f} | -{turn * 26:.2f} | -{2 * turn * 26:.2f} | {delay:.2f} | {2 * delay:.2f} | {rate_lamp:.4f}"
        )
print(
    "   at [1, 4096] the turn is 0.3 to 0.8 radian, whole fan steps of 2.4 degrees by the dozen, outside the small-angle form; the pair [1, 16384] keeps every shift above the 0.5-pixel bracket and every delay above the 1-interval bracket at angles below 0.2 radian: the pin this note recommends"
)
print(
    "   under the clock's word alone (record 394, the flight blind): 0.000 pixel and 0.00 interval in every world, the register's numbers"
)
print(
    "   under the age word for light alone (the clock keeping the presence): the same light numbers; the clock rows of NATURE 12 FAIL as registered"
)
print()
print(
    "   THE BEAM'S PLANE: the in-plane lines of the fan (c = 0) never leave z = 0 and each crosses the row's line once whatever b; a line with c != 0 visits z = 0 only in its first Links"
)
in_plane = sum(1 for v in FAN if v[2] == 0)
print(f"   {in_plane} of {Q_RAYS} directions lie in the plane z = 0")
print(
    "   the row's line moved off the mass's plane, the same 53 Nodes of path: the crossings, the sum of the transverse label |u_perp| (the turn's integrand) and of A (the delay's)"
)
for b, z in ((6, 0), (6, 1), (6, 2), (3, 0), (3, 1), (4, 4), (2, 5)):
    crossings = 0
    u_perp = 0.0
    a_sum = 0
    for dx in range(X_LAMP, X_SCREEN + 1):
        node = (dx, b, z)
        for line, _made, ages in CROSSINGS.get(node, []):
            crossings += 1
            u_perp += math.sqrt(line.label[1] ** 2 + line.label[2] ** 2)
            a_sum += sum(ages)
    r_perp = math.sqrt(b * b + z * z)
    print(
        f"   (y, z) = ({b}, {z}), the distance {r_perp:.2f}: {crossings:3d} crossings, sum |u_perp| = {u_perp:7.1f}, sum A = {a_sum:5d}; the isotropic continuum's sum |u_perp| = {2 * 3 * Q_RAYS / (4 * math.pi * r_perp) * 26 / math.sqrt(26 * 26 + r_perp * r_perp) * Q / 3:7.1f}"
    )
print(
    "   in the mass's plane the lattice reads 3 to 4 times the isotropic sum and nearly the same at b = 3 as at 6; one Node off the plane it reads a tenth of it: at this fan (P = 6) the row's reading is the comb of the in-plane lines, not the 1 / b field; the field needs P >> r (the dense fan of 3.2's limit)"
)
print()
GM_SUN, R_SUN, C_SI = 1.32712e20, 6.957e8, 299_792_458.0
k_limb = GM_SUN / (R_SUN * C_SI**2)
arcsec = 180 / math.pi * 3600
print(
    f"   THE SUN: k = G M / (R c^2) = {k_limb:.3e} at the limb; the bending 2 f k: f = 1 {2 * k_limb * arcsec:.4f} arcsec (Newton 1801, Soldner), f = 2 {4 * k_limb * arcsec:.4f} arcsec (Einstein 1915; Dyson, Eddington and Davidson 1920 1.98 +- 0.16 and 1.61 +- 0.40; VLBI gamma = 0.99992 +- 0.00012, Lambert and Le Poncin-Lafitte 2011, to verify against the source)"
)
print(
    "   PPN gamma = f - 1: the six verbs with one word give f = 1, gamma = 0; nature gamma = 1 to 1.2 x 10^-4: f = 2 is an input"
)
