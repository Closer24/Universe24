"""The builders of the wrapped board's tests (tests/test_the_uniform_mode.py, tests/test_the_interval.py; beside tests/laws.py, whose size the tests' shape caps): the rule's own universe at gravity's level weight 1 with a held row's keys and the quantum action chosen (`universe_at_weight_one`), the matter record laid uniform over the 3-cube torus (`uniform_world`) and the same with its counts at the share the gate reads (`laid_torus`)."""

import json
import re

from event_universe import board_readings, records
from event_universe.core import paces
from event_universe.lattice import Lattice
from event_universe.world_files import input_digest, load_world
from tests.laws import BACK, UNIVERSE, refused

GAMMA, ACTION, CUBE, AMPLITUDE = 6000, 32768, 3, 435  # the rule's clock and quantum, a 3-cube torus
TORUS = {"x": "periodic", "y": "periodic", "z": "periodic"}


def universe_at_weight_one(folder, action=ACTION, **rows):  # type: ignore[no-untyped-def]
    """The rule's own universe beside the world with gravity's level weight 1, so that the content moves within a test's intervals, at the quantum action `action` (the rule's 32,768; 36,000 the closure where Gamma divides n E_s T) with the held keys `rows` names per family (gravity={"booking": "form"}: the form's own clock), and without the binding holder: a row with a gap rests on a torus through its gap alone, and at the pair [2400, 2401] the division act's iteration contracts the uniform mode by 1 - 1 / 2,400 per act and cycles under the floors (the shipped tests' 170,000 passes at [24, 25]), a limit of the rest's iteration and nothing of the carried mode, left open by name."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    universe["families"] = [f for f in universe["families"] if f["name"] != "binding"]
    for family in universe["families"]:
        family["reads"] = {name: w for name, w in family["reads"].items() if name != "binding"}
        if family["name"] == "gravity":
            family["held"]["level_weight"] = 1
        family.get("held", {}).update(rows.get(family["name"], {}))
    universe["integers"]["quantum_action"] = action
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")


def uniform_world(folder, name, counts=1, **changes):  # type: ignore[no-untyped-def]
    """A matter record laid uniform over the 3-cube at the band's rest rotation in the vacuum's content (the gravity rest 60): now A at every Node, before A cos omega with cos omega = 1 - (den - num) p_0^2 / (den Gamma^2), the k = 0 line's own; the body declared on every Node at `counts` each; the mode file beside at the world's digest."""
    nodes = CUBE**3
    world = {"shape": [CUBE] * 3, "boundary": dict(TORUS), "intervals": 20, "universe": "u.json"}
    world["bodies"] = [
        {
            "family": "matter",
            "nodes": [
                {
                    "node": [x, y, z],
                    "count": counts[(x * CUBE + y) * CUBE + z] if isinstance(counts, list) else counts,
                }
                for x in range(CUBE)
                for y in range(CUBE)
                for z in range(CUBE)
            ],
        }
    ]
    world.update(node_detectors=[], **changes)
    clock = paces.clock(GAMMA, 60)
    before = (2 * (6000 * GAMMA * GAMMA - 2000 * clock * clock) * AMPLITUDE + 6000 * GAMMA * GAMMA) // (
        2 * 6000 * GAMMA * GAMMA
    )  # A cos omega rounded half up, the test's own arithmetic
    path = folder / f"{name}.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    entry = {
        "family": "matter",
        "pair": [4000, 6000],
        "moving": {"now": [AMPLITUDE] * nodes, "before": [before] * nodes},
    }
    mode = {"world_digest": input_digest(world), "bodies": [entry], "packets": []}
    path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return path


def laid_counts(folder, name, **changes):  # type: ignore[no-untyped-def]
    """The matter record's counts at the share the gate reads (the count is the record's share, a reading: the first load names it), spread over the Nodes."""
    first = refused("share reads", Lattice, load_world(uniform_world(folder, name, 1, **changes)))
    read = int(re.search(r"share reads (\d+) quanta", str(first)).group(1))
    nodes = CUBE**3
    return [read // nodes + (1 if i < read % nodes else 0) for i in range(nodes)]


def laid_torus(folder, name, **changes):  # type: ignore[no-untyped-def]
    """The uniform world with its counts redeclared at the share the gate reads (`laid_counts`)."""
    return uniform_world(folder, name, laid_counts(folder, name, **changes), **changes)


def lockstep(board, gravity, matter, intervals):  # type: ignore[no-untyped-def]
    """The lockstep torus stepped `intervals` intervals, each interval's numbers read from the engine's own state and nothing computed: gravity's level now and before and its write remainder (one number at every Node each, asserted, the tension lines 0), the matter record's level now and before at the centre, then after the step the record's level next, gravity's level and write remainder after, and the eras as the board reads them (`board_readings.eras` from the record's lines kept before the step and the rulers read at -1 after it, the host's way); a list of dicts in the intervals' order."""
    course = []
    for _ in range(intervals):
        lines, record = board.states[gravity].lines, board.states[matter].lines[0]
        assert all(not line.now.any() for line in lines[1:])  # the tensions of a uniform record are 0
        step = {"level": one_number(lines[0].now), "before": one_number(lines[0].before)}
        step.update(remainder=one_number(board.states[gravity].write_remainders[0]))
        step.update(now=int(record.now[1, 1, 1]), before_record=int(record.before[1, 1, 1]))
        kept = [
            records.Record(r.now.copy(), r.before.copy(), r.remainder)
            for r in board.states[matter].lines
        ]
        board.step()
        step.update(next=one_number(board.states[matter].lines[0].now), after=one_number(lines[0].now))
        step["after"] = one_number(board.states[gravity].lines[0].now)
        step["remainder_after"] = one_number(board.states[gravity].write_remainders[0])
        forms = {(matter, 0): records.form(kept, board.lines_of(matter, 0))}
        step["eras"] = board_readings.eras(board, gravity, forms, board.rulers(-1))
        step["snapshot"] = BACK.snapshot(board)  # the interval's end, the run back's comparison
        course.append(step)
    return course


def light_torus(folder, name, amplitude, **changes):  # type: ignore[no-untyped-def]
    """The laid torus with a massless real-line family `light` [6000, 6000] reading gravity at 1 added to the universe beside the world, and one light plane wave along x at the wave [2, 3] (k = 2 pi / 3, the one wave the 3-cube closes) laid by hand in the mode file: now A cos(2 pi x / 3), before A cos(2 pi x / 3 + omega) with cos omega = (cos k + 2) / 3 = 1 / 2 at the vacuum's paces (ALGEBRA.md, The band at a pace), the two sums over the board 0 by the full period; the matter record's counts at the share the gate reads as `laid_torus` has them."""
    universe = json.loads((folder / "u.json").read_text(encoding="utf-8"))
    universe["families"].append(
        {"name": "light", "pair": [6000, 6000], "reads": {"gravity": 1}, "dimension": 1}
    )
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    counts = laid_counts(folder, name, **changes)
    top = {axis: [0, CUBE - 1] for axis in TORUS}
    wave = {"family": "light", "along": "x", "wave": [2, 3], "phase": [0, 1], "amplitude": amplitude}
    path = uniform_world(
        folder,
        name,
        counts,
        packets=[{**wave, "top": top, "edge": {axis: 0 for axis in TORUS}}],
        **changes,
    )
    mode = json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))
    levels = [amplitude, -amplitude // 2, -amplitude // 2], [amplitude // 2, -amplitude, amplitude // 2]
    moving = {
        k: [v[x] for x in range(CUBE) for _y in range(CUBE) for _z in range(CUBE)]
        for k, v in zip(("now", "before"), levels, strict=True)
    }
    mode["packets"] = [{"family": "light", "pair": [6000, 6000], "moving": moving}]
    path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return path


def one_number(array):  # type: ignore[no-untyped-def]
    """An array over the lattice that is one number at every Node, the lockstep board's; asserted."""
    assert int(array.max()) == int(array.min()), array
    return int(array.max())
