"""Write JSON fixtures (tensor + Q + initial state + final state + official click rows of every update) so that an
independent implementation can cross-check this engine bit for bit on the documented tensor format.

    python universe24/tools/export_fixtures.py [out_dir]

Default out_dir: universe24/results/fixtures/. Read-only with respect to the engine and universe24.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from universe24.core import Engine, State, build, reference_block, reference_names  # noqa: E402
from universe24.core.engine import OBJ  # noqa: E402
from universe24.core.tensor import Block  # noqa: E402
from universe24.tests import randgen  # noqa: E402


def stamp() -> str:
    return subprocess.run(["date", "-u"], capture_output=True, text=True, check=True).stdout.strip()


def state_hash(s: State) -> str:
    return hashlib.sha256(json.dumps(s.to_dict(), separators=(",", ":")).encode()).hexdigest()


def fixture(name, tensor, Q, s0, steps):
    eng = Engine(tensor, Q)
    s = s0
    hashes, clicks = [state_hash(s0)], []
    for k in range(1, steps + 1):
        s2 = eng.step(s)
        clicks.append([[*xyz, g, kind, q, lab] for _, xyz, g, kind, q, lab in eng.clicks(s, s2, k).rows()])
        hashes.append(state_hash(s2))
        s = s2
    back = eng.rewind(s, steps)
    return {"name": name, "written_utc": stamp(), "Q": Q, "D": 6 * Q, "L": s0.L, "steps": steps,
            "tensor_fingerprint": tensor.fingerprint, "tensor": tensor.to_dict(), "initial": s0.to_dict(),
            "final": s.to_dict(), "state_sha256_per_update": hashes,
            "official_clicks_per_update": clicks,
            "click_row_format": ["x", "y", "z", "gear_index", "kind(0=C0,1=C1,2=C2)", "quotient", "gear_label"],
            "rewind_returns_initial": back.same_as(s0), "engine_stats": eng.stats}


def ref_state(seed, Q, L, lo=-20, hi=20):
    s = randgen.random_state(seed, 48, L, 6, lo, hi)          # r in 0..5, then scaled by Q
    return State(L, s.a, s.b, s.r.astype(OBJ) * Q)


def main(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    jobs = []
    jobs.append(("ref_Q1_L4", build(reference_block(1)), 1, ref_state(501, 1, 4), 12))
    jobs.append(("ref_Q7_L4", build(reference_block(7)), 7, ref_state(501, 7, 4), 12))
    tA = build(randgen.random_tensor_block(10, G=6, Q=10 ** 6, a_reads=False))
    jobs.append(("rand_b_only_seed10_L4", tA, 10 ** 6, randgen.random_state(1010, 6, 4, 6 * 10 ** 6, -20, 20), 20))
    tB = build(randgen.random_tensor_block(11, G=6, Q=10 ** 6, a_reads=True))
    jobs.append(("rand_a_reads_seed11_L4", tB, 10 ** 6, randgen.random_state(1011, 6, 4, 6 * 10 ** 6, -20, 20), 20))
    tC = build(randgen.random_tensor_block(32, G=5, Q=1, a_reads=True, small=5))
    jobs.append(("cubic_Q1_bigint_seed32_L4", tC, 1, randgen.random_state(2032, 5, 4, 6, -3, 3), 6))
    new, back = randgen.coupled_new_block(62, reference_names(), deviation=False)
    tD = build(reference_block(7), new, Block((), tuple(back)))
    sD = randgen.random_state(3062, tD.G, 4, 42, -5, 5)
    jobs.append(("ref7_plus_32_new_coupled_L4", tD, 7, sD, 6))
    index = []
    for name, tensor, Q, s0, steps in jobs:
        data = fixture(name, tensor, Q, s0, steps)
        path = out_dir / f"{name}.json"
        path.write_text(json.dumps(data, separators=(",", ":")) + "\n")
        index.append({"file": path.name, "Q": Q, "L": s0.L, "G": tensor.G, "monomials": len(tensor),
                      "rank": tensor.rank, "stages": len(tensor.stages), "steps": steps,
                      "final_sha256": data["state_sha256_per_update"][-1],
                      "rewind_returns_initial": data["rewind_returns_initial"]})
        print(name, index[-1])
    (out_dir / "INDEX.json").write_text(json.dumps({"written_utc": stamp(), "fixtures": index}, indent=1) + "\n")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "results" / "fixtures")
