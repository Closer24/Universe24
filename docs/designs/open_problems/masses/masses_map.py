"""The masses and charges as inputs and the missing binding energy: the map of problem (6)
of the seven (the open-problems physicist, read-only, 2026-09-21;
docs/designs/open_problems/masses/NOTE.md).

Integers of the lattice's geometry and nature's binding energies (AME2020 as NATURE.md and
issue #369 cite them); no engine import, no run.

(A) The binding counts on the cubic lattice for the light nuclei: the bodies at adjacent
    Nodes (the bipartite lattice has no triangle and no tetrahedron: the alpha is a square,
    the three-body sets a line or an L), the counts per body, per contact Link, per pair with
    the square's diagonals, and per contact Link BILINEAR in the two partners' contact
    numbers (each body's count of occupied Ports, a local reading of the six neighbours);
    against nature's B / B(deuteron); and the same counts in the saturated crystal (every
    body with six contacts, three Links per body) against nature's B / A of 8 MeV.
(B) The mass defect as a fraction: the law's give of 4 units of 3677 against nature's
    0.1185 percent for the deuteron, 0.76 for the alpha, 0.85 at iron (per nucleon).
(C) The linearity that forbids a ladder (the masses design's theorem, 24.2's additivity):
    the content dynamics of the exchange as a linear map with every equal split a fixed
    point, checked on the integers for a two-body exchange.

Run from the repository root:

    python docs/designs/open_problems/masses/masses_map.py > docs/designs/open_problems/masses/masses_map.out
"""

from __future__ import annotations

# nature's binding energies, MeV (AME2020), and the masses in m_e for the fractions
B = {"deuteron": 2.2246, "triton": 8.4818, "helium-3": 7.7180, "alpha": 28.2957}
A_NUCLEONS = {"deuteron": 2, "triton": 3, "helium-3": 3, "alpha": 4}
B_PER_A_SATURATED = 8.0  # MeV per nucleon near iron

# the lattice sets: bodies at adjacent Nodes; the contact Links between them; each body's contact count
SETS = {
    "deuteron": {"bodies": 2, "links": [(0, 1)]},
    "triton (a line)": {"bodies": 3, "links": [(0, 1), (1, 2)]},
    "triton (an L)": {"bodies": 3, "links": [(0, 1), (1, 2)]},
    "alpha (a square)": {"bodies": 4, "links": [(0, 1), (1, 2), (2, 3), (3, 0)]},
    "alpha (a square, with the two diagonals as second neighbours)": {
        "bodies": 4,
        "links": [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)],
    },
}


def counts(entry):
    bodies, links = entry["bodies"], entry["links"]
    contacts = [0] * bodies
    for a, b in links:
        contacts[a] += 1
        contacts[b] += 1
    per_body = bodies
    per_link = len(links)
    bilinear = sum(contacts[a] * contacts[b] for a, b in links)
    return per_body, per_link, bilinear, contacts


print("A. THE BINDING COUNTS ON THE CUBIC LATTICE, AGAINST NATURE'S RATIOS B / B(deuteron)")
print(
    "   set | bodies | contact Links | each body's contacts | per body (binding-v1 as built) | per contact Link | bilinear in the partners' contacts | nature's B / B(d)"
)
d_b, d_l, d_bil, _ = counts(SETS["deuteron"])
nature = {
    "deuteron": B["deuteron"] / B["deuteron"],
    "triton (a line)": B["triton"] / B["deuteron"],
    "triton (an L)": B["helium-3"] / B["deuteron"],
    "alpha (a square)": B["alpha"] / B["deuteron"],
    "alpha (a square, with the two diagonals as second neighbours)": B["alpha"] / B["deuteron"],
}
for name, entry in SETS.items():
    pb, pl, bil, contacts = counts(entry)
    print(
        f"   {name} | {entry['bodies']} | {len(entry['links'])} | {contacts} | {pb / d_b:.2f} | {pl / d_l:.2f} | {bil / d_bil:.2f} | {nature[name]:.2f}"
    )
print(
    "   (the triton's line and L give the same counts; nature's triton 3.81 and helium-3 3.47 differ by the Coulomb repulsion, not modelled here)"
)
print()
print(
    "   the saturated crystal (every body with six contacts, three contact Links per body), the binding per nucleon over the deuteron's per pair:"
)
sat_per_link = 3 * 1  # three Links per body, one give each
sat_bilinear = 3 * 36
print(
    f"   per contact Link: B / A = 3 gives per body = {3 * B['deuteron']:.1f} MeV per nucleon against nature's 8.0 (the ratio {3 * B['deuteron'] / B_PER_A_SATURATED:.2f}); bilinear: 3 x 36 = 108 gives per body = {108 * B['deuteron']:.0f} MeV per nucleon (the ratio {108 * B['deuteron'] / B_PER_A_SATURATED:.0f})"
)
print(
    "   the count per contact Link is right at saturation within 20 percent and short on the alpha by 3; the bilinear count is right on the light nuclei within 25 percent and over at saturation by 30: no single count of the lattice's geometry carries nature's binding from the deuteron to iron"
)
print()

print("B. THE MASS DEFECT AS A FRACTION OF THE MASS")
m_e = 0.51099895  # MeV
masses_me = {"deuteron": 3670.48297, "alpha": 7294.29954}
print(
    f"   the deuteron: nature {B['deuteron'] / (masses_me['deuteron'] * m_e) * 100:.4f} percent (4.353 m_e of 3674.84); the law's give 4 units of 3677: {4 / 3677 * 100:.4f} percent (series N: 0.109, an input width 8 percent under nature)"
)
print(
    f"   the alpha: nature {B['alpha'] / (masses_me['alpha'] * m_e) * 100:.3f} percent; the law's give 8 of 7354: {8 / 7354 * 100:.3f} percent (the ratio to the deuteron 2.0 against 12.72, NATURE row 7b)"
)
print(f"   iron: nature about {B_PER_A_SATURATED / 931.5 * 100:.2f} percent per nucleon")
print()

print(
    "C. THE LINEARITY THAT FORBIDS A LADDER: a two-body exchange of paid quanta as a linear map on the contents"
)
# each interval body 1 pays h units to body 2 at the rate n / d of its own content and vice versa: (M1, M2) -> (M1 - k M1 + k M2, M2 - k M2 + k M1) in the mean: the total conserved, the difference multiplied by (1 - 2k)
for m1, m2 in ((32768, 8192), (20480, 20480), (40000, 960)):
    a, b = m1, m2
    k_num, k_den = 1, 1024
    for _ in range(6000):
        give_a = a * k_num // k_den
        give_b = b * k_num // k_den
        a, b = a - give_a + give_b, b - give_b + give_a
    print(
        f"   ({m1}, {m2}) -> ({a}, {b}) after 6000 intervals at the rate 1 / 1024 each way: the total {m1 + m2} kept, the difference shrinks by (1 - 2 / 1024) per interval, the equal split the only fixed point of every total"
    )
print(
    "   every rule that acts per unit of content is linear in it (24.2's additivity), so no content is selected: the masses design's theorem; a ladder needs a rule that is not per unit of content (the window against the reader's own clock, which gives a harmonic ladder with 3068 unseen leptons)"
)
