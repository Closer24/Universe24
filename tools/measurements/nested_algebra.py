"""THE ALGEBRA OF A BOUND BODY INSIDE A BOUND BODY (the owner's word of 2026-09-29): two standing records a (the outer, 600 quanta) and b (the inner, 300 quanta) laid alone by the pixel tool on the chain of Gamma 6,000, set at overlapping Nodes; the family's level at a Node is one number, so at shared Nodes the two are one record a + b. Checked in the engine's own integers: (i) Rule3 is linear, step(a + b) = step(a) + step(b) to the rounding; (ii) the current is bilinear, F(a + b) = F(a) + F(b) + the interference current; (iii) the form is quadratic, E(a + b) = E(a) + E(b) + 2 B(a, b), so the count of the union is not the sum of the counts; (iv) the band at a pace: the inner's rotation against the band's top at the outer's centre. Usage: nested_algebra.py <offset> <inner>."""

import json
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, "src")
import event_universe.world_files as wf
from event_universe.core.rule3 import coefficients, rule3
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world
from tests.laws import load_file

ROOT = Path(".")
TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
offset, inner = int(sys.argv[1]), int(sys.argv[2])
LENGTH, GAMMA, NUM, DEN = 240, 6000, 4000, 6000
d = Path(tempfile.mkdtemp())
wf.REPOSITORY_ROOT = d
events = ROOT / "examples" / "events"
universe = json.loads((events / "planck_6000.json").read_text())
for family in universe["families"]:
    if family.get("name") == "gravity":
        family["held"]["divisor"] = 10_000
(d / "u.json").write_text(json.dumps(universe))
(d / "e.json").write_bytes((events / "engine_start.json").read_bytes())


def body(x, count):
    return dict(
        family="matter",
        nodes=[dict(node=[x, 0, 0], count=count)],
        momentum=[0, 0, 0],
        momentum_before=[0, 0, 0],
        phase_denominator=1024,
    )


def document(bodies):
    return dict(
        shape=[LENGTH, 1, 1],
        boundary=dict(x="open", y="periodic", z="periodic"),
        detectors=[],
        ticks=10,
        N=65536,
        face_depth=1,
        universe="u.json",
        engine="e.json",
        measured=bodies,
    )


records, sims = {}, {}
for name, b in (("outer", body(LENGTH // 2, 600)), ("inner", body(LENGTH // 2 + offset, inner))):
    world = d / f"{name}.json"
    world.write_text(json.dumps(document([b])))
    TOOL.main(["--input", str(world)])
    entry = json.loads(world.with_suffix(".mode.json").read_text())["bodies"][0]
    records[name] = (
        np.array(entry["moving"]["now"], dtype=np.int64).reshape(LENGTH, 1, 1),
        np.array(entry["moving"]["before"], dtype=np.int64).reshape(LENGTH, 1, 1),
        entry["clock"],
    )
    sims[name] = DetectorLawSimulation(load_world(world))
    sims[name].step()
(a_now, a_before, a_clock), (b_now, b_before, b_clock) = records["outer"], records["inner"]
sim = sims["outer"]
live = sim.blocks[0].own
family = live.family
content = sim._effective_content(
    family
)  # the outer's well alone, as the engine reads it at its first interval
num, den = sim.pair_arrays(family, live.pair)
reads, S, w = coefficients(num, den, GAMMA, content)
wrap = sim.kind_wrap[family]


def step(now, before):
    arrivals = sim._axis_sums(now, wrap)
    return rule3(reads, arrivals, S, w, now, before, np.zeros_like(now))[0]


def current(now, before):
    """The plain current into every Node through its +x Port, num (now_i before_j - before_i now_j), j the neighbour."""
    up_now, up_before = sim.ports.arrivals(now, wrap)[0], sim.ports.arrivals(before, wrap)[0]
    return NUM * (now * up_before - before * up_now)


def form(now, before):
    """The law's conserved form E_i = [w (now^2 + before^2) - S now before] / p_i^2 - 2 num now S_6(before) (ALGEBRA.md #the-conserved-form), in floats."""
    p2 = reads[0] / (2 * NUM)
    a, b = now.astype(float), before.astype(float)
    s6b = sum(np.asarray(v, dtype=float) for v in sim.ports.arrivals(before, wrap))
    return (w * (a * a + b * b) - S * a * b) / p2 - 2 * NUM * a * s6b


shared = (a_now != 0) & (b_now != 0)
print(
    f"the outer's Nodes x {np.nonzero(a_now)[0].min()}..{np.nonzero(a_now)[0].max()}, the inner's x {np.nonzero(b_now)[0].min()}..{np.nonzero(b_now)[0].max()}, shared {int(shared.sum())} Nodes"
)
# (i) linearity
sum_step, split = step(a_now + b_now, a_before + b_before), step(a_now, a_before) + step(b_now, b_before)
print(
    f"(i) Rule3 is linear: max |step(a + b) - step(a) - step(b)| = {int(np.abs(sum_step - split).max())} level unit(s) (the rounding of two divisions against one), the levels up to {int(np.abs(sum_step).max())}"
)
# (ii) the current's bilinearity
Fa, Fb, Fab = (
    current(a_now, a_before),
    current(b_now, b_before),
    current(a_now + b_now, a_before + b_before),
)
cross = Fab - Fa - Fb
T = sim.count_wall(sim.blocks[0])
print(
    f"(ii) the current is bilinear: the interference current F(a + b) - F(a) - F(b) reaches {np.abs(cross).max() / T:.2f} quanta per interval on one Link (F(a) up to {np.abs(Fa).max() / T:.2f}, F(b) up to {np.abs(Fb).max() / T:.2f}); over the shared Nodes it sums to {cross[shared].sum() / T:+.2f} quanta per interval: each body's own current moves its own quanta, the interference moves quanta neither owns"
)
# (iii) the form's quadratic
Ea, Eb, Eab = form(a_now, a_before), form(b_now, b_before), form(a_now + b_now, a_before + b_before)
print(
    f"(iii) the form is quadratic: E(a + b) = E(a) + E(b) + 2 B(a, b) with 2 B = {(Eab - Ea - Eb).sum() / (2 * T):+.1f} quanta against E(a) / 2 = {Ea.sum() / (2 * T):.1f} and E(b) / 2 = {Eb.sum() / (2 * T):.1f}: the union's count is not the sum of the counts; at the shared Nodes alone 2 B = {(Eab - Ea - Eb)[shared].sum() / (2 * T):+.1f}"
)
# (iv) the band at a pace: the inner's rotation against the band's top at the outer's centre
centre = LENGTH // 2
p0 = np.sqrt((GAMMA - content[centre, 0, 0]) ** 2 + content[centre, 0, 0] ** 2) / GAMMA
pa = np.sqrt(reads[0][centre, 0, 0] / (2 * NUM)) / GAMMA
top_vacuum = NUM / DEN
top_well = (
    1 - (1 - NUM / DEN) * p0 * p0
)  # cos omega at k = 0 with the two paces: the band's top at the outer's centre
cos_inner = b_clock[0] / (2 * b_clock[1])
cos_outer = a_clock[0] / (2 * a_clock[1])
print(
    f"(iv) the band at a pace: at the outer's centre p_0 / Gamma = {p0:.4f}, p_a / Gamma = {pa:.4f}; the band's top cos omega rises from {top_vacuum:.4f} in the vacuum to {top_well:.4f} there; the inner body's own rotation cos omega_b = {cos_inner:.4f} (the outer's {cos_outer:.4f}): a rotation below the local top lies inside the local band, so the inner body laid alone is no bound mode inside the outer's well; it is bound there only with cos omega_b above {top_well:.4f}"
)
