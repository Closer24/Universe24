"""H3 controls C1-C3 (pre-registered in NOTES_gravity_hybrid.md). NEW FILE. Same readouts and criteria as hybrid_long.
Run: OMP_NUM_THREADS=1 nice -n 19 python -m universe24.demos.gravity.hybrid_long_controls C [T]"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

from ...core.engine import OBJ, Engine, State
from ...core.lattice import lattice
from ...core.tensor import compose
from ...layers.gravity_hybrid import hybrid_system
from ...layers.system import default_system
from ...prepare.gravity_hybrid import with_hybrid_datum
from ...prepare.seed import l0_dark_seed, l0_rstar_vector, m0_band_vector, s2_star
from ...prepare.system import system_vacuum

OUT = Path(__file__).resolve().parents[2] / "results" / "gravity_hybrid"
L = 4
FINE_AFTER = 10 ** 9


def run(case, Tn=2000):
    t0 = time.time()
    hybrid = case != "C1"
    if case == "C2D":        # H3c: S2* only, hybrid with the detuned h00 (AGREE_ST S21 option)
        S = hybrid_system(detune_h00=True)
    else:
        S = hybrid_system() if hybrid else default_system(chiral=False, electroweak=False)
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
    if case in ("C1", "C3"):
        s = l0_dark_seed(s, T, (3, 3, 3), (1 << 6) if case == "C1" else (1 << 4), v=vb)
    Fi, Gi, Bi = T.gear_index("metric.h00"), T.gear_index("beta.G"), T.gear_index("bgk.B")
    if hybrid:
        s = with_hybrid_datum(s, T, Q)
    else:   # two-time snapshot datum of the b-only source (GRAV-FIX T3 idea), exact residue on the first nodes
        a, b = s.a.astype(OBJ).copy(), s.b.astype(OBJ).copy()
        for g in (Fi, Bi):
            a[g] = 0
            b[g] = 0
        u1 = np.asarray(E.inputs(State(L, a, b, s.r)), dtype=OBJ)
        u2 = np.asarray(E.inputs(State(L, b, a, s.r)), dtype=OBJ)
        Ssum = (int(np.sum(u1[Fi])) + int(np.sum(u2[Fi]))) // 2
        q, res = divmod(Ssum, N)
        vals = [q + (1 if n < res else 0) for n in range(N)]
        a, b = s.a.astype(OBJ).copy(), s.b.astype(OBJ).copy()
        a[Bi] = vals
        b[Bi] = vals
        s = State(L, a, b, s.r)
    sign = np.array([(-1) ** (x + y + z) for x, y, z in lat.all_coords()], dtype=object)
    out = {"case": case, "T": Tn, "rows": [], "runaway_t": None}
    for t in range(Tn + 1):
        if t % 10 == 0 or t >= FINE_AFTER:   # runaway check every 10 updates (every update after FINE_AFTER)
            B = s.b.astype(OBJ)
            bits = int(s.max_abs()).bit_length()
            Um = int(np.sum(B[Fi])) / (2 * P * N)
            Upi = abs(int(np.sum(B[Fi] * sign))) / (2 * P * N)
            row = {"t": t, "U_mean": Um, "U_pi": Upi, "U_min": min(int(v) for v in B[Fi]) / (2 * P),
                   "max_abs_G": int(max(abs(int(v)) for v in B[Gi])), "bits": bits}
            if t % 100 == 0:
                out["rows"].append(row)
                print(json.dumps(row), flush=True)
            if t >= FINE_AFTER:
                out.setdefault("fine_rows", []).append(row)
            if bits > 60 or abs(Um) > 0.25 or Upi > 0.25:
                out["rows"].append(row)
                out["runaway_t"] = t
                break
        if t < Tn:
            try:
                s = E.step(s)
            except OverflowError as exc:      # recorded, never hidden: the step itself failed
                out["engine_overflow"] = {"t": t, "error": repr(exc), "last_bits": int(s.max_abs()).bit_length()}
                out["runaway_t"] = t
                break
    out["bounded"] = out["runaway_t"] is None
    out["seconds"] = round(time.time() - t0, 1)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"LONG_control_{case}_T{Tn}.json").write_text(json.dumps(out, indent=1, default=str))
    print(case, out["runaway_t"], out["bounded"], [(r["t"], round(r["U_mean"], 6), round(r["U_pi"], 6)) for r in out["rows"][::2]])


if __name__ == "__main__":
    if len(sys.argv) > 3:
        FINE_AFTER = int(sys.argv[3])
    run(sys.argv[1], *[int(x) for x in sys.argv[2:3]])
