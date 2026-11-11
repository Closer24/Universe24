"""EM-D3 NON-CIRCULAR electrostatics (pre-registered in NOTES_em.md; S4-P PR-24 ported).

A neutral seed: a particle (kc = +0.6 x) and an antiparticle (the C-image of a kc = -0.6 x packet) at the SAME place,
with Phi = A = 0 (no prepared field). The separating charges build their own Coulomb field through the exact current
(A source) and the Lorenz accumulator. Readouts: relative L2 (r < 6 of the centre) of Phi_c/2 = (Phi + Phi_next)/2
against the static E1 potential of the instantaneous rho(t) (torus); the separation of the two species centroids vs a
coupling-off control (g_phi = g_A = sigma = 0); C == 0; rewind.
"""
import time

import numpy as np

if __package__:
    from .emlib import Q0, accel, em_system, phi_of, save, stamp
else:
    from emlib import Q0, accel, em_system, phi_of, save, stamp
from universe24.observe import em as oem
from universe24.prepare import vacuum_state
from universe24.prepare import em as pem

L, T, amp, width, k0 = 32, 60, 2 ** 14, 2.0, 0.6
hop, mass = Q0, (3 * Q0 + 1) // 2
t_start = stamp()
out = {}
for label, (g_phi, g_A, sigma) in (("coupled", (1, 1, 2 ** 13)), ("control_G0", (0, 0, 0))):
    blocks, Tn, eng = em_system(hop=hop, mass=mass, g_phi=g_phi, g_A=g_A, sigma=sigma)
    m, e = blocks
    D = 6 * Q0
    c = L // 2
    vac = vacuum_state(Tn, Q0, L, *blocks)
    ap, bp, _ = pem.dirac_packet(m.params, L, +1, width, amp, kc=(k0, 0, 0), center=(c, c, c))
    an, bn, _ = pem.dirac_packet(m.params, L, +1, width, amp, kc=(-k0, 0, 0), center=(c, c, c))
    s0 = pem.set_matter(vac, Tn, "matter", ap + pem.c_image(an), bp + pem.c_image(bn))
    dx = ((np.arange(L) - c + L // 2) % L) - L // 2
    Rr = np.sqrt(dx[:, None, None] ** 2 + dx[None, :, None] ** 2 + dx[None, None, :] ** 2)
    sel = Rr < 6
    Pp, Pm = oem.species_projector(1).astype(float), oem.species_projector(-1).astype(float)
    rec = []
    s = s0
    Cnz = 0
    t0 = time.time()
    em_par = dict(e.params, sigma=2 ** 13) if sigma == 0 else e.params
    for t in range(T + 1):
        wp, wm = oem.projected_density(s, Tn, Pp), oem.projected_density(s, Tn, Pm)
        cp = float((wp * dx[:, None, None]).sum() / wp.sum())
        cn = float((wm * dx[:, None, None]).sum() / wm.sum())
        item = dict(t=t, sep=cp - cn)
        if sigma:
            rho = np.asarray(oem.charge_density(s, Tn, D), float)
            phic2 = np.asarray(oem.phi_centred(s, Tn), float) / 2.0
            phiP = phi_of(rho, em_par)
            item["rel_L2_r<6"] = float(np.sqrt(((phic2 - phiP)[sel] ** 2).sum() / max((phiP[sel] ** 2).sum(), 1e-300)))
            item["phi_at_particle_side"] = float(phic2[(c + int(round(cp))) % L, c, c])
            item["phi_at_anti_side"] = float(phic2[(c + int(round(cn))) % L, c, c])
            Cnz += int(np.count_nonzero(np.asarray(oem.lorenz_C(s, Tn) != 0, bool)))
        rec.append(item)
        if t < T:
            s = eng.step(s)
    rew = eng.rewind(s, T).same_as(s0)
    out[label] = dict(records=rec, rewind_exact=rew, lorenz_C_nonzero=Cnz, secs=time.time() - t0,
                      max_abs=s.max_abs(), g_phi=g_phi, g_A=g_A, sigma=sigma)
    print(label, rew, [(r_["t"], round(r_["sep"], 3), round(r_.get("rel_L2_r<6", -1), 3)) for r_ in rec[::10]],
          flush=True)
sepG = np.array([r_["sep"] for r_ in out["coupled"]["records"]])
sep0 = np.array([r_["sep"] for r_ in out["control_G0"]["records"]])
late = [r_["rel_L2_r<6"] for r_ in out["coupled"]["records"] if 50 <= r_["t"] <= 60]
summary = dict(rel_L2_t50_60=late, rel_L2_ok=bool(max(late) <= 0.15),
               separation_coupled_minus_control=(sepG - sep0)[::10].tolist(),
               separation_slower_ok=bool(sepG[-1] < sep0[-1]), lorenz_C_nonzero=out["coupled"]["lorenz_C_nonzero"],
               rewind_exact=bool(out["coupled"]["rewind_exact"] and out["control_G0"]["rewind_exact"]))
save("EM-D3_noncircular", dict(out, summary=summary, L=L, T=T, amp=amp, width=width, k0=k0, Q=Q0, hop=hop, mass=mass,
                               started=t_start))
print(summary, flush=True)
