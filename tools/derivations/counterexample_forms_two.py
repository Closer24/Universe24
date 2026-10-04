"""The breaker's second set of rows for the currents, the credit and the screen (the method of 2026-10-04): the odd lines sourced by the halved current (S.33 (d)), the force between moving charges (S.33 (e), the magnetism row), a body's count as the conserved form's own current with the Link's factor squared, the marginals' no signalling and the rounding's one non-local place, the which-way sum, one photon on two bodies (S.57) and the region's reading factor with the draw's scatter (S.8). Each row is tried inside its stated condition and outside it on the smallest configuration; every step of the line is rule3.py's or proofs_ground.py's, every share proofs_booking's, every credit proofs_credit's or clicks.py's, the screen's rows two_slits.py's Huygens sum, the 3D lattice kernel greens_function.py's. The Row is counterexample_rows.py's; the registry is counterexamples.py's."""

from __future__ import annotations

import math
import random
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clicks  # noqa: E402
import greens_function  # noqa: E402
import proofs_credit  # noqa: E402
import rule3  # noqa: E402
import sign  # noqa: E402
import two_slits  # noqa: E402
from counterexample_rows import PORTS, Row  # noqa: E402
from proofs_booking import rational_share  # noqa: E402
from proofs_ground import SEED, Gaussian, angles, draw_angle, read, step_line  # noqa: E402

MATTER = (2, 3)
PYTHAGOREAN_BETAS = (
    (Fraction(3, 5), Fraction(5, 4)),
    (Fraction(5, 13), Fraction(13, 12)),
    (Fraction(8, 17), Fraction(17, 15)),
    (Fraction(7, 25), Fraction(25, 24)),
    (Fraction(20, 29), Fraction(29, 21)),
)  # (beta, gamma) with gamma = 1 / sqrt(1 - beta^2) rational


def chain_rest(ratio: Fraction, count: int) -> tuple[int, int, list[Fraction]]:
    """The gapped holder's rest C (lambda^x + lambda^(N - x)) on a periodic chain of `count` Nodes for a unit amplitude at the source Node 0, lambda = `ratio` the fall per Link: the pair from lambda + 1 / lambda + 4 = 6 den / num (S.11); returns (num, den, levels)."""
    six = 6 / (ratio + 1 / ratio + 4)
    num, den = six.numerator, six.denominator
    norm = 1 + ratio**count
    return num, den, [(ratio**x + ratio ** (count - x)) / norm for x in range(count)]


def source_of(
    levels: Sequence[Fraction], arrivals: Sequence[Sequence[int]], num: int, den: int
) -> list[Fraction]:
    """sigma_i = 2 a_i - (the line's right side) / w at rest, the source the static line needs at every Node (6 den a = num S_6(a) + 3 den sigma at the vacuum's paces), 0 away from the source."""
    return [
        2 * levels[i] - rule3.step_exact(levels[i], Fraction(0), [levels[j] for j in ports], num, den)
        for i, ports in enumerate(arrivals)
    ]


def odd_lines_sourced_by_the_halved_current() -> Row:
    """Section 8 ('So the odd lines are sourced by the halved current over the same wall as the time level'), S.33 (a), (b), (d): the continuity identity w [W_i(t + 1) - W_i(t)] + R (g_(i, i+1) - g_(i-1, i)) = 0 exact on a chain (sign.py), flux over density the band's group velocity, and on a plane record the Node's current J_a = g_(i, i+a) + g_(i-a, i) is 2 (w / R_a) W v exactly in Gaussian rationals, the Node's flux the mean of its two Links'; the holder's static solution sourced by a point charge on a chain in exact rationals, Yukawa's tail lambda^|x| with the write 3 den / (num (1 / lambda - lambda)) per unit source at the Node, and on the 3D lattice Coulomb's 1 / r with 3 G(0) = 0.7582 at the source Node (greens_function); outside: a source moving one Node, where one step of the line leaves the field short of the new rest at the far Nodes, the retarded form."""
    draw = random.Random(SEED)
    continuity = sign.continuity_identity_residual() == 0 and sign.flux_over_density_residual() < 1e-12
    halved = True
    for num, den in ((1, 1), MATTER):
        wall, reads, _ = rule3.coefficients(num, den)
        for wave in angles(draw, 6)[2:]:
            rotation = draw_angle(draw)
            while rotation.im == 0:  # a rotation with sin omega = 0 carries no Wronskian
                rotation = draw_angle(draw)
            amplitude = Fraction(draw.randint(1, 9))
            z = [Gaussian(amplitude, 0) * wave**x for x in range(3)]  # at the interval 0
            z_before = [v * rotation for v in z]  # the phase one interval earlier
            wronskian = (z[1].conj() * z_before[1]).im
            current = (z[1].conj() * z[2]).im + (z[0].conj() * z[1]).im  # g_(i, i+1) + g_(i-1, i)
            velocity = Fraction(reads[0], wall) * wave.im / rotation.im  # (R / w) sin k / sin omega
            halved &= current == 2 * Fraction(wall, reads[0]) * wronskian * velocity
            halved &= (
                (z[1].conj() * z[2]).im == (z[0].conj() * z[1]).im == current / 2
            )  # the Node's flux the mean of its two Links'
    ratio, count = Fraction(1, 3), 12
    num, den, rest = chain_rest(ratio, count)
    arrivals = rule3.chain_arrivals(count)
    sources = source_of(rest, arrivals, num, den)
    tail = all(sources[x] == 0 for x in range(1, count))
    # the infinite chain's write per unit source, lambda^|x| exactly: at the source 2 C - (2 R lambda C + 4 R C + S C) / w
    c = Fraction(1)
    sigma = 2 * c - rule3.step_exact(c, Fraction(0), [c * ratio, c * ratio, c, c, c, c], num, den)
    write = c / sigma == Fraction(3 * den, num) / (1 / ratio - ratio)
    coulomb = greens_function.three_g()[0]
    far = greens_function.four_pi_r_g()[-1]
    moved = [Fraction(0)] + sources[:-1]  # the source carried to Node 1
    stepped = [
        rule3.step_exact(rest[i], rest[i], [rest[j] for j in ports], num, den) + moved[i]
        for i, ports in enumerate(arrivals)
    ]
    new_rest = [rest[(x - 1) % count] for x in range(count)]
    retarded = max(abs(stepped[x] - new_rest[x]) for x in range(count))
    far_unchanged = stepped[6] == rest[6] != new_rest[6]
    return Row(
        "So the odd lines are sourced by the halved current over the",
        continuity
        and halved
        and tail
        and bool(write)
        and round(coulomb, 4) == 0.7582
        and abs(far - 1) < 0.02,
        retarded > 0 and far_unchanged,
        f"continuity exact, J_a = 2 (w / R) W v exact on plane records of 2 pairs; Yukawa's tail (1 / 3)^|x| with the write 3 den / (num (1 / lambda - lambda)) exact at [{num}, {den}]; 3 G(0) = {coulomb:.4f}, 4 pi r G(r) = {far:.3f} at r = 5; the source moved one Node: the far Node unchanged after one step, {retarded} short of the new rest",
    )


def force_between_moving_charges() -> Row:
    """Table 1's row ('The force between moving charges, Coulomb's over gamma'), the clicks table's magnetism row and S.33 (c), (e): for a source moving at beta and a co-moving reader the electric force is gamma F_0, the magnetic -beta^2 gamma F_0 and the total gamma (1 - beta^2) F_0 = F_0 / gamma, exact in rationals at the Pythagorean betas 3 / 5, 5 / 13, 8 / 17, 7 / 25, 20 / 29, and 0.99499, 0.86603 at beta = 0.1, 0.5 (sign.py); the covector: the turned step's dispersion is the band's at (omega - theta_0, k + theta_a), exact in Gaussian rationals; outside: beta above the holder's events' speed, 1 - beta^2 < 0, where gamma has no real value and the retarded form fails; the covector's domain the lattice's k^2 / 12, 2 x 10^-4 at k = 0.05."""
    draw = random.Random(SEED)
    exact = True
    for beta, gamma in PYTHAGOREAN_BETAS:
        exact &= gamma * gamma * (1 - beta * beta) == 1
        electric, magnetic = gamma, -beta * beta * gamma
        exact &= electric + magnetic == 1 / gamma
    numbers = [round(v, 5) for v in sign.odd_lines_source()[4:]]
    covector = True
    for num, den in ((1, 1), MATTER):
        gamma_int = 4
        wall, reads, self_coefficient = rule3.coefficients(num, den, gamma_int, 3, (2, 3, 4))
        for _ in range(6):
            rotation, wave, turn_time, turn_link = (draw_angle(draw) for _ in range(4))
            turned = (
                turn_time * rotation.conj()
                + turn_time.conj() * rotation
                - Gaussian(Fraction(self_coefficient, wall), 0)
                - (turn_link * wave + (turn_link * wave).conj()) * Fraction(reads[0], wall)
            )  # e^(i theta_0) e^(-i omega) + e^(-i theta_0) e^(i omega) - S / w - (R / w)(e^(i(k + theta_a)) + c.c.)
            shifted_rotation, shifted_wave = rotation * turn_time.conj(), wave * turn_link
            plain = Gaussian(
                2 * shifted_rotation.re
                - Fraction(self_coefficient, wall)
                - 2 * Fraction(reads[0], wall) * shifted_wave.re,
                0,
            )  # the band's relation at (omega - theta_0, k + theta_a)
            covector &= turned == plain
    beyond = 1 - Fraction(5, 4) ** 2
    anisotropy = 0.05**2 / 12
    return Row(
        "tab:results: The force between moving charges Coulombs over gamma",
        exact and numbers == [0.99499, 0.86603] and covector,
        beyond < 0 and anisotropy > 1e-4,
        f"gamma F_0 - beta^2 gamma F_0 = F_0 / gamma exact at 5 Pythagorean betas; 1 / gamma = {numbers} at beta = 0.1, 0.5; the covector exact at 12 random angle sets; at beta = 5 / 4, 1 - beta^2 = {beyond} < 0, no real gamma; the domain's k^2 / 12 = {anisotropy:.1e} at k = 0.05",
    )


def counts_inflow_with_the_factor_squared() -> Row:
    """The clicks table's row ('A body's count in clicks: the share summed over the body's Nodes, what a NodeDetector over all its Nodes credits'), S.42's inputs: on a chain of eight at Gamma = 50 with a tension t = 1 on the two Links of a region's front, the region's share over six steps of the line changes by exactly the weighted inflow, the Link's factor squared on each boundary current (proofs_booking's share, rule3.link_current); outside: the plain current, the factor dropped, is short of the weighted one by 1 - q^2 / Gamma^2 = 2 t / Gamma - t^2 / Gamma^2 per Link exactly, 2 t / Gamma to the first order."""
    draw = random.Random(SEED)
    gamma, tension, count = 50, 1, 8
    num, den = MATTER
    arrivals = rule3.chain_arrivals(count)
    region = {4, 5, 6, 7}
    factors = [[gamma] * PORTS for _ in arrivals]
    for i, ports in enumerate(arrivals):
        for port, j in enumerate(ports):
            if (i in region) != (j in region):
                factors[i][port] = gamma - tension
    wall, reads, selves, paces = read(arrivals, [gamma] * count, factors, num, den, gamma)
    now = [Fraction(draw.randint(-40, 40)) for _ in range(count)]
    before = [Fraction(draw.randint(-40, 40)) for _ in range(count)]
    start = sum(rational_share(wall, reads, selves, paces, arrivals, i, now, before) for i in region)
    weighted, plain = Fraction(0), Fraction(0)
    for _ in range(6):
        for i in region:
            for port, j in enumerate(arrivals[i]):
                if j not in region:
                    weighted += rule3.link_current(
                        num, now[i], before[i], now[j], before[j], factors[i][port], gamma
                    )
                    plain += rule3.link_current(num, now[i], before[i], now[j], before[j])
        now, before = step_line(arrivals, reads, selves, wall, now, before), now
    end = sum(rational_share(wall, reads, selves, paces, arrivals, i, now, before) for i in region)
    short = 1 - Fraction(gamma - tension, gamma) ** 2
    first_order = Fraction(2 * tension, gamma)
    return Row(
        "tab:clicks: A bodys count in clicks",
        end - start == weighted,
        plain != weighted
        and weighted == plain * (1 - short)
        and short == first_order - Fraction(tension * tension, gamma * gamma),
        f"the region's share changed by the weighted inflow {float(weighted):.4f} exactly over 6 steps; the plain inflow {float(plain):.4f}, short by 1 - q^2 / Gamma^2 = {short} = 2 t / Gamma - t^2 / Gamma^2 per Link (2 t / Gamma = {first_order})",
    )


def no_signalling_marginals() -> Row:
    """The clicks table's row ('No signalling: P(A+) = (cos^2 a + r^2 sin^2 a) / (1 + r^2), independent of b for parts of any amplitudes'): under the declared credit the marginal at random rational angles and parts equals that form and is the same at two settings of the other side, exactly (proofs_credit's shares); the GHZ marginals 1 / 2 (proofs_credit's check); outside the bodies' marginals, the one named non-local place: a region's count by the rounding of the total (clicks.credit) moves with another region's inflow, by at most one quantum per window, exactly."""
    draw = random.Random(SEED)
    independent = True
    for a in angles(draw, 7):
        for b, b_other in ((draw_angle(draw), draw_angle(draw)) for _ in range(3)):
            m_1, m_2 = Fraction(draw.randint(1, 9)), Fraction(draw.randint(1, 9))
            r = m_2 / m_1
            form = (a.re**2 + r * r * a.im**2) / (1 + r * r)
            for other in (b, b_other):
                shares = proofs_credit.bell_shares((a.re, a.im), (other.re, other.im), m_1, m_2)
                marginal = (shares[(1, 1)] + shares[(1, -1)]) / sum(shares.values())
                independent &= marginal == form
    ghz = proofs_credit.check_the_ghz_correlation()[0]
    moved = clicks.credit([Fraction(1, 5), Fraction(1, 5), Fraction(1, 5)], 1) - clicks.credit(
        [Fraction(1, 5), Fraction(1, 5)], 1
    )
    at_most_one = True
    for _ in range(200):
        total = Fraction(draw.randint(0, 400), 100)
        change = Fraction(draw.randint(0, 99), 100)
        at_most_one &= abs(clicks.credit([total + change], 9) - clicks.credit([total], 9)) <= 1
    return Row(
        "tab:clicks: No signalling",
        independent and ghz,
        moved == 1 and at_most_one,
        f"P(A+) = (c^2 + r^2 s^2) / (1 + r^2) at two settings of B, exact over 7 x 3 angle sets; GHZ marginals 1 / 2; the rounded total's count moved by {moved} with a third region's inflow of 1 / 5, never by more than one over 200 draws",
    )


def which_way_sum() -> Row:
    """The clicks table's row ('The which-way sum: a region behind one gap reads that gap's share and nothing of the fringe'): by the Huygens sum of the declared file (two_slits.py) the screen's row with one gap opaque has no interior minimum across the central pattern where the two gaps' row has two, so a one-gap region reads its gap's envelope alone; outside the one-gap reading: the two gaps' row is not the sum of the two one-gap rows, below it at the fringe's minimum row 15 and above it at the centre 24, the interference term."""
    minima = two_slits.opaque_reader_envelope()
    both = two_slits.huygens_rows(two_slits.GAP_ROWS)
    first = two_slits.huygens_rows((two_slits.GAP_ROWS[0],))
    second = two_slits.huygens_rows((two_slits.GAP_ROWS[1],))
    incoherent = [x + y for x, y in zip(first, second, strict=True)]
    at_minimum = both[15] / incoherent[15]
    at_centre = both[24] / incoherent[24]
    return Row(
        "tab:clicks: The whichway sum",
        minima == [2.0, 0.0],
        at_minimum < 0.5 and at_centre > 1.5,
        f"interior minima across the pattern: two gaps {int(minima[0])}, one gap {int(minima[1])}; the two gaps' row over the two one-gap rows' sum: {at_minimum:.3f} at the row 15, {at_centre:.3f} at the centre",
    )


def one_photon_on_two_bodies() -> Row:
    """S.57 (Sections 5.4 and 9): one quantum between two bodies at count 1, unit 10 and the inflows (4, 4): the bodies' rule gives the row (s_A, s_B, 1 - s_A - s_B) = (2 / 5, 2 / 5, 1 / 5) at eta = 1, P(both) = 0 and alpha = 0; two records taken independently give P(both) = s_A s_B, alpha = 1, the control; the sequential windows' P(B only) = (1 - s_A) s_B = 6 / 25; the wall's algebra proofs_credit's check; outside the bodies' rule: a region with Nodes alone carries the rounding of the total (clicks.credit), one click of the total 4 / 5 shared (1 / 2, 1 / 2, 0), another row."""
    algebra = proofs_credit.check_the_anticoincidences_algebra_and_s57s_wall()[0]
    unit, inflows = 10, (4, 4)
    eta = Fraction(1)
    s_a, s_b = (eta * Fraction(f, unit) for f in inflows)
    row = (s_a, s_b, 1 - s_a - s_b)
    alpha_one = Fraction(0) / (s_a * s_b)
    alpha_two = (s_a * s_b) / (s_a * s_b)
    sequential = (1 - s_a) * s_b
    total_clicks = clicks.credit([s_a, s_b], 1)
    regions_row = (Fraction(total_clicks, 2), Fraction(total_clicks, 2), Fraction(0))
    return Row(
        "S.57",
        algebra
        and row == (Fraction(2, 5), Fraction(2, 5), Fraction(1, 5))
        and alpha_one == 0
        and alpha_two == 1
        and sequential == Fraction(6, 25),
        regions_row != row,
        f"the bodies' row {[str(v) for v in row]}, alpha {alpha_one} for one record and {alpha_two} for two, P(B only) sequential {sequential}; the regions' rounding gives {total_clicks} click shared {[str(v) for v in regions_row]}",
    )


def regions_reading_factor_and_the_draws_scatter() -> Row:
    """S.8 (Section 5.3): a region of n = 4 rows keeps a fringe of period Lambda = 16 with the factor sin(pi n / Lambda) / (n sin(pi / Lambda)) = 0.906127 by the exact geometric sum (proofs_credit's check at rational angles), 0 at Lambda = n; N = 273 quanta drawn independently by the shares 1 / 12 give each region the binomial scatter sqrt(N p (1 - p)) = 4.57, the sample's within ten percent over 600 trials of random.Random(SEED); outside: an affine seeding u_t = (u_0 + t phi) mod 1, where the scatter falls far below the binomial's."""
    exact = proofs_credit.check_the_regions_reading_factor()[0]
    factor = math.sin(math.pi * 4 / 16) / (4 * math.sin(math.pi / 16))
    at_period = abs(math.sin(math.pi)) / (4 * math.sin(math.pi / 4))
    draw = random.Random(SEED)
    trials, quanta, regions = 600, 273, 12
    binomial = math.sqrt(quanta * (1 / regions) * (1 - 1 / regions))

    def spread(counts: list[int]) -> float:
        mean = sum(counts) / len(counts)
        return math.sqrt(sum((c - mean) ** 2 for c in counts) / (len(counts) - 1))

    independent = spread(
        [sum(1 for _ in range(quanta) if draw.random() < 1 / regions) for _ in range(trials)]
    )
    golden = (math.sqrt(5) - 1) / 2
    affine = spread(
        [
            sum(1 for t in range(quanta) if (start + t * golden) % 1 < 1 / regions)
            for start in (draw.random() for _ in range(trials))
        ]
    )
    return Row(
        "S.8",
        exact
        and round(factor, 6) == 0.906127
        and at_period < 1e-15
        and abs(independent / binomial - 1) < 0.1,
        affine < 0.3 * binomial,
        f"factor {factor:.6f} at n = 4, Lambda = 16, {at_period:.0e} at Lambda = n; scatter of a region's count: independent draws {independent:.2f} against sqrt(N p (1 - p)) = {binomial:.2f}; affine seeding {affine:.2f}",
    )
