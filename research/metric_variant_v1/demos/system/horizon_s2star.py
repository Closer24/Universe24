"""HORIZON CHECK (pre-registered in NOTES_system.md, "PRE-REGISTRATION RC2 BATCH 2b part 1"): the v2 default (GRAV-FIX A,
detuned beta) with the S2* seed (A = 2^16, i = 0, x0 = (2,2,2)), L = 6, 2,000 updates. Samples every 200 updates:
max |G_pi| (beta.G corner Fourier amplitude |Sum_x (-1)^(x+y+z) G(x)| / N), U_mean = mean(metric.h00)/(2P), max bits.
Run: OMP_NUM_THREADS=1 nice -n 10 python -m research.metric_variant_v1.demos.system.horizon_s2star [T] [beta_form] [L] [c2]
Writes results/system/horizon_s2star_<beta_form>[_L<L>][_c2].json."""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ...core.engine import OBJ, Engine
from ...core.tensor import compose
from ...layers.system import default_system
from ...prepare.seed import l0_dark_seed, l0_rstar_vector, s2_star
from ...prepare.system import system_vacuum

OUT = Path(__file__).resolve().parents[2] / "results" / "system"
L, A, X0 = 6, 1 << 16, (2, 2, 2)


def main(T: int = 2000, beta_form: str = "detuned", Lx: int = 6, c2: bool = False, l0seed: bool = False,
         A_l0: int = A):
    global L
    L = Lx
    t0 = time.time()
    S = default_system(beta_form=beta_form, c2=c2)
    Tn = compose(*S.blocks)
    E = Engine(Tn, S.Q)
    s = s2_star(system_vacuum(S, Tn, L), Tn, X0, A)
    if l0seed:                                    # + the S-symmetrised L0 dark seed (excites L0, hence c2)
        s = l0_dark_seed(s, Tn, X0, A_l0, v=l0_rstar_vector(S.info["body_signs"]))
    P = S.info["P"]
    gG, gF = Tn.gear_index("beta.G"), Tn.gear_index("metric.h00")
    lat = np.indices((L, L, L)).reshape(3, -1)
    sign = np.where((lat.sum(axis=0) % 2) == 0, 1, -1)
    N = L ** 3
    samples = []

    def sample(t, st):
        G = st.b[gG].astype(OBJ)
        F = st.b[gF].astype(OBJ)
        Gpi = abs(int(sum(int(sg) * int(g) for sg, g in zip(sign, G)))) / N
        Um = float(sum(int(f) for f in F)) / N / (2 * P)
        return {"t": t, "max_abs_G_pi": Gpi, "U_mean": Um, "max_bits": int(st.max_abs()).bit_length(),
                "seconds": round(time.time() - t0, 1)}

    samples.append(sample(0, s))
    status = "BOUNDED"
    for t in range(1, T + 1):
        s = E.step(s)
        if int(s.max_abs()).bit_length() > 60:          # every update (a runaway is doubly exponential)
            samples.append(sample(t, s))
            status = f"RUNAWAY at t = {t}"
            break
        if t % 200 == 0:
            samples.append(sample(t, s))
            print(samples[-1], flush=True)
            if samples[-1]["max_bits"] > 60:
                status = "RUNAWAY"
                break
    out = {"beta_form": beta_form, "L": L, "c2": c2, "l0seed": l0seed, "A_l0": A_l0 if l0seed else None, "c2_params": S.info.get("c2_params"), "A": A, "x0": X0, "T": T,
           "status": status,
           "max_abs_G_pi_overall": max(x["max_abs_G_pi"] for x in samples), "final": samples[-1],
           "samples": samples, "engine_stats": dict(E.stats),
           "stamp_utc": datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")}
    OUT.mkdir(parents=True, exist_ok=True)
    tag = beta_form + (f"_L{L}" if L != 6 else "") + ("_c2" if c2 else "") + (f"_l0seed{A_l0.bit_length() - 1}" if l0seed else "")
    (OUT / f"horizon_s2star_{tag}.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({k: v for k, v in out.items() if k != "samples"}, default=str))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2000, sys.argv[2] if len(sys.argv) > 2 else "detuned",
         int(sys.argv[3]) if len(sys.argv) > 3 else 6, (sys.argv[4] == "c2") if len(sys.argv) > 4 else False,
         (sys.argv[5] == "l0seed") if len(sys.argv) > 5 else False,
         (1 << int(sys.argv[6])) if len(sys.argv) > 6 else A)
