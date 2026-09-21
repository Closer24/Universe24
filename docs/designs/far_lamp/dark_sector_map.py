"""The dark sector against the law's own rules, the arithmetic (read-only, the
mathematician, 2026-09-21; docs/designs/far_lamp/DARK_SECTOR.md): (1) what the
law's detector reads of a galaxy's edge: the Doppler of a slow source is exact
(section 2), the moving reader's factor (12b) is of the order of the speed over
c, so no reading through a detector inflates a rotation curve; (2) the one
mechanism the law has for a flat curve without unseen content, the periodic
short dimension of HYPOTHESES 6: the shell count N(r) in a periodic slab against
the open board (section 3.2's shell mean q Q / N(r)), its exponent beyond the
slab's thickness, and the Tully-Fisher slope it implies against nature's; (3) the
slab's own sky, which repeats at its thickness. No run.

Run from the repository root:

    python docs/designs/far_lamp/dark_sector_map.py > docs/designs/far_lamp/dark_sector_map.out
"""

from __future__ import annotations

import math

C_KM_S = 299_792.458

print("1. THE DETECTOR READING A GALAXY'S EDGE: THE LAW'S DOPPLER OF A SLOW SOURCE")
for v in (80.0, 150.0, 220.0):
    beta = v / C_KM_S
    receiver = 1 + beta  # the receiver's 1 +- v / c on the axis (section 2.2), exact over whole Links
    source = 1 / (1 - beta)  # the source's 1 / (1 -+ v / c) (section 2.3)
    reader = 1 - beta  # the moving reader's count per direction (1 - n . beta), 12b.1
    print(
        f"   v = {v:5.0f} km/s: beta = {beta:.2e}; the receiver's ratio {receiver:.6f}, the source's {source:.6f}, the transverse exactly 1, the moving reader's factor {reader:.6f}:"
        f" every departure from the classical Doppler is of order beta^2 = {beta * beta:.1e}"
    )
print(
    "   the flat curves are read at the edge to a few km/s out of 100 to 250; the law's readings differ from the classical Doppler by parts in 10^4 of the shift (parts in 10^7 of the reading): no reading through a detector makes a Keplerian edge look flat"
)
print()


def shell_count(r: float, thickness: int | None) -> int:
    """The Nodes at Euclidean distance abs(dist - r) < 1 / 2 from a source at the origin (section 3.2's
    shell), on the open board (thickness None) or in a periodic slab whose third axis has the given
    thickness (the distance in z to the nearest image)."""
    count = 0
    span = int(r) + 2
    zs = range(-span, span + 1) if thickness is None else range(thickness)
    for x in range(-span, span + 1):
        for y in range(-span, span + 1):
            for z in zs:
                dz = z if thickness is None else min(z, thickness - z)
                dist = math.sqrt(x * x + y * y + dz * dz)
                if abs(dist - r) < 0.5:
                    count += 1
    return count


print(
    "2. THE ONE MECHANISM IN THE LAW FOR A FLAT CURVE WITHOUT UNSEEN CONTENT: A PERIODIC SHORT DIMENSION (HYPOTHESES 6)"
)
print(
    "   the shell mean of the field is q Q / N(r) (section 3.2); N(r) counted on the lattice; the exponent p of the mean between successive radii, r^p (open board -2, a line of images -1)"
)
radii = [4, 6, 8, 12, 16, 24, 32]
for name, thickness in (
    ("open board", None),
    ("slab, thickness 3", 3),
    ("slab, thickness 9", 9),
    ("slab, thickness 27", 27),
):
    counts = [shell_count(r, thickness) for r in radii]
    exps = [
        math.log(counts[i] / counts[i + 1]) / math.log(radii[i + 1] / radii[i])
        for i in range(len(radii) - 1)
    ]
    cells = "  ".join(f"r {radii[i]}-{radii[i + 1]}: {e:+.2f}" for i, e in enumerate(exps))
    print(f"   {name:18s} N(r) = {counts};  p: {cells}")
print(
    "   beyond the thickness the shell is a cylinder, N(r) -> 2 pi r x thickness and the mean falls as 1 / r (HYPOTHESES 6's measured -0.97 in the period-3 slab, -2.04 on the open cube): the flat part begins at a radius set by the thickness, one length for every source"
)
print()

print("3. WHAT THE SLAB PREDICTS FOR THE FLAT SPEED AGAINST NATURE'S TULLY-FISHER RELATION")
print(
    "   under a 1 / r force beyond the thickness L, v^2 = r F / m is constant with r at v^2 proportional to M / L: the flat speed squared grows with the content, v^4 proportional to M^2;"
)
print(
    "   nature (the baryonic Tully-Fisher relation, McGaugh 2012): M_b = 47 M_sun (v / km s^-1)^4, the slope 3.9 +- 0.2: v^4 proportional to M"
)
anchor_m, anchor_v = 1e11, (1e11 / 47) ** 0.25
print(f"   anchored at M = 1e11 M_sun where both give v = {anchor_v:.0f} km/s:")
for m in (1e8, 1e9, 1e10, 1e11):
    v_nature = (m / 47) ** 0.25
    v_slab = anchor_v * math.sqrt(m / anchor_m)
    print(
        f"   M = {m:.0e} M_sun: nature's flat speed {v_nature:6.1f} km/s, the slab's {v_slab:6.1f} km/s, the ratio {v_slab / v_nature:.2f}"
    )
print(
    "   a dwarf of 1e9 M_sun rotates at 60 to 70 km/s in nature and would rotate at 22 under the slab: the slab's slope is 2 where nature's is 4, a factor 3 in speed at the low end"
)
print()

print("4. THE SLAB'S OWN SKY")
for thickness_kpc in (1.0, 10.0):
    print(
        f"   a periodic third dimension of {thickness_kpc:.0f} kpc: every source, the Milky Way included, is seen again at {thickness_kpc:.0f}, {2 * thickness_kpc:.0f}, {3 * thickness_kpc:.0f} kpc along that axis, a sky that repeats;"
    )
print(
    "   the flat parts of the curves begin between 1 and 10 kpc, so the slab that makes them needs a thickness of that order, and nature's sky does not repeat at any such spacing (the nearest large galaxy at 780 kpc, one of it)"
)
print()

print(
    "5. THE VERDICT: the reading through a detector adds nothing at beta ~ 10^-3; the law's field is Newton's in the shell mean on the open board; the one in-law route to a flat curve, the short periodic dimension, gives one flattening length for every source, the Tully-Fisher slope 2 against 4 and a repeating sky: not a hypothesis that closes; unseen content as an input family (a charge column 0, no lamp) is what the law admits, as nature's model does"
)
