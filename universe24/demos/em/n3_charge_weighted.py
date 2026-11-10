"""EM-D1b POST-HOC (labelled, NOTES_em.md A3/A5): Newton III for the unequal-width (+,-) run read on MOMENTUM:
(Q2 a2 / <E''>_2) / (Q1 a1 / <E''>_1), Q_i = |sum rho| of packet i alone (its total charge), from the saved run."""
import json

import numpy as np

from emlib import OUT, Q0, em_system, save
from universe24.observe import em as oem
from universe24.prepare import vacuum_state
from universe24.prepare import em as pem

run = json.load(open(OUT / "EM-D1_coulomb_+-_r8_T150_w2_2.4.json"))
blocks, Tn, eng = em_system()
m, e = blocks
L = run["L"]
vac = vacuum_state(Tn, Q0, L, *blocks)
D = 6 * Q0
Q = []
for w in (run["width"], run["width2"]):
    a, b, _ = pem.dirac_packet(m.params, L, +1, w, run["amp"])
    Q.append(abs(float(np.asarray(oem.charge_density(pem.set_matter(vac, Tn, "matter", a, b), Tn, D), float).sum())))
F1 = Q[0] * run["a1"] / run["Epp"]
F2 = Q[1] * run["a2"] / run["Epp2"]
P1 = Q[0] * run["pred_a1"] / run["Epp"]
P2 = Q[1] * run["pred_a2"] / run["Epp2"]
res = dict(Q1=Q[0], Q2=Q[1], Q2_over_Q1=Q[1] / Q[0], momentum_ratio_measured=F2 / F1, momentum_ratio_predicted=P2 / P1,
           ok_2p5_percent=bool(-1.025 <= F2 / F1 <= -0.975), label="POST-HOC")
save("EM-D1b_newton3_charge_weighted_POSTHOC", res)
print(res)
