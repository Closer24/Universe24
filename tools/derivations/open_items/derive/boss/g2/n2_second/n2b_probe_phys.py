"""N2's second text, the physicist's seven items, measured on the engine's act (step.tick where the metric stands
still, the first-order form where it moves).

Clock: a held hand's beat and light's standing wave, each counted in rounds at several depths of the 00 slot and
several ii slots; the matter's stress read from the strides.
Algebra: whole numbers only: counts of sign changes, sums of squares, Rule3's carry.
Board: one Node-clock, a ring of 6 along z, a line of 96 along z (the sides of 1 wrap each site onto itself).
Clicks: the beat and the wave's period are what the clicks will read as proper time and as light's speed.

Run: <t24b>/.venv/bin/python -I n2b_probe_phys.py; the output is n2b_results_phys.txt.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
from n2b_lib import (  # noqa: E402
    A1ROWS,
    FAMILIES,
    ROWS,
    S0I,
    S00,
    SII,
    SJK,
    T1ROWS,
    Carry,
    State,
    carry,
    engine_plan,
    eye_family,
    gradient_part,
    join,
    layout,
    metric_source,
    potential,
    product_rate_part,
    rate_part,
    spring,
    step,
    table,
    terms,
)

OUT = []


def say(*xs):
    line = " ".join(str(x) for x in xs)
    print(line, flush=True)
    OUT.append(line)


REST, GRIP = 3000, 500  # the loader's ratio: the teeth at rest 6 den Gamma^2, the grip den Gamma^2
G = 210  # the clock's spring
LIGHT, CLOCK = T1ROWS[0], A1ROWS[0]  # light: a row with no spring; the clock: the A1 row with its spring
SPRING = terms(spring(G, [(A1ROWS, table("A1"))]))


def mode6(n, amplitude):
    """The standing wave of six sites along z as whole numbers: a(z + 1) = a(z) - a(z - 1) from (2, 1), the
    recurrence of cos(pi z / 3) doubled; no cosine."""
    seq = [2 * amplitude, amplitude]
    while len(seq) < n:
        seq.append(seq[-1] - seq[-2])
    return np.array(seq[:n], dtype=object)


def still(L_, rows_values, metric_values):
    """A state at rest (a = b, every tooth 0): rows laid with their profiles, metric slots laid uniform."""
    n = L_.nb.shape[1]
    a = np.zeros((ROWS, n), dtype=object)
    for row, values in rows_values.items():
        a[row] = values
    for slot, value in metric_values.items():
        a[slot] = value
    return State(a, a.copy(), 0 * a, 0 * a)


def crossings(L_, s_, plan, row, site, wanted):
    """The rounds the engine's own act takes for a gear's count to change sign `wanted` times (the metric standing)."""
    L_ = L_._replace(plan=engine_plan(plan))
    rounds, count, sign = 0, 0, None
    while count < wanted:
        s_ = step.tick(L_, s_)
        rounds += 1
        v = int(s_.a[row, site])
        if v != 0:
            new = 1 if v > 0 else -1
            if sign is not None and new != sign:
                count += 1
            sign = new
        if rounds > 200000:
            return None
    return rounds


def ratio_squared(t1, t0):
    """(t1 / t0)^2 as a whole-number permille, by one carry."""
    q, _ = carry(1000 * t1 * t1, t0 * t0, 0)
    return int(q)


# ------------------------------------------------------------------------------ P1. the beat goes as W^(-1/2)
say("== P1. the beat and light's period against the teeth W (the engine's act, the metric standing)")
L6 = layout((1, 1, 6), REST, REST, GRIP, 1, 1, clock="others")
N = 40
base_clock = base_light = None
for c00 in (0, REST, 3 * REST, 7 * REST):
    s_clock = still(L6, {CLOCK: 10**6}, {S00: c00})
    s_light = still(L6, {LIGHT: mode6(6, 10**6)}, {S00: c00})
    tc = crossings(L6, s_clock, SPRING, CLOCK, 0, N)
    tl = crossings(L6, s_light, SPRING, LIGHT, 0, N)
    if c00 == 0:
        base_clock, base_light = tc, tl
    w = REST + c00
    say(
        f"  W = {w} = {w // REST} rest: the clock's {N} sign changes take {tc} rounds (period^2 against rest: {ratio_squared(tc, base_clock)} permille), light's standing wave of six Meshes {tl} rounds ({ratio_squared(tl, base_light)} permille); W / rest = {1000 * w // REST} permille"
    )
say("  so period^2 goes as W for the beat and for light alike: the rate N = sqrt(rest / W), N^2 = rest / W; a rate read as 1 / W would double the redshift")

# ------------------------------------------------------------------------------ P2. the grips and gamma
say("\n== P2. light against the clock at one depth, with the ii slots lowered, 0 and raised (gamma)")
c00 = 600  # W = 3600, W / rest = 6 / 5
N = 60
t_clock0 = crossings(L6, still(L6, {CLOCK: 10**6}, {}), SPRING, CLOCK, 0, N)
t_light0 = crossings(L6, still(L6, {LIGHT: mode6(6, 10**6)}, {}), SPRING, LIGHT, 0, N)
say(f"  at rest: the clock {t_clock0} rounds, light {t_light0} rounds for {N} sign changes")
for ii, name in ((-50, "-c00 / 12, the grip lowered to 400"), (0, "0, the grip at rest 500"), (50, "+c00 / 12, the grip raised to 600")):
    metric = {S00: c00, SII[0]: ii, SII[1]: ii, SII[2]: ii}
    tc = crossings(L6, still(L6, {CLOCK: 10**6}, metric), SPRING, CLOCK, 0, N)
    tl = crossings(L6, still(L6, {LIGHT: mode6(6, 10**6)}, metric), SPRING, LIGHT, 0, N)
    say(
        f"  c00 = {c00}, each ii slot {name}: the clock {tc} rounds (period^2 ratio {ratio_squared(tc, t_clock0)} permille; W / rest = 1200), light {tl} rounds ({ratio_squared(tl, t_light0)} permille; (W / rest) (grip_rest / grip) = {1000 * 3600 * 500 // (3000 * (500 + 2 * ii))})"
    )
say("  light's slowing over the clock's, (1 + gamma): the lowered grip gives about 2 (gamma = 1), the rest grip 1 (gamma = 0), the raised grip about 0 (gamma = -1)")

# ------------------------------------------------------------------------------ P3. the sum form and the virial identity
say("\n== P3. the 00 slot's two forms against the act's own virial identity (one Node-clock, the clock's swing)")
L1 = layout((1, 1, 1), REST, REST, GRIP, 1, 1, clock="others")._replace(plan=engine_plan(SPRING))
A = 10**5
s_ = still(L1, {CLOCK: A}, {})
sums = {"sa2": 0, "sb2": 0, "sbsa": 0, "a2": 0, "j00": 0}
T = 2000
W = REST
prev = int(s_.a[CLOCK, 0] - s_.b[CLOCK, 0])
energy0 = None
for _ in range(T):
    a0 = int(s_.a[CLOCK, 0])
    s_ = step.tick(L1, s_)
    sa = int(s_.a[CLOCK, 0]) - a0
    sb = prev
    if energy0 is None:
        energy0 = W * sa * sa + G * a0 * int(s_.a[CLOCK, 0])  # 2E, the act's own energy: W sigma^2 + g a a+
    sums["sa2"] += sa * sa
    sums["sb2"] += sb * sb
    sums["sbsa"] += sb * sa
    sums["a2"] += a0 * a0
    sums["j00"] += W * (sb * sb + sa * sa) - G * a0 * a0  # 4K - 2V in the act's energy units (2V = g a^2)
    prev = sa
lhs_sum = W * (sums["sb2"] + sums["sa2"])
rhs = 2 * G * sums["a2"]
lhs_prod = 2 * W * W * sums["sbsa"]
rhs_prod = G * (2 * W - G) * sums["a2"]
say(f"  {T} rounds of the swing at W = {W}, g = {G}: sum sigma_a^2 = {sums['sa2']}, sum sigma_b sigma_a = {sums['sbsa']}, sum a^2 = {sums['a2']}")
say(f"  the sum form:     W sum (sigma_b^2 + sigma_a^2) = {lhs_sum} against 2 g sum a^2 = {rhs}: ratio {carry(1000000 * lhs_sum, rhs, 0)[0]} per million")
say(f"  the product form: 2 W^2 sum sigma_b sigma_a = {lhs_prod} against g (2W - g) sum a^2 = {rhs_prod}: ratio {carry(1000000 * lhs_prod, rhs_prod, 0)[0]} per million; against 2 W g sum a^2: {carry(1000000 * lhs_prod, 2 * W * rhs // 2, 0)[0]} per million")
say(f"  so the sum form's mean is 2 E / W with E the swing's energy (the virial identity W sum sigma_a^2 = g sum a^2 up to the carries), the product form's is short by g / 2W = {G} / {2 * W}")
say(f"  the 00 push in the act's energy units, W (sigma_b^2 + sigma_a^2) - g a^2 = 4K - 2V = rho + 3 pr: summed over the {T} rounds {sums['j00']}, against {T} times the swing's energy E (2E = W sigma^2 + g a a+ at the start = {energy0}): ratio {carry(1000000 * sums['j00'] * 2, T * energy0, 0)[0]} per million: the active mass of a bound swing is its energy, and the potential's strength over the kinetic's is g / W, the act's own")

# ------------------------------------------------------------------------------ P4. a travelling wave: null dust
say("\n== P4. a travelling wave (null dust) and the normalization of the slots")
NZ = 96
L96 = layout((1, 1, NZ), REST, REST, GRIP, 1, 1, clock="others")
z = np.arange(NZ)
u = z - 48
bump = np.where(abs(u) < 8, (64 - u * u) ** 2, 0).astype(object)
s_ = still(L96, {LIGHT: bump}, {})
L96e = L96._replace(plan=engine_plan(terms([])))
for _ in range(60):
    s_ = step.tick(L96e, s_)
T5 = join(terms(gradient_part(1)), terms(potential(0)))
RATE = terms(rate_part(1))
j = metric_source(L96, s_, T5, RATE)
right, left = z >= 48, z < 48
s00r, s0zr, szzr = int(j[S00][right].sum()), int(j[S0I[2]][right].sum()), int(j[SII[2]][right].sum())
s00l, s0zl, szzl = int(j[S00][left].sum()), int(j[S0I[2]][left].sum()), int(j[SII[2]][left].sum())
others = [int(j[x].sum()) for x in (SII[0], SII[1], S0I[0], S0I[1], *SJK)]
say(f"  a bump at rest split into two pulses after 60 rounds (c^2 = grip / W = 1 / 6): the pulse moving +z has sums S00 = {s00r}, S0z = {s0zr}, Szz = {szzr}; the one moving -z: {s00l}, {s0zl}, {szzl}; every other slot {others}")
say(f"  the null condition S0z^2 = S00 Szz: +z pulse {s0zr * s0zr} against {s00r * szzr} ({carry(1000 * s0zr * s0zr, s00r * szzr, 0)[0]} permille); the sign of S0z follows the direction")
say(f"  the normalization: Szz / S00 = 4 / c^2 = 24 in the continuum; measured {carry(10 * szzr, s00r, 0)[0]} / 10 (+z) and {carry(10 * szzl, s00l, 0)[0]} / 10 (-z); -S0z / S00 = 2 / c = 4.9: measured {carry(-10 * s0zr, s00r, 0)[0]} / 10")
say("  so J00 = Jzz = -J0z needs the strengths 1 : c / 2 : c^2 / 4 on (sigma sigma) : (sigma D) : (D D), c^2 = grip / W = 1 / 6 at the loader's rest: the ii slots' 1 / 24 is whole, the 0i slots' c / 2 is a root (OPEN at G4)")
# the T1 family's source is three scalars'
seq = Carry(5)
L3 = layout((3, 3, 3), REST, REST, GRIP, 1, 1, clock="none")
n3 = L3.nb.shape[1]
a = np.zeros((ROWS, n3), dtype=object)
b = np.zeros((ROWS, n3), dtype=object)
for row in T1ROWS:
    a[row] = seq.draw(-30, 31, (n3,))
    b[row] = a[row] - seq.draw(-6, 7, (n3,))
st = State(a, b, 0 * a, 0 * a)
plan_t1 = join(terms(gradient_part(1, [(T1ROWS, table("T1"))])), terms(rate_part(1, families=[(T1ROWS, table("T1"))])))
j_t1 = metric_source(L3, st, plan_t1, terms([]))
j_sum = 0 * j_t1
for row in T1ROWS:
    fam = [eye_family([row])]
    j_sum = j_sum + metric_source(L3, st, join(terms(gradient_part(1, fam)), terms(rate_part(1, families=fam))), terms([]))
say(f"  the T1 family's S through C[T1 x T1 -> A1] equals the sum of its three rows' S each as a scalar: {bool((j_t1 == j_sum).all())} (three scalars', not Maxwell's)")
# von Laue on this board: a massive standing wave's ii slots do not sum to 0
s_ = still(L6, {CLOCK: mode6(6, 10**4)}, {})
L6e = L6._replace(plan=engine_plan(SPRING))
acc = [0, 0, 0, 0]
T = 2000
for _ in range(T):
    j = metric_source(L6, s_, join(terms(gradient_part(1)), terms(potential(1))), RATE)
    for k, x in enumerate((S00, *SII)):
        acc[k] += int(j[x].sum())
    s_ = step.tick(L6e, s_)
say(f"  a massive standing wave (the clock's spring, six Meshes) over {T} rounds: the board sums of J00, Jxx, Jyy, Jzz accumulate to {acc}: sum J_ii is not 0, the wave presses on the wrap, so this board holds no von Laue lump (OPEN: a lump bound by its own forces, G3)")

# ------------------------------------------------------------------------------ P5. the clock-rate wave
say("\n== P5. the 00 slot's own wave")
N = 40
s_ = still(L6, {}, {})
s_.a[S00] = mode6(6, 10**3)
s_.b[S00] = s_.a[S00].copy()
t00 = crossings(L6, s_, SPRING, S00, 0, N)
say(f"  a standing wave of the 00 slot alone, six Meshes, the 00 row's teeth at rest: {N} sign changes in {t00} rounds, light's at rest {base_light}: the clock-rate wave runs at light's speed, c^2 = grip / rest")
say("  its own stride sources nothing (hypothesis (d) of M1): the harmonic h00 wave carries no energy here either")

# ------------------------------------------------------------------------------ P6. a split wave keeps pushing
say("\n== P6. Page and Geilker: a wave in two shares pushes the 00 slot at both")
u1, u2 = z - 20, z - 70
two = (np.where(abs(u1) < 8, (64 - u1 * u1) ** 2, 0) + np.where(abs(u2) < 8, (64 - u2 * u2) ** 2, 0)).astype(object)
s_ = still(L96, {CLOCK: two}, {})
L96s = L96._replace(plan=engine_plan(SPRING))
for _ in range(10):
    s_ = step.tick(L96s, s_)
j = metric_source(L96, s_, join(terms(gradient_part(1)), terms(potential(1))), RATE)
near1, near2 = abs(u1) < 10, abs(u2) < 10
say(f"  two lumps of one A1 train swinging on its spring, after 10 rounds: J00 summed near z = 20: {int(j[S00][near1].sum())}, near z = 70: {int(j[S00][near2].sum())}, elsewhere: {int(j[S00][~(near1 | near2)].sum())}")
say("  the act reads both shares, and no click writes into a, p or r_d (term 11), so after a split both shares keep pushing: OPEN, what it needs is named in the text")

Path(__file__).resolve().parent.joinpath("n2b_results_phys.txt").write_text("\n".join(OUT) + "\n", encoding="utf-8")
