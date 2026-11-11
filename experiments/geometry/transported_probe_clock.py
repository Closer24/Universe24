"""Transported clock experiment with an explicit common-metric failure gate."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from universe24.core import Engine, State, Tensor
from universe24.layers.transported_probe import build
from universe24.prepare.transported_probe import prepare
from universe24.observe.transported_probe import sample, assess


def digest(state):
    return hashlib.sha256(json.dumps(state.to_dict(), separators=(",", ":")).encode()).hexdigest()


def execute(tensor, seed, steps):
    """Shared Engine is the sole producer of forward states; observations are passive."""
    if type(steps) is not int or steps < 0:
        raise ValueError("Nonnegative integer steps required")
    engine, state = Engine(tensor), seed
    samples, events, hashes = [sample(state, tensor, 0)], [], [digest(state)]
    for step in range(1, steps+1):
        following = engine.step(state)
        if not engine.inverse_step(following).same_as(state):
            raise AssertionError("Complete inverse failed")
        if not np.array_equal(following.b[:16], seed.b[:16]):
            raise AssertionError("Stationary geometric preparation lost")
        events.append(engine.clicks(state, following, step).select("official").rows())
        state = following
        samples.append(sample(state, tensor, step))
        hashes.append(digest(state))
    if not engine.rewind(state, steps).same_as(seed):
        raise AssertionError("Full rewind failed")
    return dict(steps=steps, exact_rewind=True, state_sha256=hashes,
                official_events_by_step=events, samples=samples,
                assessment=assess(state, tensor, samples))


def seam_control(seed, tensor):
    """Report the discrete transverse Laplacian, including periodic seam failures."""
    f = seed.b[tensor.gear_index("E03")].astype(object)
    laplacian = np.zeros(seed.N, dtype=object)
    for direction in ((1, 0, 0), (0, 1, 0)):
        laplacian += f[seed.lattice.shift_index(direction)] + f[
            seed.lattice.shift_index(tuple(-v for v in direction))]-2*f
    xyz = seed.lattice.all_coords()
    inside = (xyz[:, 0] > 0) & (xyz[:, 0] < seed.L-1) & (xyz[:, 1] > 0) & (xyz[:, 1] < seed.L-1)
    return dict(interior_nonzero_laplacians=int(np.count_nonzero(laplacian[inside])),
                seam_nonzero_laplacians=int(np.count_nonzero(laplacian[~inside])))


def run(macrosteps=24, L=5):
    if type(macrosteps) is not int or macrosteps < 6:
        raise ValueError("At least six macrosteps are needed for both flat clock cycles")
    tensor = build()
    cases = []
    # y=1 is a held-out opposite transverse direction; no new calibration.
    for curvature, x, y in ((0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0), (1, 0, 1)):
        seed = prepare(tensor, curvature=curvature, x=x, y=y, L=L)
        result = execute(tensor, seed, 2*macrosteps)
        cases.append(dict(curvature=curvature, x=x, y=y, seed=seed.to_dict(),
                          chart=seam_control(seed, tensor), **result))
    return dict(schema="transported-probe-clock-v1", divisor=6,
        tensor=tensor.to_dict(), tensor_fingerprint=tensor.fingerprint,
        channels=tensor.G, rank=tensor.rank, strict_support=not tensor.support_violations(),
        observation="Complete snapshots plus official events; not a click-only decoder",
        calibration="At even step 2n: t=2n,z=z0+n on the longitudinal cover; c=1 units",
        cases=cases,
        common_metric_validated=all(c["assessment"]["common_metric_passes"] for c in cases),
        limitations=["Chosen stationary vacuum pp-wave chart, not emergent Einstein evolution.",
                     "Marker transport is geometry-blind; off-axis geodesics fail.",
                     "Metric-coupled clock is a candidate; its off-axis proper-time response fails.",
                     "Flat species calibrations are fixed and are not a universal clock derivation.",
                     "Periodic transverse seams violate the harmonic chart; no atlas is supplied.",
                     "No matter backreaction; arbitrary geometric histories need not stay stationary.",
                     "Only even microsteps define the continuous comparison; odd banks are staggered."])


def replay(report):
    """Re-evolve exported complete seeds with the exported tensor, checking evidence."""
    tensor = Tensor.from_dict(report["tensor"])
    if tensor.fingerprint != report["tensor_fingerprint"]:
        raise ValueError("Tensor fingerprint mismatch")
    for case in report["cases"]:
        actual = execute(tensor, State.from_dict(case["seed"]), case["steps"])
        # JSON normalization handles tuple event coordinates after a file round trip.
        for key, value in actual.items():
            if json.loads(json.dumps(value)) != case[key]:
                raise ValueError(f"Replay mismatch: {key}")
    return dict(replayed_cases=len(report["cases"]), exact=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--macrosteps", type=int, default=24)
    parser.add_argument("--L", type=int, default=5)
    parser.add_argument("--out", type=Path, default=ROOT/"runs/transported-probe/report.json")
    parser.add_argument("--replay", type=Path)
    args = parser.parse_args()
    if args.replay:
        print(json.dumps(replay(json.loads(args.replay.read_text())), indent=2))
        return
    report = run(args.macrosteps, args.L)
    sources = [Path(__file__).resolve()] + [ROOT/p for p in (
        "universe24/layers/transported_probe.py", "universe24/prepare/transported_probe.py",
        "universe24/observe/transported_probe.py", "universe24/core/engine.py",
        "universe24/core/tensor.py", "universe24/core/lattice.py")]
    report["source_sha256"] = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    report["comparison"] = "New optional 26-channel tensor, not equivalent to either the default or prior 48-channel pp-wave examples."
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(dict(channels=report["channels"], rank=report["rank"],
        tensor_fingerprint=report["tensor_fingerprint"],
        common_metric_validated=report["common_metric_validated"],
        cases=[dict(curvature=c["curvature"], x=c["x"], y=c["y"], **c["assessment"]) for c in report["cases"]]), indent=2))


if __name__ == "__main__":
    main()
