"""GRAV-FIX T2 static-law check (pre-registered): with a prescribed static F (multiples of 2^11, so F^2/(2P) is an
integer) and G prepared at F^2/(2P) (a = b), one update leaves G EXACTLY unchanged (u_G = 6Q G: the static law
G = F^2/(2P), i.e. beta = 1, holds for the detuned blocks as for the default). Also: vacuum fixed, rewind 20 exact."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import numpy as np

from universe24.core import Block, Engine, GearType, State, check_reciprocity, compose
from universe24.core.engine import OBJ
from universe24.layers import gravity as gr
from universe24.layers.gravity_beta_fix import build_beta_detuned
from universe24.prepare import vacuum_state


def main():
    Q, P, k = (1 << 33) + 1, 1 << 20, 1 << 12
    out = {}
    for name, nd in [("default", None), ("A", (1, 2)), ("B", (3, 4))]:
        Fb = Block((GearType("F", "audit"),), tuple(gr.gradient_terms(gr.wave_potential("F", 0, 6 * Q))), name="Fs",
                   vacuum={"F": 3 * Q - 1}, Q=Q)
        if name == "default":
            beta = gr.build_beta(Q=Q, P=P, k=k, field="Fs.F")
        else:
            beta = build_beta_detuned(Q=Q, P=P, k=k, field="Fs.F", num=nd[0], den=nd[1])
        blocks = [Fb, beta]
        T = compose(*blocks)
        eng = Engine(T, Q)
        L = 8
        s = vacuum_state(T, Q, L, *blocks)
        xyz = s.lattice.all_coords()
        d2 = ((xyz - 4) ** 2).sum(axis=1)
        Fv = np.array([int(round(200 * np.exp(-d / 6.0))) * (1 << 11) for d in d2], dtype=object)
        Gv = np.array([(int(f) * int(f)) // (2 * P) for f in Fv], dtype=object)
        a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
        gF, gG = T.gear_index("Fs.F"), T.gear_index("beta.G")
        a[gF], b[gF] = Fv.copy(), Fv.copy()
        a[gG], b[gG] = Gv.copy(), Gv.copy()
        s = State(L, a, b, r)
        s1 = eng.step(s)
        dG = int(max(abs(int(x)) for x in (s1.b[gG].astype(OBJ) - Gv)))
        vac = vacuum_state(T, Q, L, *blocks)
        rng = np.random.default_rng(1)
        s0 = State(L, rng.integers(-1000, 1000, (T.G, L ** 3)), rng.integers(-1000, 1000, (T.G, L ** 3)),
                   rng.integers(0, 6 * Q, (T.G, L ** 3)))
        rep = check_reciprocity(T)
        out[name] = {"static_law_max_change_one_update": dG, "max_G_static": int(max(Gv)),
                     "vacuum_fixed": eng.run(vac, 10).same_as(vac),
                     "rewind_20_exact": eng.rewind(eng.run(s0, 20), 20).same_as(s0),
                     "reciprocity_ok": rep.ok, "designated": len(rep.designated), "rank": T.rank,
                     "params": {k_: v for k_, v in beta.params.items() if k_ in ("w_G", "k_G", "detune")}}
    out["written_utc"] = subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()
    (ROOT / "universe24/results/gravity/GFIX_static.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
