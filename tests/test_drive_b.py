"""drive-b-v1, the directional drive of a body (form B in the integer form (c)
of docs/designs/light_speed/FORM.md section 3.1; docs/designs/drive_b/DESIGN.md;
the model owner's approval of form B, 2026-09-22, record 652 of the log of
2026-09-20), under the world key `drive_b`, absent by default. Three signed
accumulators on the body's record, the rate p_a Q on each against ONE wall
W = Q^2 S M + |p|_1 T_h (T_h = isqrt(3 Q^2) = 110, formed at load; Q^2 S M
alone under `covariant_readings`), at most one Link per interval on the axis
furthest over the wall (the lowest on a tie), the others keeping their
overflow: the Bresenham line of the momentum with no coincident fire lost and
no root at run time. The expected integers of docs/TEST_EXPECTATIONS.md
("The directional drive"), written down before the first run:

(a) the key absent computes nothing: every registered world outside
    `drive_b/` parses with `drive_b` false and the identity absent from its
    hypotheses; the gate world `detector/grouped_12_nodes` replays to the
    digests of `gate_set.json` byte for byte, its `run.json` without a
    `drive_b` key; `drive_wall` is Q^2 S M + |p|_1 T_h with the cap and
    Q^2 S M without it; a bar world without the key steps as `by_drive`
    against Q S M + |p| (BEAM_LAW note 17);
(b) `by_line` against `by_drive` on one axis: from an empty accumulator at a
    constant p = (6000, 0, 0), M = 64, S = 1 (W = 922144, the rate 384000)
    the fires are at the self-creations where floor(n x 384000 / 922144)
    rises, the 21st at n = 51, and the accumulator after n is n x 384000
    mod 922144; the same integers as `by_drive(drive, 384000, 922144,
    at_most 1)`;
(c) the deciding worlds of the design on the engine (an open 41^3 box, the
    body of content 64 at its centre, `width` 1, 200 intervals; the
    generator's own worlds): the axis body (6000, 0, 0) clicks on face:+x
    at tick 51 from (40, 20, 20), the plane body (3000, 3000, 0) at tick 101
    from (40, 40, 20) after 21 Links on x and 20 on y, the cube body (2000,
    2000, 2000) at tick 152 from (40, 40, 40); every step's Node within one
    Link of the line of p; the `step` lines carry the fields they carry
    without the key and no other; the controls without the key click at
    36, 50 and 65 from (40, 20, 20) (the per-axis drive, y and z never
    moved);
(d) the reviewer's pins of record 348 on the engine against the host's
    replay, integer for integer: (1) a body at a constant |p|_1 = 6000 whose
    momentum cycles every 50 intervals through (6000, 0, 0), (3000, 1000,
    2000), (0, 6000, 0), (2000, 2000, 2000), (-3000, -1000, 2000) on a
    periodic 41^3 box makes the replay's Links on every axis at every one
    of 1000 intervals, 112, 112, 83 at the end against the whole parts
    floor(sum_t p_a(t) Q / W) 111, 111, 83, within 2 at every n; (2) a
    hand-over transient of -720 on y for one interval at n = 51, the
    momentum back on the axis after, leaves the y accumulator -46080
    (-0.050 Link) and fires no y Link in the 100 intervals after;
(e) the edges: p = 0 never steps and leaves the accumulators; a reversal
    (6000, 0, 0) to (-6000, 0, 0) at n = 30 cancels first, the next Link on
    -x where the replay's signed sum reaches -W; a component of 0 with a
    residue neither advances nor steps; a refused step at a contact
    (`pass`) subtracts W and does not move the body; the escape's click
    carries the body's momentum;
(f) the refusals by name: `drive_b` of a type other than a boolean; a
    momentum whose |p|_1 T_h passes the working bound at load under the key
    (admitted without it); an accumulator that would pass the bound;
(g) under `covariant_readings` and the key: a body of content 207 (Q S M =
    13248) at p = (2574, 2574, 0) and at (2101, 2101, 2101) is admitted at
    load and at the frame (refused without the key with the text as it is),
    its E' 14671 and 14670 as on the axis, its Links per axis over 40
    intervals the replay's with the wall Q^2 S M gated by its
    self-creations; with `action` (no covariant key) the turn by momentum
    composes per Link crossed on the axis: p = (64, 64, 0), content 1,
    h = 7, N = 64: after 10 intervals the Links [2, 2, 0] (W = 18176, the
    rate 4096: x at 5 and 9, y deferred to 6 and 10) and the phase
    (floor(2 x 4096 / 7) + floor(2 x 4096 / 7)) mod 64 = 36.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import pytest

from event_universe.core.integer import MAX_WORK_INT, by_drive, by_line
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.run import execute_nature_beam_run
from event_universe.events.world import DRIVE_B_RULE, LABEL_SCALE, MOMENTUM_BOUND, drive_wall
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "events"
WORLDS = EXAMPLES / "drive_b"
GATE_SET = EXAMPLES / "gate_set.json"
Q = LABEL_SCALE
T_H = math.isqrt(3 * Q * Q)


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def box_world(
    momentum: list[int],
    *,
    key: bool = True,
    content: int = 64,
    width: int = 1,
    ticks: int = 200,
    shape: int = 41,
    periodic: bool = False,
    extra: dict[str, object] | None = None,
) -> dict[str, object]:
    """The design's deciding world: one free body of no release at the centre
    of an open (or periodic) cube, the faces the detectors."""
    document: dict[str, object] = {
        "law": "beam",
        "model_id": "drive-b-box",
        "shape": [shape, shape, shape],
        "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"} if periodic else "open",
        "ticks": ticks,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1 << 20],
        "suspension": 0,
        "width": width,
        "families": [{"name": "body", "quantum": 0, "phase": False}],
        "measured": [
            {
                "position": [shape // 2] * 3,
                "family": "body",
                "amount": content,
                "momentum": list(momentum),
            }
        ],
    }
    if periodic:
        document["age_bound"] = 64
    if key:
        document["drive_b"] = True
    if extra:
        document.update(extra)
    return document


def run_in_process(document: dict[str, object], ticks: int):
    events: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(document), observer=events.append)
    for _ in range(ticks):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    return events, simulation


def sign_of_port(port: int) -> tuple[int, int]:
    return port // 2, 1 if port % 2 == 0 else -1


def links_of(events: list[dict[str, object]], number: int = 1) -> list[int]:
    """The signed Links per axis a body crossed, off its `step` lines."""
    found = [0, 0, 0]
    for event in events:
        if event["event"] == "step" and event["number"] == number:
            axis, sign = sign_of_port(int(event["step_port"]))
            found[axis] += sign
    return found


class Replay:
    """The host's replay of the rule (docs/designs/drive_b/drive_b_map.py's
    `DriveB`): the same integers the engine must produce."""

    def __init__(self, content: int, width: int, cap: bool = True) -> None:
        self.content, self.width, self.cap = content, width, cap
        self.drives = [0, 0, 0]
        self.links = [0, 0, 0]

    def wall(self, p: list[int]) -> int:
        return Q * Q * self.width * self.content + (sum(abs(c) for c in p) * T_H if self.cap else 0)

    def step(self, p: list[int]) -> tuple[int, int] | None:
        wall = self.wall(p)
        for axis in range(3):
            if p[axis]:
                self.drives[axis] += p[axis] * Q
        over = [a for a in range(3) if p[a] and abs(self.drives[a]) >= wall]
        if not over:
            return None
        chosen = max(over, key=lambda a: (abs(self.drives[a]), -a))
        sign = 1 if self.drives[chosen] > 0 else -1
        self.drives[chosen] -= sign * wall
        self.links[chosen] += sign
        return chosen, sign


def digests(folder: Path) -> dict[str, str]:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    return {
        "state_sha256": hashlib.sha256((folder / "state.json").read_bytes()).hexdigest(),
        "audit_sha256": hashlib.sha256(json.dumps(record.get("audit", [])).encode("utf-8")).hexdigest(),
        "events_sha256": hashlib.sha256((folder / "events.jsonl").read_bytes()).hexdigest(),
    }


# -- (a) ---------------------------------------------------------------------------


def test_the_key_absent_computes_nothing_and_the_gate_world_replays_byte_identical(tmp_path):
    """(a)."""
    checked = 0
    for path in sorted(EXAMPLES.rglob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(document, dict) or "format" in document or path.parent == WORLDS:
            continue
        world = load_world(path.read_bytes(), base_dir=path.parent, root=EXAMPLES).world
        assert world.drive_b is False, path
        assert DRIVE_B_RULE not in world.hypotheses, path
        checked += 1
    assert checked >= 100
    gate = json.loads(GATE_SET.read_text(encoding="utf-8"))
    entry = next(w for w in gate["worlds"] if w["path"] == "detector/grouped_12_nodes.json")
    path = EXAMPLES / entry["path"]
    source = path.read_bytes()
    loaded = load_world(source, base_dir=path.parent, root=EXAMPLES)
    out = tmp_path / "gate"
    out.mkdir()
    execute_nature_beam_run(loaded.world, source, out, "test", entry["cap"])
    assert digests(out) == entry["digests"]
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert "drive_b" not in record
    assert DRIVE_B_RULE not in record["hypotheses"]
    assert drive_wall([6000, 0, 0], 64, 1) == Q * Q * 64 + 6000 * T_H == 922144
    assert drive_wall([3000, -3000, 0], 64, 1) == 922144
    assert drive_wall([3000, -3000, 0], 64, 1, cap=False) == Q * Q * 64 == 262144
    assert drive_wall([1, 1, 1], 5, 2) == Q * Q * 10 + 3 * T_H
    # A world without the key steps by note 17's rule: on the axis the fires
    # of by_drive against Q S M + |p| (D = 10096 at p = 6000, M = 64).
    events, simulation = run_in_process(box_world([6000, 0, 0], key=False, ticks=36), 36)
    assert simulation.world.drive_b is False and DRIVE_B_RULE not in simulation.hypotheses
    ticks = [e["tick"] for e in events if e["event"] == "step"]
    drive, expected = 0, []
    for n in range(1, 37):
        count, drive = by_drive(drive, 6000, Q * 64 + 6000, at_most=1)
        if count:
            expected.append(n)
    assert ticks == expected[:20] and len(expected) == 21
    assert [e for e in events if e["event"] == "click"][0]["tick"] == 36


# -- (b) ---------------------------------------------------------------------------


def test_by_line_on_one_axis_is_by_drive():
    """(b)."""
    wall, rate = 922144, 6000 * Q
    assert wall == Q * Q * 64 + 6000 * T_H and rate == 384000
    drives = [0, 0, 0]
    reference = 0
    fires = []
    for n in range(1, 61):
        axis, sign, drives = by_line(drives, [rate, 0, 0], wall)
        count, reference = by_drive(reference, rate, wall, at_most=1)
        assert (axis, sign) == ((0, 1) if count else (None, 0)), n
        assert drives == [reference, 0, 0] == [(n * rate) % wall, 0, 0], n
        assert (n * rate) // wall == len(fires) + (1 if count else 0)
        if count:
            fires.append(n)
    assert len(fires) == 24 and fires[20] == 51
    # The sign: a negative rate counts to the - side, the accumulator signed.
    drives = [0, 0, 0]
    seen = []
    for _ in range(10):
        axis, sign, drives = by_line(drives, [0, -rate, 0], wall)
        seen.append((axis, sign))
    assert seen[2] == (1, -1) and drives[1] == -((10 * rate) % wall)
    # Two axes over the wall: the furthest over steps, the lowest on a tie,
    # the other keeps its overflow.
    axis, sign, drives = by_line([wall - 1, wall - 1, 0], [1, 2, 0], wall)
    assert (axis, sign, drives) == (1, 1, [wall, 1, 0])
    axis, sign, drives = by_line(drives, [0, 0, 0], wall)
    assert (axis, sign, drives) == (0, 1, [0, 1, 0])
    axis, sign, drives = by_line([wall, wall, 0], [0, 0, 0], wall)
    assert (axis, sign, drives) == (0, 1, [0, wall, 0])
    with pytest.raises(ValueError):
        by_line([0, 0, 0], [1, 0, 0], 0)


# -- (c) ---------------------------------------------------------------------------


GENERATOR = (
    load_script("drive_b_make_worlds", WORLDS / "make_worlds.py")
    if (WORLDS / "make_worlds.py").exists()
    else None
)


@pytest.mark.parametrize(
    ("name", "momentum", "tick", "node", "links"),
    [
        ("axis_b", [6000, 0, 0], 51, [40, 20, 20], [20, 0, 0]),
        ("plane_b", [3000, 3000, 0], 101, [40, 40, 20], [20, 20, 0]),
        ("cube_b", [2000, 2000, 2000], 152, [40, 40, 40], [20, 20, 20]),
    ],
)
def test_the_deciding_worlds_click_where_the_design_pins_them(name, momentum, tick, node, links):
    """(c), the key on."""
    assert GENERATOR is not None
    document = GENERATOR.worlds()[name]
    assert document["drive_b"] is True and document["measured"][0]["momentum"] == momentum
    events, simulation = run_in_process(document, 200)
    assert DRIVE_B_RULE in simulation.hypotheses
    clicks = [e for e in events if e["event"] == "click"]
    assert len(clicks) == 1
    click = clicks[0]
    assert (click["tick"], click["detector"], click["node"]) == (tick, "face:+x", node)
    assert click["momentum"] == momentum
    assert links_of(events) == links
    norm = math.sqrt(sum(c * c for c in momentum))
    steps = [e for e in events if e["event"] == "step"]
    assert len(steps) == sum(links)
    for event in steps:
        r = [event["to"][a] - 20 for a in range(3)]
        along = sum(r[a] * momentum[a] for a in range(3)) / norm
        assert sum(c * c for c in r) - along * along <= 1.0 + 1e-9, event
        assert set(event) == {
            "event",
            "tick",
            "number",
            "node",
            "to",
            "momentum",
            "phase",
            "drive",
            "step_port",
            "last_step_port",
        }
    if name == "axis_b":
        assert simulation.fast_steps == 0


@pytest.mark.parametrize(("name", "tick"), [("axis_main", 36), ("plane_main", 50), ("cube_main", 65)])
def test_the_controls_click_by_the_per_axis_drive(name, tick):
    """(c), the controls: the key off, y and z never moved."""
    assert GENERATOR is not None
    document = GENERATOR.worlds()[name]
    assert "drive_b" not in document
    events, simulation = run_in_process(document, 200)
    assert DRIVE_B_RULE not in simulation.hypotheses
    click = [e for e in events if e["event"] == "click"][0]
    assert (click["tick"], click["detector"], click["node"]) == (tick, "face:+x", [40, 20, 20])
    assert links_of(events) == [20, 0, 0]


# -- (d) ---------------------------------------------------------------------------


CYCLE = [[6000, 0, 0], [3000, 1000, 2000], [0, 6000, 0], [2000, 2000, 2000], [-3000, -1000, 2000]]


def test_the_reviewers_pin_1_the_wandering_direction():
    """(d) (1)."""
    world = box_world([6000, 0, 0], periodic=True, ticks=1000)
    events: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=events.append)
    entry = simulation.measured[1]
    replay = Replay(64, 1)
    wall = replay.wall(CYCLE[0])
    exact = [0, 0, 0]
    worst = 0
    for n in range(1000):
        p = CYCLE[(n // 50) % len(CYCLE)]
        entry.momentum = list(p)
        replay.step(p)
        simulation.step()
        assert links_of(events) == replay.links, n
        assert entry.drive == replay.drives, n
        for a in range(3):
            exact[a] += p[a] * Q
            whole = exact[a] // wall if exact[a] >= 0 else -((-exact[a]) // wall)
            worst = max(worst, abs(replay.links[a] - whole))
    assert replay.links == [112, 112, 83]
    assert [e // wall for e in exact] == [111, 111, 83]
    assert worst == 2
    assert entry.steps == 112 + 112 + 83


def test_the_reviewers_pin_2_the_hand_over_transient():
    """(d) (2)."""
    world = box_world([6000, 0, 0], periodic=True, ticks=160)
    events: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=events.append)
    entry = simulation.measured[1]
    for _ in range(50):
        simulation.step()
    entry.momentum = [6000, -720, 0]
    simulation.step()
    entry.momentum = [6000, 0, 0]
    assert entry.drive[1] == -720 * Q == -46080
    before = links_of(events)
    for _ in range(100):
        simulation.step()
    assert entry.drive[1] == -46080
    after = links_of(events)
    assert after[1] == before[1] == 0 and after[0] > before[0]


# -- (e) ---------------------------------------------------------------------------


def test_the_edges_of_the_rule():
    """(e)."""
    # p = 0 never steps and leaves the accumulators.
    world = box_world([6000, 3000, 0], periodic=True, ticks=100)
    events: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=events.append)
    entry = simulation.measured[1]
    replay = Replay(64, 1)
    for _ in range(10):
        replay.step([6000, 3000, 0])
        simulation.step()
    assert entry.drive == replay.drives and links_of(events) == replay.links
    held = list(entry.drive)
    entry.momentum = [0, 0, 0]
    for _ in range(20):
        simulation.step()
    assert entry.drive == held and links_of(events) == replay.links
    # A component of 0 with a residue neither advances nor steps.
    entry.momentum = [6000, 0, 0]
    for _ in range(30):
        replay.step([6000, 0, 0])
        simulation.step()
    assert entry.drive == replay.drives and entry.drive[1] == held[1]
    assert links_of(events) == replay.links and links_of(events)[1] == replay.links[1]
    # The reversal cancels first.
    world = box_world([6000, 0, 0], periodic=True, ticks=100)
    events = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=events.append)
    entry = simulation.measured[1]
    replay = Replay(64, 1)
    for _ in range(30):
        replay.step([6000, 0, 0])
        simulation.step()
    entry.momentum = [-6000, 0, 0]
    first_back = None
    for n in range(31, 61):
        st = replay.step([-6000, 0, 0])
        simulation.step()
        assert entry.drive == replay.drives, n
        if st and first_back is None:
            first_back = n
    assert first_back is not None and links_of(events) == replay.links
    # The wall from the sign change: the signed sum reaches -W first at n =
    # 30 + ceil((30 x 384000 mod 922144 + 922144) / 384000).
    residue = (30 * 384000) % 922144
    assert first_back == 30 + math.ceil((residue + 922144) / 384000) == 34
    # A refused step at a contact under `pass` pays W and does not move.
    world = box_world([6000, 0, 0], ticks=60)
    world["measured"] = [
        {**world["measured"][0], "table": {"body": "pass"}},
        {
            "position": [21, 20, 20],
            "family": "body",
            "amount": 64,
            "fixed": True,
            "table": {"body": "pass"},
        },
    ]
    events, simulation = run_in_process(world, 60)
    entry = simulation.measured[1]
    assert entry.position == (20, 20, 20) and entry.steps == 24 and links_of(events) == [0, 0, 0]
    assert entry.drive == [(60 * 384000) % 922144, 0, 0]
    assert entry.momentum == [6000, 0, 0]
    # The escape's click carries the momentum on the face (the design's axis world).
    events, simulation = run_in_process(box_world([6000, 0, 0], ticks=60), 60)
    click = [e for e in events if e["event"] == "click"][0]
    assert click["momentum"] == [6000, 0, 0] and click["detector"] == "face:+x" and click["tick"] == 51


# -- (f) ---------------------------------------------------------------------------


def test_the_refusals_by_name():
    """(f)."""
    with pytest.raises(ValueError, match="drive_b must be true or false"):
        parse_nature_beam_world(box_world([6000, 0, 0], extra={"drive_b": 1}))
    with pytest.raises(ValueError, match="drive_b must be true or false"):
        parse_nature_beam_world(box_world([6000, 0, 0], extra={"drive_b": "yes"}))
    huge = 1 << 60
    with pytest.raises(OverflowError, match="drive-b-v1"):
        parse_nature_beam_world(box_world([huge, 0, 0]))
    parse_nature_beam_world(box_world([huge, 0, 0], key=False))
    parse_nature_beam_world(box_world([6000, 0, 0], extra={"drive_b": False}))
    world = box_world([6000, 0, 0], periodic=True, ticks=10)
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    entry.drive = [MOMENTUM_BOUND - 10, 0, 0]
    with pytest.raises(OverflowError, match="drive-b-v1"):
        simulation.step()
    assert MAX_WORK_INT == 2 * MOMENTUM_BOUND + 1


# -- (g) ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("momentum", "energy"),
    [([2574, 2574, 0], 14671), ([2101, 2101, 2101], 14670), ([3640, 0, 0], 14671)],
)
def test_under_the_covariant_key_the_off_axis_body_is_admitted(momentum, energy):
    """(g), the covariant composition."""
    extra = {"covariant_readings": {"c2": [1, 3], "grain": 1}}
    if sum(1 for c in momentum if c) > 1:
        with pytest.raises(ValueError, match="components on more than one axis"):
            parse_nature_beam_world(box_world(momentum, key=False, content=207, extra=extra))
    events, simulation = run_in_process(box_world(momentum, content=207, ticks=40, extra=extra), 40)
    entry = simulation.measured[1]
    lines = [e for e in events if e["event"] == "energy"]
    assert len(lines) == 40 and all(e["energy"] == energy for e in lines)
    replay = Replay(207, 1, cap=False)
    for line in lines:
        if line["creating"]:
            replay.step(momentum)
    assert links_of(events) == replay.links and entry.drive == replay.drives
    assert sum(abs(c) for c in replay.links) >= 5
    assert set(simulation.hypotheses) == {"covariant-readings-v1", DRIVE_B_RULE}


def test_with_action_the_turn_composes_per_link_crossed():
    """(g), the turn by momentum under the key."""
    world = box_world([64, 64, 0], content=1, ticks=10, shape=65)
    world["action"] = 7
    world["families"] = [{"name": "body", "quantum": 0, "charge": 0}]
    world["measured"][0].update({"phase": 0, "phase_by_momentum": True, "position": [4, 4, 0]})
    world["shape"] = [64, 64, 1]
    events, simulation = run_in_process(world, 10)
    entry = simulation.measured[1]
    assert drive_wall([64, 64, 0], 1, 1) == 18176
    assert [e["tick"] for e in events if e["event"] == "step"] == [5, 6, 9, 10]
    assert entry.position == (6, 6, 0) and entry.axis_steps == [2, 2, 0] and entry.steps == 4
    assert links_of(events) == [2, 2, 0]
    assert entry.counts.values("action") == [(2 * 4096) % 7, (2 * 4096) % 7, 0]
    assert entry.phase == (2 * (2 * 4096 // 7)) % 64 == 36
