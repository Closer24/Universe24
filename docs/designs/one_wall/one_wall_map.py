"""One wall for every accumulator and the push on a row with its energy as the weight
(`one-wall-v1`, issue #605): the map of the design note beside it
(docs/designs/one_wall/NOTE.md; the physicist, read-only, 2026-09-21).

Integers only: the flight rule, the unit label and the Bresenham order are transcribed from
BEAM_LAW section 3 as the light-bending map transcribed them (docs/designs/open_problems/
light_bending/light_bending_map.py, whose stationary crowd this map rebuilds line for line);
the push is the bilinear form of BEAM_LAW section 3 step 4 with the weight named by the
rule; no engine import; nothing run on the engine, nothing registered.

(A) The one constant: the clock's k_a = (n / d) A against the push's G M / (r c^2) on the
    same stationary crowd (series K's mass: the fan of the 290 primitive directions within
    Manhattan 6, one unit per direction per interval), from the lattice's own lines: the
    ratio is n S / d, so ONE G for the clock and for Newton is the world's pair [n, d] =
    [1, S] (the register's series E `scalar` world at [1, 1], S = 1).
(B) One row of light on the heading (1, 0, 0) at the impact parameter b (series K's
    geometry: the lamp 26 Links before the mass, the screen 26 after, the beam in the
    mass's plane), flown offline under the rule interval by interval: the wall stretched
    by the age moment at its Node (verb 1), the push of the flow on its energy into a
    vector accumulator and the direction moved to the fan's nearest (verbs 2 and 3), the
    landing pixel and the arrival interval against the control.
(C) The two readings of one deflection: the row's bend (a pixel detector's centroid, the
    push) and the front's tilt (a phase reading: the wall's delay differing between
    neighbouring rows), the closed forms in the continuum, and whether they add.
(D) The pin worlds: the width S and the pair [1, S] that keep the angles small at series
    K's crowd, with the numbers a run would meet; the Sun; the host price as a count.

Run from the repository root:

    python docs/designs/one_wall/one_wall_map.py > docs/designs/one_wall/one_wall_map.out
"""

from __future__ import annotations

import math
from collections import defaultdict

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
    """One direction's flight constants and digital line (BEAM_LAW section 3): the rate
    2 S_1 Q, the wall 2 T_D, the start T_D; the energy of one unit of content on the
    direction e_D = isqrt(3 u_D . u_D), the massless case of the massive rows' E'_D
    (DERIVATIONS_BEAM 23: E'_D = isqrt(E'_0^2 + 3 p . p) with E'_0 = 0, p = u_D)."""

    def __init__(self, vector: tuple[int, int, int]):
        self.vector = vector
        self.s1 = sum(abs(c) for c in vector)
        self.t_d = isqrt(3 * sum(c * c for c in vector) * Q * Q)
        self.steps = bresenham(vector)
        self.label = unit_label(vector)
        self.energy = isqrt(3 * sum(c * c for c in self.label))

    def age_of(self, made: int) -> int:
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
    per Node the presence, the age moment (the sum of the dwelling rows' ages) and the
    arrival flow (one arrival per line per interval, its label u_D)."""
    presence: dict = defaultdict(int)
    age_moment: dict = defaultdict(int)
    flow: dict = defaultdict(lambda: [0, 0, 0])
    for line in lines:
        for node, made in line.nodes(links):
            if made == 0:
                continue
            ages = line.dwell(made)
            presence[node] += len(ages)
            age_moment[node] += sum(ages)
            for i in range(3):
                flow[node][i] += line.label[i]
    return presence, age_moment, flow


FAN = primitive_fan(6)
LINES = {v: Line(v) for v in FAN}
LINKS = 60
PRESENCE, AGE_MOMENT, FLOW = stationary(list(LINES.values()), LINKS)
HEADING = LINES[(1, 0, 0)]
Q_RAYS = len(FAN)
C_CONT = 1 / math.sqrt(3)
X_LAMP, X_SCREEN = -26, 26

print(
    f"THE FAN: {Q_RAYS} primitive directions within Manhattan 6; the heading's T_D = {HEADING.t_d}, "
    f"u = {HEADING.label}, e_D = isqrt(3 u . u) = {HEADING.energy}; c_h = {Q}/{HEADING.t_d} = {Q / HEADING.t_d:.4f}, "
    f"1 / sqrt 3 = {C_CONT:.4f}"
)
print()

# -- A. the one constant ------------------------------------------------------------------
print(
    "A. THE ONE CONSTANT: the clock's k_a against the push's G M / (r c^2) on the same crowd (GAMEBOARD, host arithmetic)"
)
print(
    "   the push on a body of content M: p += -M V per interval (BEAM_LAW 3 step 4, gravity's term), the drive one Link per"
)
print(
    "   (Q S M + |p|) / |p| self-creations, so the acceleration is |V| / (Q S) Links per interval^2, and with the continuum's"
)
print(
    "   flow |V| = q Q / (4 pi r^2) the push's 'G M' is q / (4 pi S); with c^2 = 1 / 3, G M / (r c^2) = 3 q / (4 pi S r)."
)
print(
    "   the clock's count k_a = (n / d) A with A = 3 q / (4 pi r) (DERIVATIONS 5.1: dwell = 1 / c): k_a / (G M / (r c^2)) = n S / d."
)
shell_a, shell_v = [], []
SHELL_NODES: dict = defaultdict(list)
for x in range(-15, 16):
    for y in range(-15, 16):
        for z in range(-15, 16):
            rr = math.sqrt(x * x + y * y + z * z)
            r = round(rr)
            if 4 <= r <= 14 and abs(rr - r) < 0.5:
                SHELL_NODES[r].append((x, y, z))
print(
    "   r | A r (the lattice's shell mean) | 3 q / (4 pi) | |V| r^2 / Q (the lattice) | q / (4 pi) | the ratio A r / (3 |V| r^2 / Q) (n S / d at [1, 1], S = 1)"
)
for r in range(4, 15):
    nodes = SHELL_NODES[r]
    ma = sum(AGE_MOMENT.get(n, 0) for n in nodes) / len(nodes)
    mv = sum(math.sqrt(sum(c * c for c in FLOW.get(n, [0, 0, 0]))) for n in nodes) / len(nodes)
    shell_a.append(ma * r)
    shell_v.append(mv * r * r / Q)
    print(
        f"   {r:2d} | {ma * r:6.2f} | {3 * Q_RAYS / (4 * math.pi):6.2f} | {mv * r * r / Q:6.2f} | {Q_RAYS / (4 * math.pi):6.2f} | {ma * r / (3 * mv * r * r / Q):.3f}"
    )
mean_a = sum(shell_a) / len(shell_a)
mean_v = sum(shell_v) / len(shell_v)
print(
    f"   the means over r = 4 .. 14: A r = {mean_a:.2f}, |V| r^2 / Q = {mean_v:.2f}, the ratio {mean_a / (3 * mean_v):.3f} (1.000 in the continuum)"
)
print(
    "   so the clock's k_a and Newton's G M / (r c^2) are ONE number exactly when n S = d: the pair [1, S]; series E's `scalar`"
)
print(
    "   world declares [1, 1] at S = 1 (its `age` world [1, 2]: the clock's G half of Newton's). THE LATTICE CONSTANT: the age"
)
print(
    "   moment is isotropic (a line's dwell per Euclidean Link is T_D / (|D| Q) = 1 / c on every direction, DERIVATIONS 5.1's F05)"
)
print(
    "   while the flow a Node reads counts one arrival per line per interval at S_1 / |D| Nodes per Euclidean Link, the fan's L1"
)
print(
    f"   factor ({mean_v / (Q_RAYS / (4 * math.pi)):.2f} here): at [1, S] the clock's constant is {mean_a / (3 * mean_v):.2f} of the push's on the lattice, 1.00 in the continuum."
)
print()


# -- B. the row flown offline under the rule ------------------------------------------------
def nearest_direction(p: tuple[int, int, int], current: tuple[int, int, int]) -> tuple[int, int, int]:
    """The fan direction nearest the vector p by integer comparisons of (p . D)^2 |D'|^2
    against (p . D')^2 |D|^2 among the directions with p . D > 0; the current one on a tie."""
    best = current
    for d in FAN:
        dot = sum(a * b for a, b in zip(p, d, strict=True))
        if dot <= 0:
            continue
        bd = sum(a * b for a, b in zip(p, best, strict=True))
        lhs = dot * dot * sum(c * c for c in best)
        rhs = bd * bd * sum(c * c for c in d)
        if lhs > rhs:
            best = d
    return best


def fly(b: int, n: int, d: int, width: int, wall_on: bool, push_on: bool, content: int = 1):
    """One unit of light released at (-26, b, 0) on (1, 0, 0), flown interval by interval
    until x reaches 26 or 400 intervals pass: the position accumulator with the wall
    2 T_D (d + n A) against the rate 2 S_1 Q d (verb 1; d + 0 without the key), the push
    w += -content e_D V per interval (verb 2: the crowd's flow on the row's energy, gravity's
    sign), the row's whole momentum P = Q S content u_D + w and the direction moved to the
    fan's nearest (verb 3) with w keeping the remainder Q S content (u_D - u_D'). Returns
    (the landing y, the landing z, the intervals, the turns made, the energy read)."""
    line = HEADING
    x, y, z = X_LAMP, b, 0
    acc = line.t_d * d  # the start T_D at the pair's scale
    made_on_line = 0
    w = [0, 0, 0]
    turns = 0
    for tick in range(1, 401):
        node = (x, y, z)
        a_here = AGE_MOMENT.get(node, 0) if wall_on else 0
        v_here = FLOW.get(node, [0, 0, 0]) if push_on else [0, 0, 0]
        rate = 2 * line.s1 * Q * d
        wall = 2 * line.t_d * (d + n * a_here)
        acc += rate
        if acc >= wall:
            acc -= wall
            sx, sy, sz = line.steps[made_on_line % line.s1]
            x, y, z = x + sx, y + sy, z + sz
            made_on_line += 1
            if x >= X_SCREEN:
                return y, z, tick, turns
        if push_on:
            for i in range(3):
                w[i] -= content * line.energy * v_here[i]
            p = tuple(Q * width * content * line.label[i] + w[i] for i in range(3))
            new = nearest_direction(p, line.vector)
            if new != line.vector:
                new_line = LINES[new]
                for i in range(3):
                    w[i] += Q * width * content * (line.label[i] - new_line.label[i])
                # the accumulator carries over at the new direction's scale of the wall
                acc = acc * new_line.t_d // line.t_d
                line = new_line
                made_on_line = 0
                turns += 1
    return y, z, 400, turns


def continuum_numbers(b: int, n: int, d: int, width: int):
    """The closed forms: the push's bend 2 G M / (b c^2) with G M = q / (4 pi S), the wall's
    tilt 2 k_a(b) with k_a = (n / d) 3 q / (4 pi b), the wall's delay (k_a(b) b / c) 2 asinh(L / b)."""
    gm_c2 = 3 * Q_RAYS / (4 * math.pi * width)  # G M / c^2 in Links
    bend = 2 * gm_c2 / b
    k_a = (n / d) * 3 * Q_RAYS / (4 * math.pi * b)
    tilt = 2 * k_a * 26 / math.sqrt(26 * 26 + b * b)
    delay = k_a * b / C_CONT * 2 * math.asinh(26 / b)
    return bend, tilt, delay


print(
    "B. ONE ROW OF LIGHT FLOWN OFFLINE UNDER THE RULE at series K's geometry (the lamp at x = -26, the screen at x = 26,"
)
print(
    "   the crowd of one unit per direction per interval; content 1: the angle is content-blind, P and w both scale with it)"
)
print(
    "   S | pair | b | control: y, intervals | wall only: y, intervals (the delay) | push only: y, intervals, turns | both: y, intervals, turns |"
)
print(
    "   the continuum: the push's bend 2 G M / (b c^2) in Links at the screen, the wall's tilt 2 k_a(b) L / sqrt(L^2 + b^2) in Links, the wall's delay in intervals"
)
CASES = [(1, 1, 1), (64, 1, 64), (256, 1, 256), (1024, 1, 1024), (256, 1, 4096), (256, 1, 16384)]
RESULTS: dict = {}
for width, n, d in CASES:
    for b in (6, 3):
        control = fly(b, n, d, width, False, False)
        wall = fly(b, n, d, width, True, False)
        push = fly(b, n, d, width, False, True)
        both = fly(b, n, d, width, True, True)
        bend, tilt, delay = continuum_numbers(b, n, d, width)
        RESULTS[(width, n, d, b)] = (control, wall, push, both)
        print(
            f"   {width:4d} | [{n}, {d}] | {b} | {control[0]:3d}, {control[2]:3d} | {wall[0]:3d}, {wall[2]:3d} (+{wall[2] - control[2]}) | "
            f"{push[0]:3d}, {push[2]:3d}, {push[3]:2d} | {both[0]:3d}, {both[2]:3d}, {both[3]:2d} | "
            f"bend {bend * 26:7.2f}, tilt {tilt * 26:7.2f}, delay {delay:7.2f}"
        )
print(
    "   (a landing y below b is toward the mass; 400 intervals without reaching the screen is a capture)"
)
print()

# -- C. the two readings of one deflection ------------------------------------------------
print("C. THE TWO READINGS OF ONE DEFLECTION (derived; the continuum, then the lattice)")
print(
    "   the row's bend (DETECTOR: a pixel screen's centroid): the push's turn per interval e_D |V_perp| / (Q^2 S) radians"
)
print(
    "   (w gains e_D V, P's base is Q S u with |u| = Q), summed over the intervals the row dwells at each Node of its path;"
)
print(
    "   in the continuum d theta / dt = |V_perp| / (Q S c) (e_D / Q = sqrt 3 = 1 / c), the sum 2 G M / (b c^2) with G M = q / (4 pi S)."
)
print(
    "   the front's tilt (DETECTOR: a phase reading across the screen, the record's phase per pixel): c times the difference"
)
print(
    "   of the wall's delay between the rows at b and b + 1, which in the continuum is 2 k_a(b) L / sqrt(L^2 + b^2): the same"
)
print(
    "   form; at n S = d the same number as the bend. The rows then ride their own wavefront; the two are one deflection,"
)
print(
    "   Newton's 2 G M / (b c^2) (Soldner 1801; Einstein 1911), and they never add: a row bent by the push arrives at its"
)
print(
    "   pixel with the delay of its own path, and the phase gradient across the screen is the delay's gradient alone"
)
print("   (the bent path's extra length is second order in the angle).")
for width, n, d in ((256, 1, 256), (1024, 1, 1024)):
    print(
        f"   S = {width}, the pair [{n}, {d}] (n S = d): per unit of the crowd, at b = 6 and 3, on the lattice's lines"
    )
    for b in (6, 3):
        _c, wall_b, push_b, _both = RESULTS[(width, n, d, b)]
        wall_up = fly(b + 1, n, d, width, True, False)
        control_up = fly(b + 1, n, d, width, False, False)
        delay_b = wall_b[2] - RESULTS[(width, n, d, b)][0][2]
        delay_up = wall_up[2] - control_up[2]
        tilt_links = (
            (delay_b - delay_up) * Q / HEADING.t_d * 26
        )  # c_h x the delay difference per Link of b, over 26 Links
        bend_links = b - push_b[0]
        bend_c, tilt_c, _ = continuum_numbers(b, n, d, width)
        print(
            f"     b = {b}: the delay {delay_b} intervals at b, {delay_up} at b + 1; the front's tilt {tilt_links:6.2f} Links at the screen "
            f"(the continuum {tilt_c * 26:5.2f}); the row's bend {bend_links} Links (the continuum {bend_c * 26:5.2f})"
        )
print(
    "   the lattice reads the two combs (the age moment's and the flow's, in the mass's plane) and not the continuum's one number:"
)
print(
    "   the row's bend is the flow's comb (3 to 4 times the isotropic sum in the plane, the light-bending note's section 4), and"
)
print(
    "   the delay's difference between the rows at b and b + 1 is not a gradient at this fan (its sign flips from b = 6 to 3):"
)
print(
    "   the front's tilt is not readable by neighbouring rows at P = 6; it needs the dense fan (P >> r) or a shell mean. The pin"
)
print(
    "   for a run is the lattice's own two readings, the click's pixel and the click's age; the sum of the two halves never."
)
print()

# -- D. the pins, the Sun, the price ---------------------------------------------------------
print("D. THE PIN WORLDS, THE SUN, THE HOST PRICE")
print(
    "   at S = 1 (series K as registered) the push captures the beam (G M / (b c^2) = 11.5 at b = 6: the register's own words,"
)
print(
    "   'nature would capture the beam'); the width S is the world's one lever on the push (the drive's Q S M), the pair [1, S]"
)
print(
    "   keeps the wall's constant equal to the push's. The pin this note recommends: S = 256, the pair [1, 256], M = 2^12, b = 6 and 3:"
)
for b in (6, 3):
    control, wall, push, both = RESULTS[(256, 1, 256, b)]
    print(
        f"     b = {b}: the click's pixel {both[0]} against the control's {control[0]} (DETECTOR; the bracket 0.5 pixel), the age at the click "
        f"{both[2]} against {control[2]} (DETECTOR; the bracket 1 interval), {both[3]} turn(s) of the fan on the way (GAMEBOARD)"
    )
gm = 1.32712e20
r_sun, c_si = 6.957e8, 299_792_458.0
k_limb = gm / (r_sun * c_si**2)
arcsec = 180 / math.pi * 3600
print(
    f"   THE SUN: k = G M / (R c^2) = {k_limb:.3e}; the rule's bending 2 k = {2 * k_limb * arcsec:.4f} arcsec against nature's 4 k = {4 * k_limb * arcsec:.4f}"
)
print(
    "   (Dyson, Eddington and Davidson 1920: 1.98 +- 0.16 and 1.61 +- 0.40; VLBI gamma = 0.99992 +- 0.00012); the rule's delay"
)
print(
    "   (G M / c^3) ln(4 r_1 r_2 / b^2), half Shapiro's (Cassini 2003: gamma - 1 = (2.1 +- 2.3) x 10^-5): PPN gamma = 0 in both."
)
rows_crowd, rows_beam, nodes_with_rows = 13618, 447, 0
nodes_with_rows = sum(
    1 for n, p in PRESENCE.items() if p and abs(n[0]) <= 28 and abs(n[1]) <= 20 and abs(n[2]) <= 20
)
print(
    f"   THE PRICE (a count per interval on series K's `mass` world; the rows from BEAM_LAW note 35 (vii): {rows_crowd} crowd rows, {rows_beam} beam rows):"
)
print(
    f"     the reading of A and V at every Node with a row (5 columns, about 12 operations per row read): {12 * (rows_crowd + rows_beam)} per interval,"
)
print(f"     shared by every row at the Node ({nodes_with_rows} Nodes of the box hold crowd rows);")
print(
    f"     per row: the wall 2, the push 6, the nearest of the fan's neighbours 2 x 6, a turn 3: about 23 x {rows_crowd + rows_beam} = {23 * (rows_crowd + rows_beam)};"
)
print(
    f"     against today's walk, 16 x {rows_crowd + rows_beam} = {16 * (rows_crowd + rows_beam)}: about {(12 + 23 + 16) / 16:.1f} times the walk's count."
)
