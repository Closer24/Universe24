"""EM-D6 click-space charge (pre-registered in NOTES_em.md; S4-P PR-9 ported to the centred-accumulator design).

Passive readout only: click sizes ell(t) = b(t+1) + b(t-1) of the matter gears; per species (projector 2 Pi_s) the
click charge q_click(t) = sum ell(t)^T J' ell(t+1) against the event charge Q'(t+1) = sum a^T J' b of the same species
(a, b of the state between the two updates). The official click rule (ell != 0 and the triple changed) is also counted.
"""
import numpy as np

if __package__:
    from .emlib import Q0, em_system, save, stamp
else:
    from emlib import Q0, em_system, save, stamp
from universe24.observe import em as oem
from universe24.prepare import vacuum_state
from universe24.prepare import em as pem

L, T, amp, width = 10, 60, 2 ** 16, 1.5
t_start = stamp()
blocks, Tn, eng = em_system(g_phi=4, g_A=1, sigma=2 ** 11)
m, e = blocks
D = 6 * Q0
vac = vacuum_state(Tn, Q0, L, *blocks)
a0, b0, _ = pem.dirac_packet(m.params, L, +1, width, amp)
a = pem.shift(a0, (2, 5, 5)) + pem.c_image(pem.shift(a0, (7, 5, 5)))
b = pem.shift(b0, (2, 5, 5)) + pem.c_image(pem.shift(b0, (7, 5, 5)))
s0 = pem.set_matter(vac, Tn, "matter", a, b)
Phi = pem.static_phi_for(oem.charge_density(s0, Tn, D), e.params)
s0 = pem.set_field(s0, Tn, "em", "Phi", Phi, Phi)
hist = eng.run(s0, T, history=True)
P = {+1: oem.species_projector(1).astype(float), -1: oem.species_projector(-1).astype(float)}
ells = [oem.click_sizes(hist[t], hist[t + 1], Tn) for t in range(T)]
ratios = {+1: [], -1: []}
qsigns = {+1: [], -1: []}
for t in range(T - 1):
    for sp in (1, -1):
        q = float(oem.click_charge(ells[t], ells[t + 1], P[sp]).sum())
        Qs = float(oem.projected_density(hist[t + 1], Tn, P[sp]).sum())
        ratios[sp].append(q / Qs)
        qsigns[sp].append(np.sign(q))
# official click statistics of the matter gears (engine readout)
mi = {Tn.gear_index(f"matter.{n}") for n in ("X0", "X1", "X2", "X3", "X4", "X5", "X6", "X7",
                                             "Y0", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7")}
kinds = [0, 0, 0]
nclick = 0
fld = {"A": 0, "Phi": 0}
fkinds = {"Phi": [0, 0, 0]}
for t in range(T):
    log = eng.clicks(hist[t], hist[t + 1])
    for g, k in zip(log.gear, log.kind):
        name = Tn.names[int(g)]
        if int(g) in mi:
            kinds[int(k)] += 1
            nclick += 1
        elif name == "em.Phi":
            fld["Phi"] += 1
            fkinds["Phi"][int(k)] += 1
        else:
            fld["A"] += 1
res = {}
for sp in (1, -1):
    r_ = np.array(ratios[sp])
    res[f"species_{sp:+d}"] = dict(qclick_over_Q_mean=float(r_.mean()), rel_std=float(r_.std() / abs(r_.mean())),
                                   qclick_sign=float(np.mean(qsigns[sp])))
summary = dict(res, ratio_ok=bool(all(0.95 <= res[k]["qclick_over_Q_mean"] <= 1.10 for k in res)),
               std_ok=bool(all(res[k]["rel_std"] <= 1e-3 for k in res)),
               sign_flips_with_C=bool(res["species_+1"]["qclick_sign"] == -res["species_-1"]["qclick_sign"]
                                      and abs(res["species_+1"]["qclick_sign"]) == 1.0),
               matter_official_clicks=nclick, matter_kinds_C0_C1_C2=kinds,
               matter_click_fraction=nclick / (16 * L ** 3 * T), field_official_clicks=fld, Phi_kinds=fkinds,
               rewind_exact=bool(eng.rewind(hist[-1], T).same_as(s0)))
save("EM-D6_qclick", dict(summary=summary, L=L, T=T, amp=amp, width=width, Q=Q0, started=t_start))
print(summary, flush=True)
