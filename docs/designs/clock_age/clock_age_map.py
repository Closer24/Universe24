"""The clock's word, the presence or the age moment: the numbers of the read
(the mathematician, read-only, 2026-09-21; docs/designs/clock_age/NOTE.md).
(A) The dwell of a row at every Link of the heading by the flight's
accumulator on the engine's own lines (`direction_flight`, the one import):
the ages at which a row born at the source is at the Link r, checked against
series E's registered axis readings. (B) The two-crowd pin in series P's
geometry (two `mass` sources at 3 or 6 Links from a lamp on +y and +z, the
fan of nine, the same F): the presence and the age moment at the lamp's
Node per unit of F, the owed count k at F = 4915 and `suspension`
[1, 2^16], the detector's 1 + z = 1 + k, the ratio 6 : 3 under each word.
(C) The same pin as series E's shell means (the fan of 290 directions,
one unit per direction per interval): the presence and the age moment
averaged over the shells r = 3 and 6, and r = 4 .. 14 against the register.
(D) Nature's form: the gravitational shift between two heights under
k ~ M / r^2 and k ~ M / r, with the one constant fixed by the ground's
gradient (Pound and Rebka). Every lattice number is the stationary state
derived from the lines (a host derivation of what the detector or the
GameBoard would read, labelled); no run.

Run from the repository root:

    PYTHONPATH=src python docs/designs/clock_age/clock_age_map.py > docs/designs/clock_age/clock_age_map.out
"""

from __future__ import annotations

import math
from collections import defaultdict

from event_universe.events.nature_beam import Q, direction_flight

HEADINGS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def primitive(a: int, b: int, c: int) -> tuple[int, int, int]:
    g = math.gcd(math.gcd(abs(a), abs(b)), abs(c))
    return (a // g, b // g, c // g)


def fan_manhattan(bound: int) -> list[tuple[int, int, int]]:
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
    """The engine's Bresenham lines and flight constants of a direction table."""

    def __init__(self, table: list[tuple[int, int, int]]):
        self.table = table
        self.flight = direction_flight(tuple(table))
        self.index = {d: i for i, d in enumerate(table)}

    def age_of(self, d: tuple[int, int, int], made: int) -> int:
        """The first age at which the accumulator's count reaches `made` Links:
        (2 tau S_1 Q + T_D) // (2 T_D) >= made (Flight.accumulator, started at
        T_D, the rate 2 S_1 Q, the wall 2 T_D)."""
        i = self.index[d]
        rate = 2 * int(self.flight.manhattan[i]) * Q
        wall = 2 * int(self.flight.resolution[i])
        start = int(self.flight.resolution[i])
        return max(0, -(-(made * wall - start) // rate))

    def dwell(self, d: tuple[int, int, int], made: int) -> list[int]:
        """The ages at which the row is at its Link `made`."""
        return list(range(self.age_of(d, made), self.age_of(d, made + 1)))

    def nodes(self, d: tuple[int, int, int], links: int):
        """(the Node relative to the source, the Link index) along the line."""
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


def moments(lines: Lines, sources, links: int):
    """The stationary presence and age moment per Node from sources
    releasing one unit per direction per interval: sums over (line, Link)
    of the dwell's length and of its ages."""
    presence: dict = defaultdict(int)
    age_moment: dict = defaultdict(int)
    for origin, fan in sources:
        for d in fan:
            for (dx, dy, dz), made in lines.nodes(d, links):
                node = (origin[0] + dx, origin[1] + dy, origin[2] + dz)
                ages = lines.dwell(d, made)
                presence[node] += len(ages)
                age_moment[node] += sum(ages)
    return presence, age_moment


# -- A. the heading's dwell against series E's axis ---------------------------
print("A. THE DWELL OF A ROW AT EVERY LINK OF THE HEADING (the engine's accumulator, host)")
heading = Lines(HEADINGS)
d = (1, 0, 0)
i = heading.index[d]
print(
    f"   T_D = {int(heading.flight.resolution[i])}, the rate 2 S_1 Q = {2 * Q}, the wall 2 T_D = {2 * int(heading.flight.resolution[i])}, started at T_D"
)
register_axis = {4: 1.00, 6: 2.03, 8: 2.03, 10: 1.99, 12: 1.99, 14: 1.00}
register_age_r = {6: 65, 8: 106, 10: 172, 12: 255}
for r in range(1, 15):
    ages = heading.dwell(d, r)
    note = ""
    if r in register_axis:
        note = f"; series E's +x axis k scalar {register_axis[r]:.2f} at [1, 1]"
    if r in register_age_r:
        note += f", k age x r {register_age_r[r]} at [1, 2] (the moment {register_age_r[r] / r * 2:.1f})"
    print(f"   Link {r:2d}: the ages {ages} (the dwell {len(ages)}, the age moment {sum(ages)}){note}")
print(
    "   the continuum: the age at r is r sqrt 3 = 5.196 at 3 and 10.392 at 6, the ratio 2.000; the lattice's moments 11 and 21, the ratio 1.909"
)
print()

# -- B. series P's geometry at 3 and 6 Links -----------------------------------
print("B. THE TWO-CROWD PIN IN SERIES P'S GEOMETRY (the lamp at the origin; sources on +y and +z; host)")
F = 4915
SUSPENSION = (1, 1 << 16)
for distance in (3, 6):
    fan_y = sorted({primitive(dx, -distance, 0) for dx in range(-4, 5)})
    fan_z = sorted({primitive(dx, 0, -distance) for dx in range(-4, 5)})
    table = HEADINGS + [v for v in fan_y + fan_z if v not in HEADINGS]
    lines = Lines(table)
    sources = [((0, distance, 0), fan_y), ((0, 0, distance), fan_z)]
    presence, age_moment = moments(lines, sources, 3 * distance + 12)
    at_lamp = [
        (origin, v, made)
        for origin, fan in sources
        for v in fan
        for (dx, dy, dz), made in lines.nodes(v, 3 * distance + 12)
        if (origin[0] + dx, origin[1] + dy, origin[2] + dz) == (0, 0, 0)
    ]
    p = presence[(0, 0, 0)]
    a = age_moment[(0, 0, 0)]
    k_p = p * F * SUSPENSION[0] / SUSPENSION[1]
    k_a = a * F * SUSPENSION[0] / SUSPENSION[1]
    print(f"   the sources at {distance} Links, the fan of {len(fan_y)} per source {fan_y}")
    print(
        f"   the lines through the lamp's Node: {[(o, v, m) for o, v, m in at_lamp]} (the headings alone; the oblique lines cross the lamp's line beside it)"
    )
    print(
        f"   per unit of F: the presence {p} (2 sources x the dwell {p // 2}), the age moment {a} (the ages {heading.dwell((1, 0, 0), distance)} per source)"
    )
    print(
        f"   at F = {F} and suspension [1, 2^16]: the presence clock k = {p} F / 2^16 = {k_p:.3f}, 1 + z = {1 + k_p:.3f}; the age clock k = {a} F / 2^16 = {k_a:.3f}, 1 + z = {1 + k_a:.3f}"
    )
    print(
        f"   the F that reads k = 0.300 under the age word at {distance} Links: {0.3 * SUSPENSION[1] / a:.0f} (the presence word's {0.3 * SUSPENSION[1] / p:.0f})"
    )
    print(
        f"   the first interval with the crowd's rows at the lamp: age {heading.age_of((1, 0, 0), distance)} of the first row (the sources release from tick 1: tick {1 + heading.age_of((1, 0, 0), distance)})"
    )
    print(
        f"   the flow at the lamp (the push a coupled body would read, per unit of F): {p // 2} F x (0, -{Q}, 0) + {p // 2} F x (0, 0, -{Q}), the same at both distances"
    )
print(
    "   the ratio 6 : 3 of k: the presence word 4 / 4 = 1.000; the age word 42 / 22 = 1.909 (the continuum's 2)"
)
print()

# -- C. series E's shells --------------------------------------------------------
print(
    "C. THE SAME PIN AS SERIES E'S SHELL MEANS (the fan of 290, one unit per direction per interval; host)"
)
fan_e = fan_manhattan(6)
lines_e = Lines(fan_e)
presence_e, age_e = moments(lines_e, [((0, 0, 0), fan_e)], 40)
print(f"   the fan: {len(fan_e)} directions, q = {len(fan_e)} units per interval")


def shell(radius: int):
    found = []
    for x in range(-radius - 1, radius + 2):
        for y in range(-radius - 1, radius + 2):
            for z in range(-radius - 1, radius + 2):
                if abs(math.sqrt(x * x + y * y + z * z) - radius) < 0.5:
                    found.append((x, y, z))
    return found


register_shell = {
    4: (2.521, 8.748),
    6: (1.092, 5.711),
    8: (0.700, 4.904),
    10: (0.416, 3.657),
    12: (0.297, 3.097),
    14: (0.199, 2.366),
}
means = {}
for r in (3, 4, 6, 8, 10, 12, 14):
    nodes = shell(r)
    p_mean = sum(presence_e[n] for n in nodes) / len(nodes)
    a_mean = sum(age_e[n] for n in nodes) / len(nodes)
    counting = sum(1 for n in nodes if presence_e[n]) / len(nodes)
    means[r] = (p_mean, a_mean)
    note = ""
    if r in register_shell:
        ks, ka = register_shell[r]
        note = f"; the register (the window means) k scalar {ks:.3f} at [1, 1] and k age {ka:.3f} at [1, 2] (the moment {2 * ka:.2f})"
    print(
        f"   r = {r:2d}: {len(nodes):4d} Nodes, counting {counting:.2f}; the presence mean {p_mean:.3f} (x r^2 = {p_mean * r * r:.1f}), the age moment mean {a_mean:.3f} (x r = {a_mean * r:.1f}){note}"
    )
p3, a3 = means[3]
p6, a6 = means[6]
print(
    f"   the same source at 3 and 6: the presence 6 : 3 = {p6 / p3:.3f} (the continuum's 0.250), the age moment 6 : 3 = {a6 / a3:.3f} (the continuum's 0.500)"
)
print(
    f"   the crowd at 6 with 4 units per row (the same F at the shell): the presence 6 : 3 = {4 * p6 / p3:.3f} (1.000), the age moment 6 : 3 = {4 * a6 / a3:.3f} (2.000)"
)
print()

# -- D. nature's form ---------------------------------------------------------
print(
    "D. NATURE'S FORM: THE SHIFT BETWEEN TWO HEIGHTS UNDER EACH WORD (the constant fixed by the ground's gradient)"
)
GM = 3.986004418e14  # m^3 / s^2, the Earth
C_LIGHT = 299792458.0
R_EARTH = 6.371e6
R_GPS = 2.6560e7
g = GM / R_EARTH**2
print(
    f"   the Earth: G M / (R c^2) = {GM / (R_EARTH * C_LIGHT**2):.3e}; g / c^2 = {g / C_LIGHT**2:.3e} per metre"
)
print(
    f"   Pound and Rebka's 22.5 m: g h / c^2 = {g * 22.5 / C_LIGHT**2:.2e} under either word (one reading fixes the one constant)"
)
ratio_pot = R_EARTH / R_GPS
ratio_pres = (R_EARTH / R_GPS) ** 2
print(
    f"   k(orbit) / k(ground) at the GPS radius {R_GPS / 1e3:.0f} km: the age word (M / r) {ratio_pot:.4f}; the presence word (M / r^2) {ratio_pres:.4f}"
)
shift_pot = GM / C_LIGHT**2 * (1 / R_EARTH - 1 / R_GPS)
shift_pres = (g / C_LIGHT**2) * (R_EARTH / 2) * (1 - ratio_pres)
print(
    f"   the ground-to-orbit shift per day: the age word {shift_pot * 86400 * 1e6:.1f} us (nature's 45.7, Ashby 2003); the presence word with the ground's gradient {shift_pres * 86400 * 1e6:.1f} us, the ratio {shift_pres / shift_pot:.3f}"
)
e = 0.162
print(
    f"   an eccentric orbit (Galileo 5 and 6, e = {e}): the modulation of k over the orbit, peak to peak over the mean: M / r gives {2 * e / (1 - e * e):.3f}, M / r^2 gives {(1 / (1 - e) ** 2 - 1 / (1 + e) ** 2) / ((1 / (1 - e) ** 2 + 1 / (1 + e) ** 2) / 2):.3f}: the presence word doubles the modulation nature reads at the potential's value"
)
sigma = 1.0e6
print(
    f"   a cluster member at a velocity dispersion sigma = 1000 km/s: the potential term G M / (r c^2) ~ sigma^2 / c^2 = {sigma**2 / C_LIGHT**2:.1e}; the Doppler spread sigma / c = {sigma / C_LIGHT:.1e}"
)
print()

# -- E. the shell's lines: Poisson's source term after a detector --------------
# Added 2026-09-22 for series X (Poisson after a detector), the chief
# physicist's design of record 574 of docs/LOG_2026-09-20.md under the
# owner's word of that day ("build them", records 574 and 581): series T
# reads a clock's rate after a detector OUTSIDE a point crowd, Laplace's
# part; Poisson's equation is the source term, so the crowd's point source
# is replaced by a spherical shell of sources of radius R and the same
# total release, and a lamp is read INSIDE it (the shell theorem: the age
# moment flat) and outside it (C / r). The shell's Nodes are selected as
# the lensing generator selects a shell, |r - R| < 1/2 (section C's
# `shell`), and every source releases on the full fan of section C.
#
# The one thing this section adds to sections B and C: the shell's sources
# stand in one another's rows, so each one's OWN clock counts the age
# moment at its Node and owes intervals by the law's default word
# (clock-age-v1, record 394), and a source releases only at its
# self-creations (`nature_beam._release` is reached only when the frame
# left the body creating). A source's release per interval is therefore
# its declared rate over 1 + its own count, and the shell's effective
# release is the fixed point of that map, which this section iterates to
# convergence. With uniform sources the interior is flat exactly; the
# spread of the sources' own clocks over the lattice shell is the ripple
# this section names, the one the pin of series X carries.
SHELL_RADIUS = 6
SHELL_LAMP_RADII = (2, 4, 12)
# The reach in Links of the walk from a source: the furthest target is the
# lamp outside at 12 Links from the centre, 18 Euclidean Links from the far
# side of the shell, at most sqrt 3 Links of the digital line per Euclidean
# Link on the cube diagonal.
SHELL_REACH = 40
print("E. THE SHELL'S LINES: POISSON'S SOURCE TERM AFTER A DETECTOR (series X; host)")
shell_nodes = shell(SHELL_RADIUS)
shell_lamps = {r: (-r, 0, 0) for r in SHELL_LAMP_RADII}
# The targets of the walk: every source's own Node (for its own clock) and
# the three lamp Nodes.
shell_targets = {node: index for index, node in enumerate(shell_nodes)}
for offset, radius in enumerate(SHELL_LAMP_RADII):
    shell_targets[shell_lamps[radius]] = len(shell_nodes) + offset
shell_walk = {d: lines_e.nodes(d, SHELL_REACH) for d in fan_e}
shell_dwell = {(d, made): lines_e.dwell(d, made) for d in fan_e for _, made in shell_walk[d]}
# The contribution matrix, one walk of the fan from every source: per
# source the presence and the age moment it leaves at every target, per
# unit of its release per direction per interval.
target_count = len(shell_targets)
shell_presence = [[0] * target_count for _ in shell_nodes]
shell_moment = [[0] * target_count for _ in shell_nodes]
for index, origin in enumerate(shell_nodes):
    presence_row, moment_row = shell_presence[index], shell_moment[index]
    for d in fan_e:
        for (dx, dy, dz), made in shell_walk[d]:
            target = shell_targets.get((origin[0] + dx, origin[1] + dy, origin[2] + dz))
            if target is not None:
                ages = shell_dwell[(d, made)]
                presence_row[target] += len(ages)
                moment_row[target] += sum(ages)
print(
    f"   the shell |r - {SHELL_RADIUS}| < 1/2: {len(shell_nodes)} Nodes, each releasing on the fan of "
    f"{len(fan_e)}; the lamp at {', '.join(str(r) for r in SHELL_LAMP_RADII)} Links from the centre"
)
for radius in SHELL_LAMP_RADII:
    target = shell_targets[shell_lamps[radius]]
    print(
        f"   uniform sources, r = {radius:2d}: per unit of the release the presence "
        f"{sum(row[target] for row in shell_presence):5d}, the age moment "
        f"{sum(row[target] for row in shell_moment):6d}"
        + ("  (inside)" if radius < SHELL_RADIUS else "  (outside)")
    )
uniform_inside = [sum(row[shell_targets[shell_lamps[r]]] for row in shell_moment) for r in (2, 4)]
print(
    f"   the shell theorem on the lattice, the age moment: {uniform_inside[0]} at r = 2 and "
    f"{uniform_inside[1]} at r = 4, the ratio "
    f"{uniform_inside[0] / uniform_inside[1]:.6f} (the continuum's 1 exactly; the flat interior)"
)
uniform_presence = [sum(row[shell_targets[shell_lamps[r]]] for row in shell_presence) for r in (2, 4)]
print(
    f"   the presence at the same two Nodes: {uniform_presence[0]} and {uniform_presence[1]}, the "
    f"ratio {uniform_presence[0] / uniform_presence[1]:.4f} (the flux rises toward the shell: "
    "1 / r^2 obeys Gauss, not Poisson, and is not flat inside)"
)
# The release: series T's crowd's total release pair (two sources at
# F = 4915 units per direction per interval) spread over the shell's Nodes,
# the design's scaling of record 574 (each source on the full fan, the
# release pair per source scaled down by the shell's Node count).
SHELL_AMOUNT = 2 * F * SUSPENSION[1] // len(shell_nodes)
shell_rate = SHELL_AMOUNT / SUSPENSION[1]
# The fixed point of the sources' own clocks: a source's release per
# interval is its rate over 1 + its own count (the age word).
effective = [shell_rate] * len(shell_nodes)
own_count = [0.0] * len(shell_nodes)
rounds = 0
move = 0.0
while rounds < 200:
    rounds += 1
    own_count = [
        sum(
            effective[source] * shell_moment[source][target]
            for source in range(len(shell_nodes))
            if source != target
        )
        * SUSPENSION[0]
        / SUSPENSION[1]
        for target in range(len(shell_nodes))
    ]
    moved = [shell_rate / (1 + count) for count in own_count]
    move = max(abs(a - b) for a, b in zip(moved, effective, strict=True))
    effective = moved
    if move < 1e-12:
        break
print(
    f"   the declared release per source per direction: {SHELL_AMOUNT} / 2^16 = {shell_rate:.4f} units "
    f"per interval (series T's crowd's total 2 F over {len(shell_nodes)} Nodes)"
)
print(
    f"   the sources' own clocks (the fixed point after {rounds} rounds, the last move "
    f"{move:.1e}): each source's own count k {min(own_count):.3f} to {max(own_count):.3f} (mean "
    f"{sum(own_count) / len(own_count):.3f}), so its release per interval is "
    f"{min(effective):.4f} to {max(effective):.4f} (mean {sum(effective) / len(effective):.4f}), "
    f"{sum(effective) / len(effective) / shell_rate:.3f} of the declared rate"
)
shell_k = {}
for radius in SHELL_LAMP_RADII:
    target = shell_targets[shell_lamps[radius]]
    k_age = (
        sum(effective[source] * shell_moment[source][target] for source in range(len(shell_nodes)))
        * SUSPENSION[0]
        / SUSPENSION[1]
    )
    k_presence = (
        sum(effective[source] * shell_presence[source][target] for source in range(len(shell_nodes)))
        * SUSPENSION[0]
        / SUSPENSION[1]
    )
    k_age_uniform = shell_rate * sum(row[target] for row in shell_moment) * SUSPENSION[0] / SUSPENSION[1]
    shell_k[radius] = (k_age, k_presence, k_age_uniform)
    print(
        f"   r = {radius:2d}: the age word k = {k_age:.4f} (uniform sources {k_age_uniform:.4f}), "
        f"1 + z = {1 + k_age:.4f}, the clicks per interval {1 / (1 + k_age):.4f}; the presence word "
        f"k = {k_presence:.4f}, 1 + z = {1 + k_presence:.4f}"
    )
inside_age = shell_k[2][0] / shell_k[4][0]
inside_presence = shell_k[2][1] / shell_k[4][1]
outside_age = shell_k[12][0] / shell_k[4][0]
print(
    f"   THE PIN INSIDE (the age word): k(2) / k(4) = {inside_age:.4f}, the continuum's 1.0000 "
    f"(the shell theorem); the ripple {abs(inside_age - 1):.4f} is the spread of the sources' own "
    "clocks over the lattice shell, nothing else (with uniform sources the two are one integer)"
)
print(
    f"   THE PIN INSIDE (the presence word, expected to FAIL): k(2) / k(4) = {inside_presence:.4f}, "
    f"{abs(inside_presence - 1) / abs(inside_age - 1):.0f} times the age word's ripple from 1: the "
    "one reading that tells the two words apart at a source term"
)
print(
    f"   THE PIN OUTSIDE (the age word): k(12) / k(4) = {outside_age:.4f}, the continuum's "
    f"R / 12 = {SHELL_RADIUS / 12:.4f} (the shell's exterior is the point source's C / r); the "
    "lattice reads above it by the grain of section C, where the age moment x r rises with r "
    f"({outside_age / (SHELL_RADIUS / 12):.3f} of the continuum's)"
)
print(
    f"   the rates a detector reads: rate(2) / rate(4) = "
    f"{(1 + shell_k[4][0]) / (1 + shell_k[2][0]):.4f} inside under the age word, "
    f"{(1 + shell_k[4][1]) / (1 + shell_k[2][1]):.4f} under the presence word; rate(4) / rate(12) = "
    f"{(1 + shell_k[12][0]) / (1 + shell_k[4][0]):.4f} outside under the age word"
)
print(
    "   THE PINS OF SERIES X IN ONE LINE (what the register quotes, six decimals; the release "
    f"{SHELL_AMOUNT} / 2^16 per source per direction):"
)
for radius in SHELL_LAMP_RADII:
    k_age, k_presence, k_age_uniform = shell_k[radius]
    print(
        f"     r = {radius:2d}: k_age {k_age:.6f}  k_presence {k_presence:.6f}  "
        f"k_age_uniform {k_age_uniform:.6f}"
    )
print(
    f"     k_age(2) / k_age(4) {inside_age:.6f}   k_presence(2) / k_presence(4) "
    f"{inside_presence:.6f}   k_age(12) / k_age(4) {outside_age:.6f}"
)
