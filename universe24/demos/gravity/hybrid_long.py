"""H3 LONG RUN of the HYBRID gravity source (pre-registered in NOTES_gravity_hybrid.md). NEW FILE.
Run: OMP_NUM_THREADS=1 nice -n 19 python -m universe24.demos.gravity.hybrid_long [T] [detune_h00 0/1]
Writes results/gravity_hybrid/LONG_<tag>.json (checkpoint every 500 updates; final at the end or at a runaway)."""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ...core.engine import OBJ, Engine
from ...core.lattice import lattice
from ...core.tensor import compose
from ...layers.gravity_hybrid import hybrid_system
from ...prepare.gravity_hybrid import hybrid_source_total, with_hybrid_datum
from ...prepare.seed import l0_dark_seed, l0_rstar_vector, m0_band_vector, s2_star
from ...prepare.system import system_vacuum

OUT = Path(__file__).resolve().parents[2] / "results" / "gravity_hybrid"
L = 4


def stamp():
    return datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")


def main(Tn=20000, detune=0):
    t0 = time.time()
    S = hybrid_system(detune_h00=bool(detune))
    Q, P = S.Q, S.info["P"]
    T = compose(*S.blocks)
    E = Engine(T, Q)
    lat = lattice(L)
    N = lat.N
    vac = system_vacuum(S, T, L)
    bs = S.info["body_signs"]
    vb = None
    for band in range(9):
        try:
            vb = l0_rstar_vector(bs, m0_band_vector(bs, band, 64))
            break
        except (ValueError, IndexError):
            continue
    s = s2_star(vac, T, (1, 1, 1), 1 << 16)
    s = l0_dark_seed(s, T, (3, 3, 3), 1 << 6, v=vb)
    s = with_hybrid_datum(s, T, Q)
    Fi, Gi = T.gear_index("metric.h00"), T.gear_index("beta.G")
    sign = np.array([(-1) ** (x + y + z) for x, y, z in lat.all_coords()], dtype=object)
    tag = f"T{Tn}_detune{detune}"
    out = {"stamp_start": stamp(), "L": L, "T": Tn, "detune_h00": bool(detune), "info_gravity_source": S.info.get("gravity_source"),
           "beta_form": S.info.get("beta_form"), "seed": "S2* A=2^16 at (1,1,1) + L0 S-symmetrised band seed x 2^6 at (3,3,3)",
           "datum_total": hybrid_source_total(s, T, Q), "rows": [], "runaway_t": None}
    for t in range(Tn + 1):
        if t % 100 == 0:
            B = s.b.astype(OBJ)
            bits = int(s.max_abs()).bit_length()
            Um = int(np.sum(B[Fi])) / (2 * P * N)
            Upi = abs(int(np.sum(B[Fi] * sign))) / (2 * P * N)
            row = {"t": t, "U_mean": Um, "U_pi": Upi, "max_abs_G": int(max(abs(int(v)) for v in B[Gi])),
                   "max_abs_F_over_2P": max(abs(int(v)) for v in B[Fi]) / (2 * P), "bits": bits,
                   "wall_s": round(time.time() - t0, 1)}
            out["rows"].append(row)
            if bits > 60 or abs(Um) > 0.25 or Upi > 0.25:
                out["runaway_t"] = t
                break
            if t % 500 == 0:
                OUT.mkdir(parents=True, exist_ok=True)
                (OUT / f"LONG_{tag}.json").write_text(json.dumps(out, indent=1, default=str))
                print(json.dumps(row), flush=True)
        if t < Tn:
            s = E.step(s)
    out["stamp_end"] = stamp()
    out["bounded"] = out["runaway_t"] is None
    out["seconds"] = round(time.time() - t0, 1)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"LONG_{tag}.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({k: out[k] for k in ("runaway_t", "bounded", "seconds")}))


if __name__ == "__main__":
    args = [int(x) for x in sys.argv[1:]]
    main(*args)
