"""EM-D7 ONE BOARD, TWO FORCES (MECHANISM: prescribed static fields; pre-registered in NOTES_em.md; S4-P PR-21 ported).

A particle and its exact C-image antiparticle at rest, separated in y, both at x = 0 where the prescribed profiles
sin(2 pi x / L) have their largest gradient.
  G : a static lapse gear N(x) (MECHANISM block on the matter's rest-clock mass entries), charge-blind;
  E : a static Phi(x) on the E1 board with sigma = 0 (test charges: Phi and A stay exactly static), charge-odd;
  GE: both at once (superposition check).
Event view: species-projected Wronskian centroids. Click view: species-projected click-size Wronskian centroids
(ell(t)^T J' ell(t+1)). Accelerations from quadratic fits over the window.
"""
import time

import numpy as np

from emlib import MASS0, HOP0, Q0, accel, save, stamp
from universe24.core import Engine, State, compose
from universe24.layers.em import build_em
from universe24.layers.matter import build_matter, build_static_lapse_mechanism
from universe24.observe import em as oem
from universe24.prepare import vacuum_state
from universe24.prepare import em as pem

L, T, amp, width = 24, 200, 2 ** 14, 2.0
D = 6 * Q0
t_start = stamp()
X = np.arange(L)
prof = np.sin(2 * np.pi * X / L)
gN = int(0.002 * D)
Phi0 = D // 8000
Nprof = np.rint(gN * prof).astype(np.int64)[:, None, None] * np.ones((1, L, L), np.int64)
Pprof = np.rint(Phi0 * prof).astype(np.int64)[:, None, None] * np.ones((1, L, L), np.int64)
dx = ((X + L // 2) % L) - L // 2
Pp, Pm = oem.species_projector(1).astype(float), oem.species_projector(-1).astype(float)


def cen(w):
    return float((w * dx[:, None, None]).sum() / w.sum())


out = {}
t0 = time.time()
for kind in ("G", "E", "GE"):
    m = build_matter(Q=Q0, hop=HOP0, mass=MASS0)
    blocks = [m]
    if "E" in kind:
        blocks.append(build_em(Q=Q0, matter=m, g_phi=4, g_A=1, sigma=0))
    if "G" in kind:
        blocks.append(build_static_lapse_mechanism(Q=Q0, matter=m, coupling=1))
    Tn = compose(*blocks)
    eng = Engine(Tn, Q0)
    vac = vacuum_state(Tn, Q0, L, *blocks)
    a0, b0, _ = pem.dirac_packet(m.params, L, +1, width, amp)
    x0, x1 = (0, L // 4, L // 2), (0, 3 * L // 4, L // 2)
    s0 = pem.set_matter(vac, Tn, "matter", pem.shift(a0, x0) + pem.c_image(pem.shift(a0, x1)),
                        pem.shift(b0, x0) + pem.c_image(pem.shift(b0, x1)))
    if "E" in kind:
        s0 = pem.set_field(s0, Tn, "em", "Phi", Pprof, Pprof)
    if "G" in kind:
        s0 = pem.set_field(s0, Tn, "lapse", "N", Nprof, Nprof)
    ev, ck = [], []
    prev = None
    s = s0
    for t in range(T + 1):
        ev.append((cen(oem.projected_density(s, Tn, Pp)), cen(oem.projected_density(s, Tn, Pm))))
        if t < T:
            s2 = eng.step(s)
            ell = oem.click_sizes(s, s2, Tn)
            if prev is not None:
                ck.append((cen(oem.click_charge(prev, ell, Pp)), cen(oem.click_charge(prev, ell, Pm))))
            prev = ell
            s = s2
    ae = [accel([e_[i] for e_ in ev]) for i in (0, 1)]
    ac = [accel([c_[i] for c_ in ck]) for i in (0, 1)]
    rew = eng.rewind(s, T).same_as(s0)
    out[kind] = dict(a_particle=ae[0], a_antiparticle=ae[1], ratio_anti_over_part=ae[1] / ae[0],
                     click_a_particle=ac[0], click_a_antiparticle=ac[1], click_over_event=[ac[0] / ae[0], ac[1] / ae[1]],
                     rewind_exact=rew)
    print(kind, out[kind], flush=True)
G, E, GE = out["G"], out["E"], out["GE"]
summary = dict(
    gravity_ratio=G["ratio_anti_over_part"], gravity_ok=bool(0.999 <= G["ratio_anti_over_part"] <= 1.001),
    em_ratio=E["ratio_anti_over_part"], em_ok=bool(-1.01 <= E["ratio_anti_over_part"] <= -0.99),
    click_over_event=G["click_over_event"] + E["click_over_event"],
    click_ok=bool(all(0.995 <= x <= 1.005 for x in G["click_over_event"] + E["click_over_event"])),
    superposition_grav=(GE["a_particle"] + GE["a_antiparticle"]) / (G["a_particle"] + G["a_antiparticle"]),
    superposition_em=(GE["a_particle"] - GE["a_antiparticle"]) / (E["a_particle"] - E["a_antiparticle"]),
    rewind_exact=bool(all(v["rewind_exact"] for v in out.values())), secs=time.time() - t0)
save("EM-D7_twoforces", dict(out, summary=summary, L=L, T=T, amp=amp, width=width, Q=Q0, gN=gN, Phi0=Phi0,
                             started=t_start))
print(summary, flush=True)
