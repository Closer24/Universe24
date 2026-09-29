"""THE FORM THE RECORD CONSERVES IN ITS WELL (ALGEBRA.md #the-conserved-form): E_i = [w (now^2 + before^2) - S_i now before] / p_i^2 - 2 num now S_6(before), the Node term weighted by the pace, the Link term plain; against the vacuum share E0_i / 2 = 3 den (now^2 + before^2) - num now S_6(before) the count is laid by. Per interval on the chain body at rest and moving: the two totals, their change split into the dynamics at the paces of the interval (rounding alone where the form is exact) and the work term (the paces' change), and the continuity defect at every Node, Delta share - SUM_j F_ij, for each share, with its accumulation. Usage: form_watch.py <m> <ticks> <every>."""

import json
import math
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, "src")
import event_universe.events.detector_law as detector_law  # noqa: E402
import event_universe.world_files as wf  # noqa: E402
from event_universe.events.detector_law import DetectorLawSimulation  # noqa: E402

RECORDED = {}
_rule3 = detector_law.rule3


def recording_rule3(reads, arrivals, self_coefficient, wall, now, other, carry, direction=1):
    """The reads, self coefficient and wall the record's step used, recorded at the division act itself (the matter record's: an array of reads at the wall 6 den Gamma^2)."""
    if (
        isinstance(reads[0], np.ndarray)
        and reads[0].ndim == 3
        and int(np.asarray(wall).max()) > 10**9
        and isinstance(now, np.ndarray)
        and now.shape == reads[0].shape
    ):
        import traceback

        caller = traceback.extract_stack(limit=2)[0]
        RECORDED["paces"] = ((reads, self_coefficient, wall), None, None)
        RECORDED.setdefault("calls", []).append(
            (caller.name, caller.lineno, float(np.asarray(reads[0]).sum()))
        )
    return _rule3(reads, arrivals, self_coefficient, wall, now, other, carry, direction)


detector_law.rule3 = recording_rule3
import event_universe.features.phase as phase_folder  # noqa: E402

phase_folder.rule3 = (
    recording_rule3  # the two-pace branch (the axis contents) steps through the phase folder
)
from event_universe.world_files import load_world  # noqa: E402
from tests.laws import load_file  # noqa: E402

ROOT = Path(".")
TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
m, ticks, every = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
LENGTH, QUANTA = 240, 600
d = Path(tempfile.mkdtemp())
wf.REPOSITORY_ROOT = d
events = ROOT / "examples" / "events"
universe = json.loads((events / "planck_6000.json").read_text())
for family in universe["families"]:
    if family.get("name") == "gravity":
        family["held"]["divisor"] = 10_000
(d / "u.json").write_text(json.dumps(universe))
(d / "e.json").write_bytes((events / "engine_start.json").read_bytes())
body = dict(
    family="matter",
    nodes=[dict(node=[LENGTH // 2, 0, 0], count=QUANTA)],
    momentum=[0, 0, 0],
    momentum_before=[0, 0, 0],
    phase_denominator=1024,
)
document = dict(
    shape=[LENGTH, 1, 1],
    boundary=dict(x="open", y="periodic", z="periodic"),
    detectors=[],
    ticks=ticks,
    N=65536,
    face_depth=1,
    universe="u.json",
    engine="e.json",
    measured=[body],
)
rest = d / "rest.json"
rest.write_text(json.dumps(document))
TOOL.main(["--input", str(rest)])
mode = json.loads(rest.with_suffix(".mode.json").read_text())
entry = mode["bodies"][0]
now = np.array(entry["moving"]["now"], dtype=np.int64)
before = np.array(entry["moving"]["before"], dtype=np.int64)
peak = int(np.argmax(np.abs(now)))
cos_b = before[peak] / now[peak]
sin_b = math.sqrt(1 - cos_b * cos_b)
k = 2 * math.pi * m / LENGTH
x = np.arange(LENGTH) - peak
factor = 1.0692  # the gate's scale of the moving levels to the declared count (moving_body.py)
m_now = np.rint(factor * now * np.cos(k * x)).astype(np.int64)
m_before = np.rint(factor * now * (np.cos(k * x) * cos_b - np.sin(k * x) * sin_b)).astype(np.int64)
moving_mode = json.loads(json.dumps(mode))
e = moving_mode["bodies"][0]
e["moving"] = {"now": m_now.tolist(), "before": m_before.tolist()}
e["profile"] = m_now.tolist()
e["amplitude"] = int(np.abs(m_now).max())
grow = max(factor, e["amplitude"] / e["clock"][1])
e["clock"] = [int(round(e["clock"][0] * grow)), int(round(e["clock"][1] * grow))]
moving = d / "moving.json"
moving.write_text(rest.read_text())
moving.with_suffix(".mode.json").write_text(json.dumps(moving_mode))


def forms(sim, live):
    """The pace-weighted form E_i (float) and the vacuum share E0_i / 2 (int) from the engine's own coefficients at this interval, with the plain flux into every Node."""
    gamma = sim.node_clock
    wrap = sim.kind_wrap[live.family]
    (reads, S, w), _, _ = RECORDED["paces"]  # the reads this interval's step used
    num, den = sim.pair_arrays(live.family, live.pair)
    w = np.asarray(w, dtype=np.float64)
    S = np.asarray(S, dtype=np.float64)
    p2 = reads[0] / (2 * num)  # p_i^2, isotropic on the chain
    aniso = float(np.abs(reads[1] - reads[0]).max())
    a, b = live.now.astype(np.float64), live.before.astype(np.float64)
    s6b = sum(np.asarray(v, dtype=np.float64) for v in sim.ports.arrivals(live.before, wrap))
    s6a = sum(np.asarray(v, dtype=np.float64) for v in sim.ports.arrivals(live.now, wrap))
    weighted = (w * (a * a + b * b) - S * a * b) / p2 / 2 - num * a * s6b
    vacuum = 3 * den * (a * a + b * b) - num * a * s6b
    flux = num * (a * s6b - b * s6a)
    return weighted, vacuum, flux, np.sqrt(p2) / gamma, aniso, (a, b, S, w, p2, num)


def watch(path, label):
    print(f"=== {label}")
    sim = DetectorLawSimulation(load_world(path))
    block = sim.blocks[0]
    live = block.own
    prev = None
    acc_w = acc_0 = None
    work_total = dyn_total = 0.0
    walk_0 = 0.0
    for t in range(1, ticks + 1):
        RECORDED["calls"] = []
        sim.step()
        if t <= 3:
            print(
                f"t={t} coefficients calls (caller, line, content sum, reads sum): {RECORDED['calls']} | content sum {int(sim._effective_content(live.family).sum())} | twist reads {sim._twist_reads(live, False) is not None} axis contents {sim._axis_contents(live.family) is not None} second level {live.im_now is not None} self-source {sim._self_source(live, False) is not None} | momentum {block.momentum} | block.own is live {block.own is live} | own None {block.own is None} | clicked {getattr(live, 'clicked', None)} | sum|now| {int(np.abs(live.now).sum())} | identity {getattr(block.own, 'identity', None)} | silent {getattr(live, 'silent', None)} | events {[e.get('event') for e in getattr(sim, 'events', [])][-5:]}"
            )
        weighted, vacuum, flux, pace, aniso, parts = forms(sim, live)
        wall = sim.count_wall(block)
        if t == 1:
            print(
                f"paces p_i / Gamma at x 112..128: {np.round(pace[112:129, 0, 0], 4).tolist()}; anisotropy of the reads {aniso}"
            )
            acc_w = np.zeros_like(weighted)
            acc_0 = np.zeros_like(weighted)
        if t % every == 0:
            axis = sim._axis_contents(live.family)
            print(
                f"      t={t} reads' anisotropy max |R_y - R_x| / R_x {aniso / float(np.abs(parts[4]).max() * 2 * 4000):.5f}; axis contents t_a max |t_x| / Gamma {0 if axis is None else float(np.abs(axis[0]).max()) / sim.node_clock:.5f}"
            )
        if prev is not None:
            p_weighted, p_vacuum, p_parts, p_s6b = prev
            a, b, S, w, p2, num = parts
            pa, pb, pS, pw, pp2, pnum = p_parts
            # THE THEOREM'S SPLIT: the previous levels under this interval's paces (the paces the step read); the dynamics at fixed paces (rounding alone where the form is exact), then the work term (the paces' change on the previous levels)
            previous_now_paces = (w * (pa * pa + pb * pb) - S * pa * pb) / p2 / 2 - num * pa * p_s6b
            dyn = float(weighted.sum() - previous_now_paces.sum())
            work = float(previous_now_paces.sum() - p_weighted.sum())
            dyn_total += dyn
            work_total += work
            walk_0 += float(vacuum.sum() - p_vacuum.sum())
            acc_w += (weighted - previous_now_paces) - flux
            acc_0 += (vacuum - p_vacuum) - flux
        wrap = sim.kind_wrap[live.family]
        prev = (
            weighted,
            vacuum,
            parts,
            sum(np.asarray(v, dtype=np.float64) for v in sim.ports.arrivals(live.before, wrap)),
        )
        if t % every == 0 or t == 2:

            def q(v, wall=wall):
                return v / wall

            print(
                f"t={t:4d} weighted form total {q(weighted.sum()):9.2f} quanta (dynamics at fixed paces so far {q(dyn_total):+8.3f}, work term so far {q(work_total):+8.3f}) | vacuum share total {q(vacuum.sum()):9.2f} (drift so far {q(walk_0):+8.3f}) | counts min {int(block.counts.min()):3d} | continuity defect accumulated, weighted share: max |.| {q(np.abs(acc_w).max()):7.3f} quanta at x {int(np.argmax(np.abs(acc_w)))}; vacuum share: max |.| {q(np.abs(acc_0).max()):7.3f} at x {int(np.argmax(np.abs(acc_0)))}",
                flush=True,
            )
            if t % (4 * every) == 0:
                print(
                    f"      accumulated defect at x 112..128, weighted: {np.round(q(acc_w[112:129, 0, 0]), 1).tolist()}\n      vacuum:   {np.round(q(acc_0[112:129, 0, 0]), 1).tolist()}",
                    flush=True,
                )


watch(rest, "AT REST")
watch(moving, f"MOVING, k = 2 pi {m} / {LENGTH}")
