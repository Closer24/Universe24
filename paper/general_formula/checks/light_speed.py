"""The pace of the rows, c = 1 / sqrt 3 Links per interval, from the flight
table's definition alone (BEAM_LAW section 3; the paper's model section):
what is proved, what is a choice, what the finite grain predicts, and the
known lattice numbers it must be told apart from. Formulas evaluated from
the definitions and the repository's integers, not an engine run.

1. Cauchy-Schwarz: S_1 <= sqrt 3 |d| for every direction d, so S_1 Q_f
   <= T_d = isqrt(3 |d|^2 Q_f^2): at most one Link per interval on every
   digital line; S_1 = sqrt 3 |d| exactly on the cube diagonals, and the
   integer equality also holds where isqrt's floor closes a gap below
   1 / Q_f. Counted over
   every primitive direction with components within 64 (the design's
   map counted 1 780 418; this script counts them again).
2. The Euclidean pace Q_f |d| / T_d per direction: 1 / sqrt 3 within
   1 / T_d, largest on a heading (64 / 110 at Q_f = 64); the anisotropy
   shrinks as 1 / (sqrt 3 Q_f), so a measured bound on the anisotropy of c
   bounds the flight scale Q_f.
3. The supremum: any pace v the same in every direction with at most one
   Link per interval satisfies v <= |d| / S_1 for every d, least on the
   cube diagonals, 1 / sqrt 3 (1 / sqrt n in n dimensions). The flight
   table sits at the supremum: that it does is a choice of the design, not
   a consequence of the two rules.
4. The octahedron: the Nodes one interval away form the L1 unit ball, the
   octahedron with the six Ports as vertices; its inscribed sphere has the
   radius 1 / sqrt 3 and touches the faces on the cube diagonals; the 48
   signed axis permutations (3! x 2^3) are its symmetry, 24 of determinant
   +1 and 24 of -1; T_d and S_1 are invariant under all 48, the digital
   line's tie by axis order is not.
5. The known numbers: the Courant bound of the wave equation on the cubic
   grid, c dt / dx <= 1 / sqrt n, and the lattice Boltzmann sound speed
   c_s^2 = 1 / 3 in three dimensions (Qian, d'Humieres and Lallemand 1992),
   both 1 / sqrt 3 in lattice units.

    python paper/click_model/checks/light_speed.py
"""

from __future__ import annotations

import math
from itertools import permutations, product

FLIGHT_SCALE = 64  # Q_f, the flight scale of every world of the paper
WITHIN = 64  # the components' bound of the design's map


def resolution(direction: tuple[int, ...], scale: int) -> int:
    """T_d = isqrt(3 |d|^2 Q_f^2), the flight table's resolution of d."""
    return math.isqrt(3 * sum(c * c for c in direction) * scale * scale)


def manhattan(direction: tuple[int, ...]) -> int:
    return sum(abs(c) for c in direction)


def section(title: str) -> None:
    print(f"\n== {title}")


def cauchy_schwarz() -> None:
    section(
        f"1. S_1 Q_f <= T_d on every primitive direction with components within {WITHIN}, Q_f = {FLIGHT_SCALE}"
    )
    count = equal = diagonal = 0
    nearest = None
    slowest = (1.0, (0, 0, 0))
    fastest = (0.0, (0, 0, 0))
    for direction in product(range(-WITHIN, WITHIN + 1), repeat=3):
        if direction == (0, 0, 0) or math.gcd(*direction) != 1:
            continue
        count += 1
        s1 = manhattan(direction)
        t_d = resolution(direction, FLIGHT_SCALE)
        assert s1 * FLIGHT_SCALE <= t_d, direction
        if s1 * FLIGHT_SCALE == t_d:
            equal += 1
            if abs(direction[0]) == abs(direction[1]) == abs(direction[2]) == 1:
                diagonal += 1
            elif nearest is None or s1 < manhattan(nearest):
                nearest = direction
        pace = FLIGHT_SCALE * math.sqrt(sum(c * c for c in direction)) / t_d
        slowest = min(slowest, (pace, direction))
        fastest = max(fastest, (pace, direction))
    print(f"  primitive directions: {count}; S_1 Q_f <= T_d on every one (asserted)")
    print(
        f"  equality S_1 Q_f = T_d on {equal} directions: the {diagonal} cube diagonals (+-1, +-1, +-1), where"
        f" S_1 = sqrt 3 |d| exactly, and {equal - diagonal} directions near them where isqrt's floor closes a gap"
        f" below 1 / Q_f (the shortest {nearest}: S_1 = {manhattan(nearest)}, sqrt 3 |d| ="
        f" {math.sqrt(3 * sum(c * c for c in nearest)):.4f}); on all of them the row crosses exactly one Link"
        " per interval and its Euclidean pace |d| / S_1 exceeds 1 / sqrt 3 by less than 1 / T_d"
    )
    print(
        f"  the Euclidean pace Q_f |d| / T_d: slowest {slowest[0]:.4f} on {slowest[1]},"
        f" fastest {fastest[0]:.4f} on {fastest[1]}; 1 / sqrt 3 = {1 / math.sqrt(3):.4f}"
    )


def anisotropy() -> None:
    section("2. The pace per direction and the anisotropy's scale 1 / (sqrt 3 Q_f)")
    directions = ((1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 1, 0), (3, 1, 0), (5, 2, 1))
    print("   Q_f      " + "  ".join(f"{str(d):>11s}" for d in directions) + "   bound 1/(sqrt3 Q_f)")
    for scale in (64, 256, 4096, 1 << 20):
        paces = []
        for direction in directions:
            t_d = resolution(direction, scale)
            paces.append(scale * math.sqrt(sum(c * c for c in direction)) / t_d)
        print(
            f"  {scale:8d}  "
            + "  ".join(f"{p:11.6f}" for p in paces)
            + f"   {1 / (math.sqrt(3) * scale):.2e}"
        )
    heading = FLIGHT_SCALE / resolution((1, 0, 0), FLIGHT_SCALE)
    print(
        f"  at Q_f = {FLIGHT_SCALE} the heading's pace is {FLIGHT_SCALE} / {resolution((1, 0, 0), FLIGHT_SCALE)}"
        f" = {heading:.4f}, {100 * (heading * math.sqrt(3) - 1):.2f} percent above 1 / sqrt 3;"
        f" the plane diagonal {100 * (FLIGHT_SCALE * math.sqrt(2) / resolution((1, 1, 0), FLIGHT_SCALE) * math.sqrt(3) - 1):.2f} percent;"
        " the cube diagonal exact"
    )
    for bound in (1e-9, 1e-17, 1e-18):
        print(
            f"  a measured anisotropy of c below {bound:.0e} (in the lattice's frame) needs"
            f" Q_f >= 1 / (sqrt 3 x {bound:.0e}) = {1 / (math.sqrt(3) * bound):.1e}"
        )
    print(
        "  the anisotropy is the table's rounding on the heading, both ways along the line;"
        " a bound of order 1e-18 (Nagel et al. 2015) puts Q_f above 5.8e17 if the laboratory is the lattice's frame"
    )


def supremum() -> None:
    section(
        "3. The supremum of isotropic paces under one Link per interval: min |d| / S_1 over directions"
    )
    for dimension in (1, 2, 3):
        diagonal = tuple([1] * dimension)
        ratio = math.sqrt(dimension) / manhattan(diagonal)
        print(
            f"  n = {dimension}: the cube diagonal {diagonal} gives |d| / S_1 = {ratio:.4f} = 1 / sqrt {dimension}"
        )
    print(
        "  every other direction gives more (Cauchy-Schwarz), so 1 / sqrt 3 is the largest pace the same in every direction"
        " that crosses at most one Link per interval on every digital line; a slower isotropic pace also obeys both rules:"
        " the flight table's choice of the supremum is a third statement, not a consequence of the two"
    )


def digital_line(direction: tuple[int, int, int], links: int) -> list[tuple[int, int, int]]:
    """The digital line of d as LAW.md 4.1 states it: at each Link the axis
    whose deficit |d_i| (m + 1) - S_1 |pos_i| is largest steps, x before y
    before z on a tie."""
    s1 = manhattan(direction)
    position = [0, 0, 0]
    nodes = []
    for m in range(links):
        deficits = [abs(direction[i]) * (m + 1) - s1 * abs(position[i]) for i in range(3)]
        axis = max(range(3), key=lambda i: (deficits[i], -i))
        position[axis] += 1 if direction[axis] > 0 else -1
        nodes.append(tuple(position))
    return nodes


def octahedron_and_group() -> None:
    section("4. The octahedron of one interval, its inscribed sphere and the group of 48")
    face_distance = 1 / math.sqrt(3)
    print(
        f"  the L1 unit ball |x| + |y| + |z| <= 1: vertices the six Ports, faces x +- y +- z = +-1 at the distance"
        f" {face_distance:.4f} = 1 / sqrt 3 from the Node, touched at (+-1, +-1, +-1) / 3 on the cube diagonals"
    )
    group = []
    for axes in permutations(range(3)):
        for signs in product((1, -1), repeat=3):
            group.append((axes, signs))
    hands = {}
    for axes, signs in group:
        parity = 1
        for i in range(3):
            for j in range(i + 1, 3):
                if axes[i] > axes[j]:
                    parity = -parity
        hand = parity * signs[0] * signs[1] * signs[2]
        hands[hand] = hands.get(hand, 0) + 1
    print(
        f"  signed axis permutations: {len(group)} = 3! x 2^3; determinant +1 (rotations) {hands[1]}, -1 (reflections) {hands[-1]}"
    )

    def act(axes, signs, vector):
        image = [0, 0, 0]
        for i in range(3):
            image[axes[i]] = signs[i] * vector[i]
        return tuple(image)

    for direction in ((1, 0, 0), (1, 1, 0), (2, 1, 0), (5, 2, 1)):
        s1 = manhattan(direction)
        invariant = all(
            resolution(act(a, s, direction), FLIGHT_SCALE) == resolution(direction, FLIGHT_SCALE)
            and manhattan(act(a, s, direction)) == s1
            for a, s in group
        )
        period = 2 * s1
        line = digital_line(direction, period)
        differing = at_periods = 0
        for a, s in group:
            image_line = digital_line(act(a, s, direction), period)
            moved_line = [act(a, s, node) for node in line]
            for m, (x, y) in enumerate(zip(image_line, moved_line, strict=True)):
                if x != y:
                    differing += 1
                    if (m + 1) % s1 == 0:
                        at_periods += 1
        print(
            f"  {direction}: T_d and S_1 invariant under all 48: {invariant}; the digital line of g d against g applied to"
            f" the line of d over two periods ({period} Links): {differing} of {48 * period} Node positions differ"
            f" (the tie by axis order), {at_periods} of them at a whole period"
        )


def known_numbers() -> None:
    section("5. The known lattice numbers to tell apart")
    for dimension in (1, 2, 3):
        print(
            f"  the Courant bound of the wave equation on the cubic grid in {dimension} dimension(s):"
            f" c dt / dx <= 1 / sqrt {dimension} = {1 / math.sqrt(dimension):.4f}"
        )
    print(
        "  the lattice Boltzmann sound speed on D3Q19 (and D2Q9): c_s^2 = 1 / 3 of the lattice speed squared,"
        f" c_s = {math.sqrt(1 / 3):.4f} in lattice units; in the click model the same number by the Courant condition's"
        " own domain-of-dependence argument (the sphere of radius c dt inside the stencil's octahedron), on an exact integer table"
    )


def no_dispersion() -> None:
    """The pace of a row is a function of its direction alone, Q_f |d| / T_d,
    whatever its phase rate n / d: the flight table has no rate argument and
    no rule of the interval reads the phase into the pace (the pure-shift
    case of a lattice automaton, a ballistic walker with a passenger phase).
    Paired with the isotropy of section 1 this is what no local linear wave
    scheme on Z^3 can do: its dispersion relation is a trigonometric
    polynomial in k a, and c |k| is not periodic, so omega = c |k| holds on
    no open set of k. The numbers: the standard second-order scheme at the
    Courant number 1 / sqrt 3 on an axis, sin^2(omega dt / 2) = (1/3)
    sin^2(k a / 2), has the group velocity 1 - (k a)^2 / 12 and zero at the
    band edge; on the cube diagonal the same scheme is exactly dispersionless;
    a fourth-order scheme has (k a)^4. Under the reading (assumed) that a
    photon of energy E is a family whose phase turns E dt / h per interval,
    the Link is bounded by the shortest wavelength seen (the 1.4 PeV photon of
    LHAASO 2021; a bound every lattice model shares) and by nothing of the
    time-of-flight tests, which bound the second-order scheme's Link on an
    axis through one GRB photon (GRB 090510: 31 GeV within 0.83 s at z =
    0.903, the comoving distance 9.47e25 m for H_0 = 71 and Omega_m = 0.27,
    without the cosmological weighting, conservative)."""
    section("6. No dispersion: the pace is the direction's, at every phase rate")
    planck_ev_m = 1.23984198e-6  # h c in eV m
    for direction in ((1, 0, 0), (1, 1, 0), (5, 2, 1)):
        t_d = resolution(direction, FLIGHT_SCALE)
        pace = FLIGHT_SCALE * math.sqrt(sum(c * c for c in direction)) / t_d
        for n, d in ((1, 8), (8, 1), (32, 1)):
            wavelength_intervals = 64 * d / n
            print(
                f"  {direction}: rate {n}/{d} steps per interval at N = 64, a turn every {wavelength_intervals:6.2f} intervals"
                f" = {wavelength_intervals * pace:6.3f} Links along the line, pace {pace:.4f} (the same at every rate)"
            )
    print(
        "  the shortest turn: the alias bound N / 2 steps per interval, two intervals, 2 / sqrt 3 = 1.1547 Links on the cube"
        " diagonal, 1.164 on a heading (the pair form); two Links under the integer form, spanning sqrt 2 Links of length on"
        " a cube diagonal's line"
    )
    lhaaso_ev = 1.4e15
    wavelength = planck_ev_m / lhaaso_ev
    print(
        f"  the 1.4 PeV photon (LHAASO 2021), read as a family turning E dt / h per interval (assumed): lambda = {wavelength:.3e} m;"
        f" the Link a <= lambda sqrt 3 / 2 = {wavelength * math.sqrt(3) / 2:.3e} m under the pair form,"
        f" a <= lambda / sqrt 2 = {wavelength / math.sqrt(2):.3e} m under the integer form (the weakest direction, the cube diagonal)"
    )
    nu2 = 1 / 3

    def omega_axis(ka: float) -> float:
        return 2 * math.asin(math.sqrt(nu2) * math.sin(ka / 2))  # omega dt on an axis

    def omega_diagonal(ka: float) -> float:
        # k = (k, k, k) / sqrt 3: sin^2(omega dt / 2) = (1 / 3) x 3 sin^2(k a / (2 sqrt 3))
        return 2 * math.asin(math.sin(ka / (2 * math.sqrt(3))))

    def group_velocity(omega, ka: float) -> float:
        h = 1e-6
        return (omega(ka + h) - omega(ka - h)) / (2 * h) / math.sqrt(nu2)  # over c

    print(
        "  the standard second-order scheme on the same Link (Courant number 1 / sqrt 3): group velocity over c, on an axis"
        " and on the cube diagonal"
    )
    for ka in (1e-2, 1e-1, 1.0, 2.0, 3.0, math.pi - 1e-9):
        print(
            f"    |k| a = {ka:8.4f}: axis {group_velocity(omega_axis, ka):.9f} (1 - (k a)^2 / 12 = {1 - ka * ka / 12:.9f});"
            f" cube diagonal {group_velocity(omega_diagonal, ka):.9f}"
        )
    print(
        "    the scheme is exactly dispersionless on the cube diagonal at this Courant number, and zero at the axis's band edge"
    )
    photon_ev, delay_s, distance_m = 31e9, 0.83, 9.47e25
    light = 299792458.0
    dv = delay_s / (distance_m / light)
    grb_wavelength = planck_ev_m / photon_ev
    ka_second = math.sqrt(12 * dv)
    a_second = ka_second * grb_wavelength / (2 * math.pi)
    alpha = 1 / 100
    ka_fourth = (dv / alpha) ** 0.25
    a_fourth = ka_fourth * grb_wavelength / (2 * math.pi)
    print(
        f"  GRB 090510: a {photon_ev / 1e9:.0f} GeV photon within {delay_s} s over {distance_m:.2e} m: |v_g - c| / c < {dv:.2e}"
        f" (lambda = {grb_wavelength:.1e} m); the second-order scheme on an axis needs (k a)^2 / 12 below it: a < {a_second:.1e} m;"
        f" a fourth-order scheme with (k a)^4 / 100 needs a < {a_fourth:.1e} m; on the cube diagonal the second-order scheme is not bounded at all"
    )
    print(
        "  the model's rows: the pace independent of the rate on every line, so no time-of-flight bound; the Link bounded only by"
        " the shortest wavelength seen, the bound every lattice shares; one measured energy dependence of c refutes the flight as defined"
    )
    print(
        "  what the lattice leaves: the direction's rounding, below 1 / T_d, the same at every wavelength; the price: no wave on the"
        " lattice, the interference summed in the record, and the photon's energy entering only by the reading assumed above"
    )


def main() -> None:
    cauchy_schwarz()
    anisotropy()
    supremum()
    octahedron_and_group()
    known_numbers()
    no_dispersion()


if __name__ == "__main__":
    main()
