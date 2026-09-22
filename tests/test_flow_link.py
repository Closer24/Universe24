"""flow-link-v1, one arrival counts one Euclidean Link of its line, not one
Node (the model owner's decision of 2026-09-22, record 915 of the log of
2026-09-20; the Flow Weight Designer's design docs/designs/flow_weight/DESIGN.md
at b463ac24 (PR #839) with ALGEBRA.md and flow_weight_map.py; the
physics-rule reviewer's ADMISSIBLE of record 902), under the world key
`flow_link`, absent by default. The arrival flow every reader sums counts
each arriving row of direction D with the flow label f_D, the integer vector
nearest |p_D| D / S_1 (per component sign(D_i) x (2 |p_D| |D_i| + S_1) //
(2 S_1), one Euclidean division at load), in place of the unit label u_D
nearest |p_D| D / |D|; |p_D| is Q = 64 for the photon and a massive family's
`momentum_magnitude`. The expected integers of docs/TEST_EXPECTATIONS.md
("The flow label per Euclidean Link"), written down before the first run:

(a) the key absent reads byte for byte as main: every registered world
    outside `flow_link/` parses with `flow_link` false and the identity
    absent from its hypotheses; the flow labels of a table without the key
    ARE its labels (one array); the gate world `coupling/1b_m16` (a
    phase-less family's push on a body through the group moment, the path
    the key changes) replays at its cap to the digests of `gate_set.json`
    byte for byte, its `run.json` without a `flow_link` key; the small
    optical bar of `tests/test_optical.py` (a) (a lamp, a rest crowd, the
    wall and the push) runs 40 intervals to the digests main
    `ab96e7e899d5e7c5be58c00a0f5a02a97a337d8a` produced (the state
    `48e145edb54885d6...`, the audit `b946a5d62220786c...`, the events
    `6ff9d83d77533d67...`);
(b) the design's numbers on series K's fan (the 290 primitive directions
    within Manhattan 6, the one copy in `examples/events/lensing/make_worlds.py`):
    the fan's mean of the incidence S_1 / |D| times the weight |f_D| / Q is
    1.0003 (the exact weight |D| / S_1 gives 1.0000 by identity, the
    incidence alone 1.4355, F_L1); the worst rounding on (-2, -2, -1),
    f = (-26, -26, -13) for (-25.6, -25.6, -12.8); the beam's lines
    (24, 1, 0) -> (61, 3, 0) and (12, 1, 0) -> (59, 5, 0), the heading
    (64, 0, 0) unchanged; on every line |f_i| <= |u_i| per component and
    f_{-D} = -f_D; a massive family's magnitude in Q's place: (1, 1, 0) at
    |p_D| = 10 gives (5, 5, 0) where the label is (7, 7, 0), (2, 1, 0) at Q
    gives (43, 21, 0) where u is (57, 29, 0);
(c) the engine reads f_D under the key and u_D without it, on both flow
    sums: (1) the rows' push (`CrowdMoments`, `optical_turn`): the turn
    world of `tests/test_optical.py` (b) with the m row of amount 1 at
    (1, 1, 0) on the diagonal (1, 1, 0), arriving with the light row at
    (2, 1, 0) in interval 1: the light row's whole momentum after the
    interval (conserved across the turn) is Q d content u_x - n x w x V =
    (16384, 0, 0) - 221 x V, V = (32, 32, 0) under the key, so P =
    (9312, -7072, 0); (45, 45, 0) without it, P = (6439, -9945, 0);
    (2) a body's push through the group moment: the fan-ray world of
    `tests/test_nature_beam_push.py` (g) (a source of content 4 releasing
    on (2, 1, 0), a probe of content 5 at (4, 2, 0)) reads every push
    -5 x 4 x (43, 21, 0) = (-860, -420, 0) under the key and `pushed`
    (-18920, -9240, 0) after 22 reads, against (-1140, -580, 0) and
    (-25080, -12760, 0) without; (3) a paid ray's push stays its label
    (the momentum a click moves, record 902): the lamp-and-reader world of
    the same file (f) under the key reads the pushes 512, 448, 512 ... and
    the lamp's momentum -15296 exactly as without, the books balanced;
    (4) the clock's word unchanged: the bar of `tests/test_optical.py` (a)
    under the key walks the same x chain as without it (the crowd at rest
    carries the zero label; the wall reads the age moment, not the flow);
    (5) the record: the identity `flow-link-v1` under `hypotheses` (after
    `optical-v1`, before `binding-v1`) and `flow_link: true` in `run.json`
    under the key alone; the key stands alone (a world without `optical`
    declares it and carries the identity);
(d) the refusals and the edge of the working bound: `flow_link` 1, "true",
    null or [] refused at load naming flow-link-v1; the flow label's one
    product 2 |p_D| |D_i| + S_1 tested by division before it is formed:
    the magnitude 2^62 - 1 on the heading (1, 0, 0) passes with the label
    (2^62 - 1, 0, 0) (2 (2^62 - 1) + 1 = 2^63 - 1, the bound itself), the
    magnitude 2^62 refused naming flow-link-v1 and the working bound.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import pytest

from event_universe.core.integer import MAX_WORK_INT
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import direction_flight, flow_label, nature_beam_tables
from event_universe.events.run import execute_nature_beam_run
from event_universe.events.world import BINDING_RULE, FLOW_LINK_RULE, OPTICAL_RULE, Q
from event_universe.world_loading import load_world
from tests import test_nature_beam_push as push_tests
from tests import test_optical as optical_tests

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "events"
GATE_SET = EXAMPLES / "gate_set.json"
FLOW_LINK_WORLDS = EXAMPLES / "flow_link"
# The gate world whose path the key changes: a phase-less family's push on a
# body through the group moment.
GATE_WORLD = "coupling/1b_m16.json"
# The digests main ab96e7e8 produced for the optical bar (a) (the first 16
# hex digits of each sha256; the run through `execute_nature_beam_run` at
# 40 intervals, the source the world's JSON).
BAR_DIGESTS = {
    "state_sha256": "48e145edb54885d6",
    "audit_sha256": "b946a5d62220786c",
    "events_sha256": "6ff9d83d77533d67",
}
DESIGN_MEAN = 1.0003
DESIGN_INCIDENCE = 1.4355


def load_script(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def digests(folder: Path) -> dict[str, str]:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    return {
        "state_sha256": hashlib.sha256((folder / "state.json").read_bytes()).hexdigest(),
        "audit_sha256": hashlib.sha256(json.dumps(record.get("audit", [])).encode("utf-8")).hexdigest(),
        "events_sha256": hashlib.sha256((folder / "events.jsonl").read_bytes()).hexdigest(),
    }


def series_k_fan() -> list[tuple[int, int, int]]:
    """The 290 directions, from the one copy of the fan."""
    generator = load_script("lensing_make_worlds_flow_link", EXAMPLES / "lensing" / "make_worlds.py")
    return [tuple(v) for v in generator.FAN]  # type: ignore[misc]


def with_key(document: dict[str, object], key: bool | object = True) -> dict[str, object]:
    return {**document, "flow_link": key}


# -- (a) ---------------------------------------------------------------------------


def test_the_key_absent_reads_byte_for_byte_as_main(tmp_path):
    """(a)."""
    checked = 0
    for path in sorted(EXAMPLES.rglob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(document, dict) or "format" in document or path.parent == FLOW_LINK_WORLDS:
            continue
        world = load_world(path.read_bytes(), base_dir=path.parent, root=EXAMPLES).world
        assert world.flow_link is False, path
        assert FLOW_LINK_RULE not in world.hypotheses, path
        checked += 1
    assert checked >= 100
    table = direction_flight(((0, 0, 0), (0, 0, 0), (1, 0, 0), (2, 1, 0)))
    assert table.flow_labels is table.labels
    gate = json.loads(GATE_SET.read_text(encoding="utf-8"))
    entry = next(w for w in gate["worlds"] if w["path"] == GATE_WORLD)
    path = EXAMPLES / entry["path"]
    source = path.read_bytes()
    loaded = load_world(source, base_dir=path.parent, root=EXAMPLES)
    out = tmp_path / "gate"
    out.mkdir()
    execute_nature_beam_run(loaded.world, source, out, "test", entry["cap"])
    assert digests(out) == entry["digests"]
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert "flow_link" not in record and FLOW_LINK_RULE not in record["hypotheses"]
    # The small optical bar against main's digests.
    document = optical_tests.bar(1)
    out = tmp_path / "bar"
    out.mkdir()
    execute_nature_beam_run(
        parse_nature_beam_world(document), json.dumps(document).encode("utf-8"), out, "test", 40
    )
    assert {k: v[:16] for k, v in digests(out).items()} == BAR_DIGESTS
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert "flow_link" not in record and record["hypotheses"] == ["amplitude-v1", OPTICAL_RULE]


# -- (b) ---------------------------------------------------------------------------


def test_the_fans_mean_of_incidence_times_weight_is_the_designs():
    """(b)."""
    fan = series_k_fan()
    assert len(fan) == 290
    table = direction_flight(tuple(fan), True)
    assert table.flow_labels is not table.labels
    incidence, product, exact = 0.0, 0.0, 0.0
    for vector, f, u in zip(fan, table.flow_labels.tolist(), table.labels.tolist(), strict=True):
        s1 = sum(abs(c) for c in vector)
        norm = math.sqrt(sum(c * c for c in vector))
        incidence += s1 / norm
        product += (s1 / norm) * math.sqrt(sum(c * c for c in f)) / Q
        exact += (s1 / norm) * (norm / s1)
        assert all(abs(fi) <= abs(ui) for fi, ui in zip(f, u, strict=True)), vector
        assert flow_label(tuple(-c for c in vector), Q) == tuple(-c for c in f)
        assert f == list(flow_label(vector, Q))
    assert abs(product / 290 - DESIGN_MEAN) <= 0.00005
    assert abs(exact / 290 - 1.0) < 1e-12
    assert abs(incidence / 290 - DESIGN_INCIDENCE) <= 0.00005
    assert flow_label((-2, -2, -1), Q) == (-26, -26, -13)
    assert flow_label((24, 1, 0), Q) == (61, 3, 0) and flow_label((12, 1, 0), Q) == (59, 5, 0)
    assert flow_label((1, 0, 0), Q) == (64, 0, 0) and flow_label((0, 0, 0), Q) == (0, 0, 0)
    assert flow_label((2, 1, 0), Q) == (43, 21, 0) and flow_label((1, 1, 0), Q) == (32, 32, 0)
    assert flow_label((1, 1, 0), 10) == (5, 5, 0)
    # A massive family's flow labels on its own magnitude (matter, |p_D| =
    # 10): the tables of the massive bar under the key.
    world = parse_nature_beam_world(with_key(optical_tests.matter_bar(1)))
    matter = nature_beam_tables(world).family_flights[0]
    diagonal = int(next(i for i, v in enumerate(world.directions) if tuple(v) == (1, 1, 0)))
    assert matter.labels[diagonal].tolist() == [7, 7, 0]
    assert matter.flow_labels[diagonal].tolist() == [5, 5, 0]
    plain = nature_beam_tables(parse_nature_beam_world(optical_tests.matter_bar(1))).family_flights[0]
    assert plain.flow_labels is plain.labels


# -- (c) ---------------------------------------------------------------------------


def diagonal_turn_world(key: bool) -> dict[str, object]:
    """The turn world of `tests/test_optical.py` (b) with the m row (amount
    1) at (1, 1, 0) on the diagonal (1, 1, 0): its first Link is +x, so it
    arrives at (2, 1, 0) with the light row in interval 1."""
    document = optical_tests.turn_world()
    diagonal = next(
        i
        for i, v in enumerate(document["directions"])
        if v == [1, 1, 0]  # type: ignore[arg-type]
    )
    transit = document["in_transit"]
    transit[1] = {  # type: ignore[index]
        **transit[1],  # type: ignore[dict-item]
        "position": [1, 1, 0],
        "direction": optical_tests.HEADING_OFFSET + 6 + diagonal,
        "amount": 1,
    }
    return with_key(document) if key else document


def whole_momentum(simulation: NatureBeamSimulation) -> list[int]:
    light = simulation.stores[0]
    unit = simulation.tables.flight.labels[int(light.direction[0])]
    return [
        int(a) * Q * 4 * 1 + int(b)
        for a, b in zip(unit.tolist(), (light.push_x[0], light.push_y[0], light.push_z[0]), strict=True)
    ]


def test_the_engine_reads_the_flow_label_under_the_key():
    """(c) (1) and (5): the rows' push."""
    for key, flow, momentum in (
        (True, (32, 32, 0), [9312, -7072, 0]),
        (False, (45, 45, 0), [6439, -9945, 0]),
    ):
        simulation = NatureBeamSimulation(parse_nature_beam_world(diagonal_turn_world(key)))
        vectors = simulation.tables.flight.vectors
        crowd_direction = int(simulation.stores[1].direction[0])
        assert vectors[crowd_direction].tolist() == [1, 1, 0]
        table = simulation.tables.family_flights[1]
        assert table.flow_labels[crowd_direction].tolist() == list(flow)
        simulation.step()
        assert simulation.books()["balanced"]
        light, crowd = simulation.stores[0], simulation.stores[1]
        assert light.size == 1 and crowd.size == 1
        assert (
            light.coordinates(light.node[:1])[0][0] == 2 and crowd.coordinates(crowd.node[:1])[0][0] == 2
        )
        assert [16384 - 221 * flow[0], -221 * flow[1], 0] == momentum
        assert whole_momentum(simulation) == momentum
        assert (FLOW_LINK_RULE in simulation.hypotheses) is key
        assert (FLOW_LINK_RULE in simulation.world.hypotheses) is key
    hypotheses = parse_nature_beam_world(diagonal_turn_world(True)).hypotheses
    assert hypotheses.index(OPTICAL_RULE) < hypotheses.index(FLOW_LINK_RULE)
    # The key stands alone: without `optical` the world declares it and
    # carries the identity; with a held paid family the identity precedes
    # binding-v1.
    alone = parse_nature_beam_world(with_key(optical_tests.turn_world(None)))
    assert alone.flow_link and alone.optical is None and alone.hypotheses[-1] == FLOW_LINK_RULE
    assert BINDING_RULE not in alone.hypotheses


def test_a_bodys_push_reads_the_flow_label_and_a_paid_ray_keeps_its_label():
    """(c) (2) and (3)."""
    fan_world = push_tests.bar(
        [push_tests.source(release_on=push_tests.FAN), push_tests.probe(position=[4, 2, 0])],
        shape=[9, 5, 1],
        boundary={"z": "periodic"},
        directions=[push_tests.FAN],
    )
    for key, push, pushed in (
        (True, [-860, -420, 0], [-18920, -9240, 0]),
        (False, [-1140, -580, 0], [-25080, -12760, 0]),
    ):
        simulation, records = push_tests.run(with_key(fan_world) if key else fan_world)
        reads = push_tests.reads_of(records, 2)
        assert [tick for tick, _, _ in reads] == list(range(9, 31))
        assert all(amount == 4 and read == push for _, amount, read in reads), key
        assert simulation.measured[2].pushed == pushed
        assert (FLOW_LINK_RULE in simulation.hypotheses) is key
    lamp = {
        "position": [0, 0, 0],
        "family": "light",
        "amount": 1 << 23,
        "fixed": True,
        "lamp": {"wheel": [1, 64], "rate": [1, 1], "directions": [push_tests.PLUS_X]},
    }
    reader = push_tests.probe(table={"light": "read"})
    world = with_key(push_tests.bar([lamp, reader], release=[0, 1]))
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), records.append)
    for _ in range(30):
        simulation.step()
        books = simulation.books()
        assert books["balanced"]
        momentum = books["momentum"]
        lamp_momentum = simulation.measured[1].momentum
        assert [
            a + b + c
            for a, b, c in zip(lamp_momentum, momentum["transit"], momentum["escaped"], strict=True)
        ] == [0, 0, 0], simulation.tick
    reads = push_tests.reads_of(records, 2)
    assert [push[0] for _, _, push in reads] == [512, 448] + [512] * 18
    assert simulation.measured[2].pushed == [10176, 0, 0]
    assert simulation.measured[1].momentum == [-15296, 0, 0]
    assert FLOW_LINK_RULE in simulation.hypotheses


def x_chain(document: dict[str, object], ticks: int) -> list[int]:
    simulation = NatureBeamSimulation(parse_nature_beam_world(document))
    found = []
    for _ in range(ticks):
        simulation.step()
        light = simulation.stores[0]
        row = optical_tests.first_row(light)
        found.append(-1 if row is None else int(light.coordinates(light.node[row : row + 1])[0][0]))
    return found


def test_the_clocks_word_and_the_record(tmp_path):
    """(c) (4) and (5)."""
    plain = x_chain(optical_tests.bar(1), 40)
    keyed = x_chain(with_key(optical_tests.bar(1)), 40)
    assert plain == keyed
    # Tick 1 births the row at x = 0; the chain of (a) from tick 2.
    assert plain[0] == 0 and plain[1:7] == [1, 1, 2, 2, 3, 3] and plain[7:19] == [4] * 12
    document = with_key(optical_tests.bar(1))
    out = tmp_path / "keyed"
    out.mkdir()
    execute_nature_beam_run(
        parse_nature_beam_world(document), json.dumps(document).encode("utf-8"), out, "test", 40
    )
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert record["flow_link"] is True
    assert record["hypotheses"] == ["amplitude-v1", OPTICAL_RULE, FLOW_LINK_RULE]


# -- (d) ---------------------------------------------------------------------------


def test_the_refusals_and_the_edge_of_the_working_bound():
    """(d)."""
    for bad in (1, "true", None, []):
        with pytest.raises(ValueError, match="flow_link must be true or false"):
            parse_nature_beam_world(with_key(optical_tests.turn_world(), bad))
    assert parse_nature_beam_world(with_key(optical_tests.turn_world(), False)).flow_link is False
    edge = (1 << 62) - 1
    assert 2 * edge + 1 == MAX_WORK_INT
    assert flow_label((1, 0, 0), edge) == (edge, 0, 0)
    with pytest.raises(OverflowError, match="flow-link-v1's flow label .* exceeds the working bound"):
        flow_label((1, 0, 0), edge + 1)
    with pytest.raises(OverflowError, match="flow-link-v1"):
        flow_label((2, 1, 0), edge)
