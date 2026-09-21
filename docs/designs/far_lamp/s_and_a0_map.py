"""The width S and the acceleration floor, the arithmetic (read-only, the mathematician,
2026-09-21; docs/designs/far_lamp/S_AND_A0.md): (A) the candidates for a width S
derived from the structure (DERIVATIONS_BEAM.md 16.2 (e) and (f), and the budget
tied to the growing wall of section 15), what each gives for G in the law's units
and what refutes it; (B) whether the push's Euclidean divisions leave an
acceleration floor (they keep the remainder: the mean is exact, the floor is
zero), the shape a discarding floor would give against the radial acceleration
relation, the fan's angular grain as the one discreteness of the far field, and
the law's granular push against c H. No run; no fit.

Run from the repository root:

    python docs/designs/far_lamp/s_and_a0_map.py > docs/designs/far_lamp/s_and_a0_map.out
"""

from __future__ import annotations

import math

# The register's integers (section 15's stream; the nucleus fan; the reading's cost).
K_FAN = 290  # the 290 fan, F_6
N_OVER_D = 1.0  # the release rate per unit of content per direction, the register's [1, 1]
H_NUM, H_DEN = 1, 400  # expansion-v1's declared H, 1 / 400 per interval
READ_COST = 26  # operations per row read (13.1)
C_LAW = 1 / math.sqrt(3)  # Links per interval

# Nature's numbers, one source each (S_AND_A0.md section 0).
A0_NATURE = 1.2e-10  # m s^-2, Milgrom 1983; McGaugh, Lelli and Schombert 2016
C_SI = 299_792_458.0
H0_SI = 70e3 / 3.0857e22  # 70 km/s/Mpc in s^-1
YEAR = 3.156e7
GDOT_LLR = 7.6e-14  # per year, the one-sigma bound of Hofmann and Muller 2018 (16.2 (f))

print(
    "A. THE WIDTH S: THE CANDIDATES, WHAT EACH GIVES FOR G = K_fan (n / d) / (4 pi S), WHAT REFUTES IT"
)
print(
    f"   K_fan = {K_FAN}, n / d = {N_OVER_D:.0f}, H = {H_NUM} / {H_DEN} per interval; G in Links^3 per unit of content per interval^2"
)
hubble_links = C_LAW * H_DEN / H_NUM
hubble_nodes = 4 / 3 * math.pi * hubble_links**3
candidates = [
    (
        "16.2 (e) first: S = K (n / d) / (4 pi), G = 1 (natural units)",
        K_FAN * N_OVER_D / (4 * math.pi),
        "a choice of units: moves the number into h; alpha / alpha_G still rho_p^2, declared",
    ),
    (
        "16.2 (e) second: S = sqrt 3 K (n / d) / (2 h), the unit the Planck mass",
        math.sqrt(3) * K_FAN * N_OVER_D / 2,
        "refuted: alpha_G = M_p^2 >= 1 against 5.9 x 10^-39 (16.2 (e))",
    ),
    (
        "16.2 (f): S = K_budget / 26, the budget unfixed",
        float("nan"),
        "derived under two assumptions; K_budget not fixed without hbar_law: no number",
    ),
    (
        "the budget as the declared H: K_budget = H_den / H_num",
        H_DEN / H_NUM / READ_COST,
        "moves the input from S to H; constant in time (H declared); nothing measured ties G to the declared H",
    ),
    (
        "the budget as the Hubble length in Links: K_budget = c_0 / H",
        hubble_links / READ_COST,
        "the same, and refuted if H is the running rate: G ~ H, Gdot / G = -H",
    ),
    (
        "the budget as the Nodes within the Hubble length: K_budget = (4 pi / 3)(c_0 / H)^3",
        hubble_nodes / READ_COST,
        "the same, and refuted if H is the running rate: G ~ H^3, Gdot / G = -3 H",
    ),
]
for name, s_value, verdict in candidates:
    if math.isnan(s_value):
        print(f"   {name:78s} S = (unfixed)      G = (unfixed)   {verdict}")
    else:
        g_value = K_FAN * N_OVER_D / (4 * math.pi * s_value)
        print(f"   {name:78s} S = {s_value:12.3f}  G = {g_value:9.3e}   {verdict}")
print()
print(
    "   the running rate under expansion-v1: a = 1 + H t gives the physical Hubble rate H / (1 + H t), falling as 1 / t under Milne;"
)
h0_per_year = H0_SI * YEAR
for factor, name in ((1, "G ~ H"), (3, "G ~ H^3")):
    print(
        f"   {name}: Gdot / G = -{factor} H_0 = -{factor * h0_per_year:.1e} per year against lunar laser ranging's {GDOT_LLR:.1e} per year (one sigma): refuted by a factor {factor * h0_per_year / GDOT_LLR:.0f}"
    )
print(
    "   the hierarchy alpha / alpha_G = rho_p^2 (3.4, 16.4) is untouched by every candidate: S sets the unit of G, the declared charge per unit of content carries the 10^36;"
)
print(
    "   what would make S = f(H) more than a relabelling: a rule driving the wall's rate H by the content (a Friedmann relation, 3 H^2 = 8 pi G rho), which the six verbs do not have; the wall's H is declared and the content does not move it"
)
print()

print("B. THE PUSH'S EUCLIDEAN DIVISIONS: IS THERE AN ACCELERATION FLOOR?")
print(
    "   (i) the push per column on main is by_clock(age, abs(V E n), D d): the whole part of the CUMULATIVE age x X / d, delivered as it crosses each integer;"
)
print(
    "       on gravity the divisor is 1 (3.5 item 7) and the push is exact per interval; on the branch acc_push keeps the remainder. A weak field on integers:"
)


def cumulative_floor(x_num: int, x_den: int, intervals: int) -> int:
    """The main form: the push delivered by the age is floor(age x X / d) - floor((age - 1) x X / d); its sum over the ages."""
    total, previous = 0, 0
    for age in range(1, intervals + 1):
        now = age * x_num // x_den
        total += now - previous
        previous = now
    return total


def discarding_floor(x_num: int, x_den: int, intervals: int) -> int:
    """A rule the law does not have: floor(X / d) per interval, the remainder dropped."""
    return intervals * (x_num // x_den)


for x_num, x_den in ((1, 1000), (1, 7), (3, 5)):
    n = 100_000
    exact = n * x_num / x_den
    print(
        f"       X / d = {x_num} / {x_den} per interval over {n} intervals: the cumulative form delivers {cumulative_floor(x_num, x_den, n)} (exact {exact:.0f}), a discarding floor would deliver {discarding_floor(x_num, x_den, n)}"
    )
print(
    "       the law's form loses nothing in the mean: the floor is zero, the granularity a delay of at most one push unit. A discarding floor is a remainder dropped, not one of the six (section 1's inventory)."
)
print()
print(
    "   (ii) the shape a discarding floor would give, against the radial acceleration relation (the pin): a body at r from a source, Newton's a_N = G M / r^2 in push units;"
)
print(
    "        the floor: below half a unit nothing, at or above it one whole unit (a band); MOND's deep law a = sqrt(a_N a_0), the RAR's g_obs = g_bar / (1 - exp(-sqrt(g_bar / a_0)))"
)
a0 = 1.0  # the unit of the push, taken as the floor's scale
gm = 100.0  # G M in push units x Links^2, so a_N = 100 / r^2: the unit is reached at r = 10
print("        r (Links) | a_N / a_0 | the floor's a | MOND's a | the floor's v^2 = r a | MOND's v^2")
for r in (2, 5, 10, 14, 20, 50, 100):
    a_n = gm / r**2
    a_floor = float(math.floor(a_n + 0.5)) if a_n < 1 else a_n
    a_mond = a_n / (1 - math.exp(-math.sqrt(a_n / a0)))
    print(
        f"        {r:9d} | {a_n:9.4f} | {a_floor:13.4f} | {a_mond:8.4f} | {r * a_floor:21.3f} | {r * a_mond:10.3f}"
    )
print(
    "        the floor's v^2 rises as r up to the radius where a_N falls below half a unit and is zero beyond: a band, never a flat curve (MOND's v^2 -> sqrt(G M a_0), constant);"
)
print(
    "        and the floor cuts the weak field where MOND raises it: the wrong sign of the departure before any number. The deep law is a root of the state, not one of the six (the vector test, record 202)."
)
print()
print(
    "   (iii) the one discreteness of the far field the law does have: the fan's angular grain (3.2, 3.5 item 1, 15.5): a lone body reads a lone source only on one of its K lines;"
)
print("         the fraction of a shell's Nodes on a line, K / N(r), N(r) -> 4 pi r^2:")
for r in (10, 100, 1000, 10000):
    for k in (290, 1423):
        print(
            f"         r = {r:5d} Links, K = {k:4d}: {min(1.0, k / (4 * math.pi * r * r)):.2e} of the shell's Nodes read the source, the rest read 0; the shell mean is Newton's (Gauss exact)"
        )
print(
    "         off the lines the far field is weaker than Newton's, never stronger: the departure has the wrong sign for a flat curve; a crowd of sources at many angles fills the lines (the shell mean per Node)"
)
print()
print(
    "   (iv) the granular push against c H: one row of amount 1 per interval at a body gives a = 1 / S Links per interval^2 (3.3: a = push / (Q S M), push = M x u_d, u_d = Q); c H = H / sqrt 3;"
)
print(
    "        a_unit / (c H) = sqrt 3 H_den / (S H_num), dimensionless; nature's a_0 / (c H_0) = 1 / (2 pi) = 0.159 (Milgrom's coincidence):"
)
for s_value in (1, 8, 32, 512, 4353, 45120, 2**20, 2**28):
    ratio = math.sqrt(3) * H_DEN / (s_value * H_NUM)
    print(f"        S = {s_value:9d}: a_unit / (c H) = {ratio:.3e}")
print(
    f"        the S at which the granular push equals nature's a_0 at H = 1 / 400: {math.sqrt(3) * H_DEN * 2 * math.pi:.0f}, a number no count of the structure carries (13.3: the widths sit at several budgets);"
)
for name, s_value in (
    ("K_budget = H_den / H_num", H_DEN / H_NUM / READ_COST),
    ("K_budget = c_0 / H in Links", hubble_links / READ_COST),
):
    print(
        f"        under S = K_budget / 26 with {name}: a_unit / (c H) = {math.sqrt(3) * H_DEN / (s_value * H_NUM):.1f}, against 0.159; and the floor is zero whatever S"
    )
print(
    f"        in m / s^2: not computable, the dictionary's Link and interval are not fixed (16.2 (f), NATURE.md 'What needs the conversion'); c H_0 = {C_SI * H0_SI:.2e} m s^-2, c H_0 / (2 pi) = {C_SI * H0_SI / (2 * math.pi):.2e} against a_0 = {A0_NATURE:.1e}"
)
print()
print(
    "   (v) the register's small-r departures (series C item 5: count x r / q within 10 percent for r >= 8, the ring mean over mostly empty Nodes, one ray or none):"
)
print(
    "        the lattice's shell count N(r) and the fan's grain (3.2's table, r / N(r) exact), not a floor: the number that pins it is the ring reading r / N(r), 0.125 at r = 4, and it is Newton's"
)
print()
print(
    "C. THE VERDICTS: (A) none derives S: the two of 16.2 (e) are a unit choice and a refuted one, the budget form leaves K_budget unfixed, and a budget tied to H moves the input (constant H) or is refuted by lunar laser ranging (running H);"
)
print(
    "   (B) REFUTED: the push's divisions keep the remainder (the floor is zero), a discarding floor would cut the weak field with a band shape (the wrong sign and the wrong shape against the RAR), and the deep law needs a root (not one of the six); the dark sector stays as record 283 says"
)
