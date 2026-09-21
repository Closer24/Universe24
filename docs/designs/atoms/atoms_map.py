"""The two atoms under form B, the pins' arithmetic (read-only, the
mathematician, 2026-09-21; docs/designs/atoms/PINS.md): the generator of the
atoms series (`examples/events/atoms/make_worlds.py`, which imports series H's
fan, flux count and orbit arithmetic) is the one source of every number here.
Hydrogen at r = 12: the orbit under form B's drive, the closure 2 pi p r = j h
against the action re-fixed under the same drive and against series H's
registered action, the period, the fan's local exponent and the precession of a
near-circular orbit it gives, the reader's velocity term, what a `wave`
detector at the proton reads. Helium: the alpha of binding-v1 fixed as the
nucleus, two electrons of the register's electron, the exact fluxes at the
start Nodes and on the ring, the net inward push with the partner's repulsion
in closed form, the orbit, and the partner's retarded drag (DERIVATIONS_BEAM
12.1: a drag of beta times the push on a transverse pair) as the momentum it
takes per orbit. Every number is a GAMEBOARD reading of the design (derived
before any run) unless labelled the detector's expected reading. No run.

Run from the repository root:

    PYTHONPATH=src python docs/designs/atoms/atoms_map.py > docs/designs/atoms/atoms_map.out
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "atoms_make_worlds", ROOT / "examples" / "events" / "atoms" / "make_worlds.py"
)
GEN = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(GEN)

Q, N, SHELL, RATIO = GEN.Q, GEN.N, GEN.SHELL, GEN.RATIO
WIDTH, PACE, C_ROWS = GEN.WIDTH, GEN.PACE, GEN.C_ROWS
REGISTERED_ACTION = (
    5414584320  # series H's h = 16 p(8) under today's drive (examples/events/bohr/README.md)
)
REGISTERED_P12 = 288249497  # series H's p at r = 12 under today's drive
REGISTERED_T12 = 1462
FLIGHT_PER_LINK = GEN.T_D_AXIS / Q  # 110 / 64 intervals per Link on an axis, the rows' pace


def today_orbit(a: float, radius: float) -> dict[str, float]:
    """Series H's arithmetic under today's drive, n^2 / (Q S + n) = A, for the comparison."""
    reach = Q * WIDTH
    n = (a + math.sqrt(a * a + 4 * reach * a)) / 2
    return {
        "n": n,
        "p": round(n * GEN.ELECTRON),
        "speed": n / (reach + n),
        "period": 2 * math.pi * radius / n * (reach + n),
    }


derived = GEN.derive()
count = derived["count"]
flux = derived["flux"]
hyd = derived["hydrogen"]
action = derived["action"]
he = derived["helium"]

print("1. HYDROGEN AT r = 12 UNDER FORM B: THE ORBIT (GAMEBOARD readings of the design)")
print(
    f"   the fan: {len(derived['directions'])} directions, one shell per {SHELL} intervals; the width S = {WIDTH} (series H's); Q S = {Q * WIDTH}"
)
print(
    f"   form B on an axis: the pace v = n / (Q S + (T_D / Q) n) with T_D / Q = {GEN.T_D_AXIS} / {Q} = {PACE:.5f} (today's v = n / (Q S + n)); the rows' pace c = 1 / sqrt 3 = {C_ROWS:.4f}"
)
for r in (8, 12):
    a = (1 + RATIO) * Q * flux[r] * r / SHELL
    today = today_orbit(a, r)
    b = hyd[r]
    print(
        f"   r = {r:2d}: E_body = {flux[r]:.3f} entries per shell (the ring mean of the electron's three Nodes), A = 16 Q E r / 10 = {a:.1f};"
        f" today n = {today['n']:.1f}, p = {today['p']}, v = {today['speed']:.5f}, T = {today['period']:.0f};"
        f" form B n = {b['n']:.1f}, p = {b['p']}, v = {b['speed']:.5f} ({b['speed'] / today['speed']:.4f} of today's, the factor 1 / (1 + 0.72 v) = {1 / (1 + 0.72 * today['speed']):.4f}),"
        f" T = {b['period']:.0f} intervals, beta = v / c = {b['beta']:.4f}"
    )
p12, t12, v12 = hyd[12]["p"], hyd[12]["period"], hyd[12]["speed"]
print(
    f"   the action re-fixed by series H's rule under form B, h_B = 16 p_B(8) = {action} (the registered h = {REGISTERED_ACTION}, the ratio {action / REGISTERED_ACTION:.4f})"
)
j_b = 2 * math.pi * p12 * 12 / action
j_reg = 2 * math.pi * p12 * 12 / REGISTERED_ACTION
j_reg_today = 2 * math.pi * REGISTERED_P12 * 12 / REGISTERED_ACTION
print(
    f"   the closure 2 pi p r = j h (DERIVATIONS_BEAM 7.2): at r = 12, j = {j_b:.3f} against h_B (whole within {abs(j_b - 4):.3f}); against the registered h, {j_reg:.3f}; series H's registered p and h give {j_reg_today:.3f}"
)
print(
    f"   the phase's turn per orbit: j_B turns of the circle, the fraction beyond whole circles {j_b - math.floor(j_b):.3f} of a circle = {(j_b - math.floor(j_b)) * N:.1f} steps of {N} per orbit; per quarter orbit (an axis crossing to the next) {j_b / 4:.4f} turns, {((j_b / 4) % 1) * N:.2f} steps beyond whole"
)
print(
    f"   the lumps: T / {SHELL} = {t12 / SHELL:.0f} kicks per orbit of {360 / (t12 / SHELL):.2f} degrees each (series H at r = 12: 146 of 2.5)"
)
print()

print("2. HYDROGEN: THE PRECESSION PER ORBIT, WHAT THE LAW HAS AND WHAT IT HAS NOT (GAMEBOARD, derived)")
print(
    "   (i) the retarded field of a FIXED source is a steady flux (DERIVATIONS_BEAM 5.3, 12.1): no retardation term acts on the electron; no post-Newtonian term exists in the push (5.3): general relativity's advance has no source here"
)
beta = hyd[12]["beta"]
print(
    f"   (ii) the reader's velocity term (12b.1), the count (1 - n . beta) per direction: on a circle n is radial and beta tangential, n . beta = 0 at first order; the second order is beta^2 = {beta * beta:.2e} of the push, a bound on its precession of 2 pi beta^2 = {360 * beta * beta:.3f} degrees per orbit if it were all radial"
)
radii = [10, 11, 12, 13, 14]
ring = {r: GEN.ring_flux(count, r) for r in radii}
print(
    "   (iii) the fan's departure from the inverse square, the one closed form: the ring mean E_body(r) at r = "
    + ", ".join(f"{r}: {ring[r]:.3f}" for r in radii)
)
for lo, hi in ((10, 12), (11, 13), (12, 14), (10, 14)):
    k = -math.log(ring[hi] / ring[lo]) / math.log(hi / lo)
    apsidal = math.pi / math.sqrt(3 - k)
    print(
        f"       the local exponent k between r = {lo} and {hi}: E ~ r^-{k:.2f}; a near-circular orbit under F ~ r^-k has the apsidal angle pi / sqrt(3 - k) = {math.degrees(apsidal):.1f} degrees, the perihelion moving {math.degrees(2 * apsidal - 2 * math.pi):+.1f} degrees per orbit (k = 2 gives 0)"
    )
print(
    "   (iv) the whole kicks (one shell per 10 intervals) have no closed form: series H's loops were eccentric and precessing at every radius; registered, not pinned"
)
print()

print(
    "3. HYDROGEN: WHAT THE DETECTOR AT THE PROTON READS (the detector's EXPECTED readings, derived; the criteria of series H beside them)"
)
flight = 12 * FLIGHT_PER_LINK
print(
    f"   the electron releases one ray per in-plane heading every {SHELL} intervals from its three Nodes; the ray on -X from its middle Node (z = c) reaches the proton's Node after 12 Links x {FLIGHT_PER_LINK:.4f} = {flight:.1f} intervals"
)
print(
    f"   a click at the proton at every crossing of an axis of the proton by the electron's middle Node: four crossings per orbit, T / 4 = {t12 / 4:.0f} intervals apart (the orbital frequency 1 / T = {1 / t12:.2e} per interval, 4 / T = {4 / t12:.2e} clicks per interval); the electron holds a Node for about 1 / v = {1 / v12:.0f} intervals at a crossing, so one or two releases fall on the axis: 4 to 8 clicks per orbit"
)
print(
    f"   the first click: the electron starts on the +x axis; its first release at age {SHELL} reaches the proton at about {SHELL + flight:.0f}; then about {SHELL + flight + t12 / 4:.0f}, {SHELL + flight + t12 / 2:.0f}, {SHELL + flight + 3 * t12 / 4:.0f}, {SHELL + flight + t12:.0f} (T within 15 percent: {0.85 * t12:.0f} to {1.15 * t12:.0f} between returns to the same axis)"
)
print(
    f"   the phase of the clicks: the ray carries the electron's phase at release (no phase_per_link on e); a whole closure reads the same step at the same axis every orbit within the drift {(j_b - 4) * N:+.1f} steps per orbit; successive axes differ by j_B / 4 turns = {((j_b / 4) % 1) * N:.1f} steps beyond whole"
)
print(
    f"   the return (the orbit criterion of series H): within r / 4 = 3 Links of the start at the closing of the angle, T within 15 percent of {t12:.0f}"
)
print()

print("4. HELIUM: THE NUCLEUS, THE TWO ELECTRONS, THE FLUXES (GAMEBOARD, derived)")
print(
    f"   the nucleus: binding-v1's square (p 1834 + held nuclear 1 + bond 2, n 1837 + the same; the proton's charge {GEN.NUCLEUS_CHARGE_P}), FIXED at the four Nodes about (c + 1/2, c + 1/2, c), each releasing on the fan by the world's release [1, {GEN.PROTON * SHELL}]: {1834 / (GEN.PROTON * SHELL):.5f} and {1837 / (GEN.PROTON * SHELL):.5f} shells per interval"
)
print(
    f"   the electrons: the register's electron (charge -{RATIO}, content {GEN.ELECTRON}) at the offsets {GEN.ELECTRON_OFFSETS[0]} and {GEN.ELECTRON_OFFSETS[1]} from c, point-symmetric about the square's centre, r = {he['radius']:.3f}, each releasing every {SHELL} intervals on the fan's band |c| <= {GEN.ELECTRON_BAND} ({he['band_directions']} directions) and the four in-plane headings: every line of the fan that reaches the partner's three Nodes lies in the band (the partner's entries per shell {he['start_partner_band']} from the band against {he['start_partner']} from the whole fan), and no ray of the band steps from an outer Node of the electron's own set into its middle Node"
)
print(
    f"   the push products per ray, |rho_e rho_k - 1|: a proton {he['products']['p']} (inward), a neutron {he['products']['n']} (inward, gravity alone), the partner electron rho_e^2 - 1 = {he['repulsion']} (outward)"
)
print(
    f"   at the start Nodes, exact (the entries per shell the electron's three Nodes receive from each source at its offset): the nucleus's four sources, weighted and projected on the centre's direction, {he['start_inward']:.2f}; the partner at 2r, {he['start_partner']} entries per shell, x 224 = {224 * he['start_partner']}"
)
print(
    f"   on the ring (the orbit's mean): the nucleus {he['ring_nucleus']:.2f} = (2 x 61 + 2 x 1) x E_body({he['radius']:.2f}) with E_body = {GEN.ring_flux(count, he['radius']):.3f}; the partner 224 x E_body({2 * he['radius']:.2f}) = 224 x {GEN.ring_flux(count, 2 * he['radius']):.3f} = {he['ring_partner']:.2f}; the net inward {he['ring_nucleus'] - he['ring_partner']:.2f} (hydrogen's 16 x {flux[12]:.3f} = {16 * flux[12]:.2f} at r = 12)"
)
alt = (2 * 16 + 2 * 1) * GEN.ring_flux(count, he["radius"]) - he["ring_partner"]
print(
    f"   with series H's proton (charge [1, 1]) in place of binding-v1's: the nucleus (2 x 16 + 2 x 1) x E_body = {(2 * 16 + 2) * GEN.ring_flux(count, he['radius']):.2f} against the partner's {he['ring_partner']:.2f}: the net {alt:+.2f}, OUTWARD: no orbit, the pair repelled (the register's electron carries 15 times the proton's charge per unit of content, so two electrons repel each other 14 times as strongly as a proton holds one)"
)
print()

print(
    "5. HELIUM: THE ORBIT AND THE PARTNER'S RETARDED DRAG (GAMEBOARD, derived; the drag DERIVATIONS_BEAM 12.1's first-order term)"
)
print(
    f"   the circular orbit under form B with the net inward push: A = Q r (net) / 10 = {he['A']:.1f}; n = {he['n']:.1f}, p = {he['p']}, v = {he['speed']:.5f}, T = {he['period']:.0f} intervals, beta = {he['beta']:.4f}"
)
j_he = 2 * math.pi * he["p"] * he["radius"] / action
print(
    f"   the closure against hydrogen's h_B: j = 2 pi p r / h_B = {j_he:.3f} (whole within {abs(j_he - round(j_he)):.3f} of {round(j_he)}); the phase's turn per orbit {(j_he % 1) * N:.1f} steps beyond whole"
)
drag_per_interval = Q / SHELL * he["ring_partner"] * he["beta"]
inward_per_interval = Q / SHELL * (he["ring_nucleus"] - he["ring_partner"])
loss = drag_per_interval * he["period"] / he["n"]
print(
    f"   the partner's rays reach the electron from where the partner was 2r / c = {2 * he['radius'] / C_ROWS:.0f} intervals earlier, {he['speed'] * 2 * he['radius'] / C_ROWS:.2f} Links behind along its orbit: the repulsion tilts backward by the angle whose sine is beta (12.1), a tangential component against the motion of beta x 224 E(2r) per interval = {drag_per_interval:.3f} per unit of content, against the net inward {inward_per_interval:.3f}: {drag_per_interval / inward_per_interval:.3f} of it"
)
print(
    f"   over one orbit the drag takes {drag_per_interval * he['period']:.0f} of n = {he['n']:.0f}: {loss:.2f} of the momentum per orbit; the reader's factor on the partner's rays (1 - beta^2) = {1 - he['beta'] ** 2:.4f} and on the nucleus's 1 at first order"
)
print(
    "   so the diametral pair is not a closed orbit of the law: the pinned reading is the DECAY, the electrons' momenta falling by about half per orbit and the pair spiralling in (or apart, if the kicks scatter them) within two turns; a closed orbit at r = 12.5 would refute 12.1's drag"
)
print()

print("6. THE HOST COST, ESTIMATED FROM SERIES H'S RUNS (host numbers, not the model's)")
rays_h = len(derived["directions"]) / SHELL
rays_he = 4 * rays_h + 2 * (he["band_directions"] + 4) / SHELL
print(
    f"   series H: 19 to 87 s per world on four cores, the proton's {rays_h:.0f} rays per interval, records a few hundred megabytes per world (the bohr README); r12 (53^3, 7400 intervals) about 60 s"
)
print(
    "   hydrogen_r12 under form B: the same world with 7500 intervals: about 60 s, a few hundred megabytes"
)
print(
    f"   helium_r12: four nucleons on the whole fan and two electrons on the band, {rays_he:.0f} rays per interval ({rays_he / rays_h:.1f} times series H's), 55^3, 3700 intervals: about {rays_he / rays_h:.1f} x 60 x 3700 / 7400 = {rays_he / rays_h * 60 * 3700 / 7400:.0f} s, about one gigabyte of records"
)
