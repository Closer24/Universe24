"""The layer of the amplitude law (`amplitude-v1`, the model owner,
2026-09-20; the design, docs/designs/amplitude-v1/DESIGN.md sections 3, 5 and 7;
docs/BEAM_LAW.md note 37): the reading `sum` at the record's scope, the
offers, the ladder at the record's completion normalised by its total with
the rungs at the nearest integer, and the gathers (the world's list of
clicks), on the worlds of series L (`examples/events/amplitude/make_worlds.py`).
The expected integers of docs/TEST_EXPECTATIONS.md ("The amplitude law: the
layer"), written down before the first run:

(a) the design's tests 1 and 3: over the lamp's first 64 records (by birth
    ordinal, the record's identity; born in the ticks 1 .. 65 since the
    fraction-free law of 2026-09-20, the exact clock stalling once at
    tick 3) the gathers per port equal the design's table (`mz_equal` D1 64, D2 0;
    `mz_half` 0, 64; `mz_quarter` 32, 32; `mz_balanced` 64, 0; `mz_345` 63,
    1; `mz_unequal_f0` 64, 0; `mz_unequal_f8` 32, 32; `mz_unequal_f16` 0,
    64; `ev_29` absorber 32, D1 17, D2 15; `ev_169` 32, 16, 16), one gather
    per birth, every one complete by tick 76; every record's `total` (in
    the unit 2^58, the square of one row of amount 1 at the identity
    rotation) is one of 8 values between 65448/65536 and 65773/65536 on
    every world (unitarity: the sum over the ports does not see the split;
    the tables' rounding depends on u), so the design's bound 0.0019 holds
    for u = 0 alone and is pinned as the design's value, marked failing,
    beside the measured bound 237/65536; the gather names the family,
    the record, u, the chosen set with its arm and channel, the weight as
    a reduced pair and the cells with their rungs, the last N;
(b) the design's test 8, determinism: the same world twice gives the same
    list of gathers; the rung moved by the (3, 4) split sends u = 63 to D2
    where the (20, 21) split sends it to D1;
(c) the review's B1, a split is not a click: on `mz_quarter` at tick 11
    the two arms of one record reach the splitter in antiphase (the phases
    u and u + 32, the crowd's pointer 0) and both are split (two `split`
    lines, no `pass` line at the splitter over the run); on
    `mz_unequal_f8` at tick 11 the rows of two records reach it together
    and both are split; a `sum` port takes no pointer gate either (no
    `pass` line at D1 or D2 on any of the ten worlds);
(d) the design's test 2 on `slits_low` against the generator's reading of
    one birth (the design's `slits_read.py`, `expectations.json` under
    `two_slits`, written before the run): the first record's cells are the
    80 sets of the reading in the layer's order with the reading's rungs;
    its chosen cell's weight and its total equal the reading's fractions
    (the total 847181/745472: the wall's three rows 3/5, the fans 2/5 and
    the cross terms of paths meeting at one Node; a face of 24 Nodes hit
    sums its Nodes' squares, coherent within a Node and incoherent across
    Nodes, the decision of 2026-09-20 on the owner's point 5); every one
    of the 64 births gathers by tick 214 (213 until the fraction-free law
    of 2026-09-20: the 64th record is born at tick 65); the clicks per set over the 64
    births equal the reading's on every one of the 80 sets: the wall's
    three Nodes 11, 12 and 11 (34, the share 0.528), fourteen pixels
    (15, 0.244; screen_61 twice), the faces 8 and 7 (15, 0.228); the
    tables' rounding (C^2 + S^2 within 361 of 65536) makes the weights
    depend on u by parts in 10^3 (32 of the 64 records share the record
    u = 0's cells, 3 distinct cell lists) without moving a rung here;
    the design's "wall 3/5, screen 2/5" is not this geometry's reading:
    the freed fans reach the open faces in y;
(e) the design's test 7, the gate set: the seventeen registered worlds
    listed in GATE_SET parse without the key (`amplitude` false, no
    `amplitude-v1` identity), the byte-identity of their replays being the
    evidence of docs/VALIDATION.md;
(f) the design's test 10, the register's replay: `tools/amplitude_path.py`
    replays the record lines of a run of `mz_equal` and of `ev_29` through
    the layer and its list equals `run.json`'s `world`;
(g) the review's S1: the pair form is bounded at the parse by
    (age_bound + 1) x n <= 2^62 - 1 ([2^61, 5] refused on a bar of
    age_bound 100 naming the key), and the largest admitted numerator reads
    the exact floor after 5 intervals (n mod 64);
(h) the review's S3: the merge returns the units cancelled per (record,
    direction, content per unit), two contents at two Nodes booked apart;
(i) the review's S4: a lamp that cannot pay one quantum on each of its
    directions refuses the birth naming the lamp (K 2, content 1 on two
    directions, refused at tick 2), and one that can births the record
    2^32 + 1 of two rows (content 2);
(j) the `record` lines a `sum` set writes at a gather carry the reading's
    scope `record`, the pointer per label and the square added to the
    set's record;
(k) the review's B1, one birth per rebirth: a lamp into a `sum`
    re-emitter of two directions (the detector `gate`) and two absorbers:
    every record gathers at the re-emitter (its one offer), and what the
    re-emitter re-creates is ONE new record of two rows (two `split` lines
    with `rebirth`, one `birth` in the layer), which gathers once with the
    cells a and b, the rungs 32 and 64, 64 such gathers;
(l) the review's B2, a free family's rows keep the unkeyed path: a source
    of a free family of amount 3 into a `rerelease` on two directions comes
    out 1 + 2 (the apportioning) with the key as without it, the rows and
    the `rerelease` lines the same;
(m) the review's S3 and S5, refused at load: a `phase_window` on a
    `rerelease` entry whose Node reads no `sum` set under the key (dead: a
    split takes no gate), and a detector named `measured:3` (the layer's
    reserved prefix);
(n) the record's total re-pinned at the tables (the reviewer): on the
    (20, 21) worlds the total of the record u is
    (1681 q[u + 16] + q[u + 32]) / (1682 x 65536) with q[p] = C[p]^2 +
    S[p]^2, exactly, for every u; the gather of `mz_equal`'s first record
    carries the content 41 and the momentum [2624, 0, 0] of its click
    (the review's S1).
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.amplitude import UNIT
from event_universe.events.nature_beam import NatureBeamStore
from event_universe.events.run import execute_nature_beam_run
from event_universe.events.world import AMPLITUDE_RULE
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
N = 64
BIRTHS = 64
# The design's bound on a record's total (mz.txt, 1 within 0.0019) and the
# measured one: over the 64 births the total takes 8 values, 65448/65536
# to 65773/65536 (the tables' rounding depends on u), on every one of the
# ten worlds (unitarity: the sum over the ports does not see the split).
DESIGN_TOTAL_BOUND = Fraction(19, 10000)
MEASURED_TOTAL_BOUND = Fraction(237, 65536)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


GENERATOR = load("amplitude_make_worlds", ROOT / "examples" / "events" / "amplitude" / "make_worlds.py")
EXPECTATIONS = json.loads(
    (ROOT / "examples" / "events" / "amplitude" / "expectations.json").read_text("utf-8")
)
# The gate set (the owner's change of 2026-09-20 to the design's test 7): one
# registered world per table rule, key and family kind, replayed
# byte-identical without the key after commit (i) and at the end
# (docs/VALIDATION.md). Per world what it covers.
GATE_SET = {
    "two_slits.json": "rerelease on 91 directions, a lamp, the wave reading, z periodic",
    "bell/read.json": "the read form of phase_window, pass, a free and a paid family",
    "bell/a0_b8.json": "measure under phase_window (the chooser), a lamp",
    "weak/j2_filter.json": "phase_width on measure",
    "weak/w_exchange.json": "become, lifetime, a charged paid family",
    "weak/j3_neutron_free.json": "columns, lifetime, become, the beam reading",
    "nucleus/deuteron_1.json": "columns and lifetime on free families",
    "lensing/mass_meeting.json": "meeting, read, measure",
    "bohr/r2.json": "action (the turn by momentum)",
    "hubble/coasting_age.json": "read, measure, pass with reads",
    "coupling/7_pp.json": "free families alone, z periodic",
    "catalog/lamp_mirror_screen.json": "rerelease with phase_window, a lamp",
    "catalog/sun_planet.json": "rerelease with a free crowd",
    "heisenberg/w3_beam.json": "the beam reading on a rerelease world",
    "one_content.json": "one free family, open faces",
    "redshift/age.json": "pass with reads on a free family",
    "detector/periodic_z_node.json": "in_transit, a paid family, z periodic",
}


def run_world(world: dict[str, object], ticks: int | None = None) -> NatureBeamSimulation:
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    for _ in range(int(world["ticks"]) if ticks is None else ticks):  # type: ignore[call-overload]
        simulation.step()
    return simulation


def observed(world: dict[str, object]) -> tuple[NatureBeamSimulation, list[dict[str, object]]]:
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=lines.append)
    for _ in range(int(world["ticks"])):  # type: ignore[call-overload]
        simulation.step()
    return simulation, lines


def births(simulation: NatureBeamSimulation) -> list[dict[str, object]]:
    """The gathers of the lamp's first 64 records, by birth ordinal (the
    record's identity, number 1's records 2^32 + 1 .. 2^32 + 64): since the
    fraction-free law of 2026-09-20 a paid lamp's exact clock stalls (on
    these worlds once, at tick 3), so the 64 births span the ticks 1 .. 65
    and a tick window is not a count of births."""
    assert simulation.layer is not None
    first = (1 << 32) + 1
    return sorted(
        (g for g in simulation.layer.gathers if first <= int(g["record"]) < first + BIRTHS),  # type: ignore[call-overload]
        key=lambda g: int(g["record"]),  # type: ignore[call-overload]
    )


def clicks(gathers: list[dict[str, object]]) -> dict[str, int]:
    return dict(Counter(str(g["chosen"][0][0]) for g in gathers if g["chosen"]))  # type: ignore[index]


def test_the_mach_zehnder_and_elitzur_vaidman_worlds_click_as_the_design_says():
    """(a)."""
    expected = EXPECTATIONS["mach_zehnder"]
    for name, world in GENERATOR.mach_zehnder_worlds().items():
        simulation = run_world(world)
        gathers = births(simulation)
        assert len(gathers) == BIRTHS, name
        assert sorted(int(g["u"]) for g in gathers) == list(range(N)), name  # type: ignore[call-overload]
        found = clicks(gathers)
        wanted = {k: v for k, v in expected[name]["clicks"].items() if v}
        assert found == wanted, (name, found, wanted)
        assert max(int(g["tick"]) for g in gathers) <= 76, name  # type: ignore[call-overload]
        totals = {
            Fraction(int(gather["total"][0]), int(gather["total"][1]) * UNIT)  # type: ignore[index]
            for gather in gathers
        }
        assert len(totals) == 8 and min(totals) == Fraction(65448, 65536), name
        assert max(totals) == Fraction(65773, 65536), name
        assert all(abs(total - 1) <= MEASURED_TOTAL_BOUND for total in totals), name
    simulation = run_world(GENERATOR.mach_zehnder("mz_equal"))
    first = births(simulation)[0]
    assert first["family"] == "light" and first["record"] == (1 << 32) + 1 and first["u"] == 0
    assert first["chosen"] == [["D1", 0, "0"]]
    assert first["unit"] == UNIT == 1 << 58
    weight = first["weight"]
    assert isinstance(weight, list) and Fraction(*weight) == Fraction(  # type: ignore[arg-type]
        int(first["total"][0]) * 1681,
        int(first["total"][1]) * 1682,  # type: ignore[index]
    )
    assert [cell[1] for cell in first["cells"]] == [64, 64]  # type: ignore[index]
    assert [cell[0][0][0] for cell in first["cells"]] == ["D1", "D2"]  # type: ignore[index]


def test_every_total_is_the_tables_formula():
    """(n): the design's bound 0.0019 held for u = 0 alone; the total is
    the tables' formula (the reviewer), pinned exactly for every u."""
    cosines, sines = phase_cosines(N), phase_sines(N)
    q = [cosines[p] ** 2 + sines[p] ** 2 for p in range(N)]
    gathers = births(run_world(GENERATOR.mach_zehnder("mz_equal")))
    for gather in gathers:
        u = int(gather["u"])  # type: ignore[call-overload]
        total = Fraction(int(gather["total"][0]), int(gather["total"][1]) * UNIT)  # type: ignore[index]
        assert total == Fraction(1681 * q[(u + 16) % N] + q[(u + 32) % N], 1682 * 65536), u
        assert abs(total - 1) <= MEASURED_TOTAL_BOUND
    first = gathers[0]
    assert first["content"] == 41 and first["momentum"] == [2624, 0, 0]
    assert first["node"] == [[4, 3, 0]]


def test_the_same_world_twice_gives_the_same_list_and_a_moved_rung_moves_u():
    """(b)."""
    once = births(run_world(GENERATOR.mach_zehnder("mz_equal")))
    twice = births(run_world(GENERATOR.mach_zehnder("mz_equal")))
    assert once == twice
    moved = births(run_world(GENERATOR.mach_zehnder("mz_345", splitter=GENERATOR.PYTHAGOREAN_5)))
    by_u = {int(g["u"]): g["chosen"][0][0] for g in moved}  # type: ignore[call-overload, index]
    assert by_u[63] == "D2" and by_u[62] == "D1"
    assert {int(g["u"]): g["chosen"][0][0] for g in once}[63] == "D1"  # type: ignore[call-overload, index]
    assert [cell[1] for cell in moved[0]["cells"]] == [63, 64]  # type: ignore[index]


def splitter_number(world: dict[str, object]) -> int:
    measured = world["measured"]
    assert isinstance(measured, list)
    for index, entry in enumerate(measured):
        if entry["position"] == [3, 3, 0]:
            return index + 1
    raise AssertionError("no splitter")


def test_a_split_is_not_a_click_and_takes_no_pointer_gate():
    """(c)."""
    for name, tick_of_two in (("mz_quarter", 11), ("mz_unequal_f8", 11)):
        world = GENERATOR.mach_zehnder_worlds()[name]
        splitter = splitter_number(world)
        _, lines = observed(world)
        at_splitter = [line for line in lines if line.get("measured") == splitter]
        passes = [line for line in at_splitter if line["event"] == "pass"]
        assert passes == [], (name, passes[:2])
        splits = [
            line for line in at_splitter if line["event"] == "split" and line["tick"] == tick_of_two
        ]
        assert len(splits) == 2, (name, splits)
        assert [s["absorbed"] for s in splits] == [1, 1] and [s["born"] for s in splits] == [41, 41]
        records = {s["record"] for s in splits}
        assert len(records) == (1 if name == "mz_quarter" else 2), (name, records)
        if name == "mz_quarter":
            arrivals = [
                line for line in at_splitter if line["event"] == "rerelease" and line["tick"] == 11
            ]
            phases = sorted(row[4] for line in arrivals for row in line["rows"])  # type: ignore[union-attr]
            assert (phases[1] - phases[0]) % N == N // 2, phases
    for name, world in GENERATOR.mach_zehnder_worlds().items():
        _, lines = observed(world)
        ports = [
            line
            for line in lines
            if line.get("event") == "pass" and line.get("detector") in ("D1", "D2", "absorber")
        ]
        assert ports == [], (name, ports[:2])


def test_the_two_slits_at_a_low_rate_against_the_reading_of_one_birth():
    """(d)."""
    reading = EXPECTATIONS["two_slits"]
    simulation = run_world(GENERATOR.two_slits_low())
    gathers = births(simulation)
    assert len(gathers) == BIRTHS
    # The 64th record is born at tick 65 (the exact clock's stall at tick
    # 3) and gathers at 214 (213 for a birth at tick 64 until the
    # fraction-free law of 2026-09-20).
    assert max(int(g["tick"]) for g in gathers) == 214  # type: ignore[call-overload]
    first = gathers[0]
    assert first["u"] == 0 and first["born"] == 1
    names = [cell[0][0][0] for cell in first["cells"]]  # type: ignore[index]
    assert len(names) == reading["sets"] == 80
    assert names == [name for name in simulation.layer.names if name in reading["weights"]]  # type: ignore[union-attr]
    # A click of a face lands at one of its Nodes, chosen within the cell.
    faces = [g for g in gathers if str(g["chosen"][0][0]).startswith("face:")]  # type: ignore[index]
    assert len(faces) == 15 and all(abs(g["node"][0][1] - 60) >= 60 for g in faces)  # type: ignore[index]
    cumulative, rungs = 0, []
    for name in names:
        cumulative += reading["clicks"].get(name, 0)
        rungs.append(cumulative)
    assert [cell[1] for cell in first["cells"]] == rungs  # type: ignore[index]
    chosen = first["chosen"][0][0]  # type: ignore[index]
    assert chosen == "measured:223"
    weight = Fraction(int(first["weight"][0]), int(first["weight"][1]) * UNIT)  # type: ignore[index]
    assert weight == Fraction(reading["weights"][chosen])
    total = Fraction(int(first["total"][0]), int(first["total"][1]) * UNIT)  # type: ignore[index]
    assert total == Fraction(reading["total"])
    assert reading["clicks_by_kind"] == {"wall": 34, "screen": 15, "faces": 15}
    assert reading["face_nodes"] == {"face:+y": 24, "face:-y": 24}
    assert total == Fraction(847181, 745472)
    assert clicks(gathers) == reading["clicks"]
    assert first["node"] == [[7, 58, 0]] and first["content"] == 1
    distinct = {json.dumps(g["cells"]) for g in gathers}
    assert len(distinct) == 3
    assert sum(1 for g in gathers if g["cells"] == first["cells"]) == 32


def test_the_gate_set_parses_with_the_key_deleted():
    """(e)."""
    assert len(GATE_SET) == 17
    for name in GATE_SET:
        path = ROOT / "examples" / "events" / name
        world = load_world(path.read_bytes(), base_dir=path.parent).world
        assert world.recorded is any(entry.lamp is not None for entry in world.measured), name
        assert (AMPLITUDE_RULE in world.hypotheses) is world.recorded, name


def test_the_register_replays_through_the_reading_tool(tmp_path: Path):
    """(f)."""
    tool = load("amplitude_path", ROOT / "tools" / "amplitude_path.py")
    for name in ("mz_equal", "ev_29"):
        world = GENERATOR.mach_zehnder_worlds()[name]
        out = tmp_path / name
        out.mkdir()
        execute_nature_beam_run(
            parse_nature_beam_world(world), json.dumps(world).encode(), out, "test", 30
        )
        record = json.loads((out / "run.json").read_text("utf-8"))
        layer, gathers = tool.replay(out)
        assert gathers == record["world"]
        assert len(gathers) >= 18 and layer.report()["open"] == record["layer"]["open"]


def test_the_pair_form_is_bounded_at_the_parse():
    """(g)."""
    split_tests = load("amplitude_split_tests", ROOT / "tests" / "test_amplitude_split.py")
    bar = split_tests.bar
    bound = (1 << 62) - 1
    largest = bound // 101
    with pytest.raises(
        ValueError, match=r"phase_per_link \[2305843009213693952, 5\]: \(age_bound \+ 1\) x n"
    ):
        parse_nature_beam_world(bar([1 << 61, 5]))
    simulation = run_world(bar([largest, 5]))
    rows = simulation.stores[0].rows()
    assert len(rows) == 1 and rows[0].phase == (5 * largest // 5) % N == largest % N


def test_the_cancel_is_booked_per_content():
    """(h)."""
    store = NatureBeamStore((3, 3, 1))
    rows = [(4, 5, 3, 1), (4, 37, 1, 1), (5, 9, 2, 3), (5, 41, 2, 3)]
    count = len(rows)
    store.append(
        node=np.array([r[0] for r in rows]),
        direction=np.full(count, 2),
        age=np.full(count, 3),
        phase=np.array([r[1] for r in rows]),
        number=np.full(count, 1),
        amount=np.array([r[2] for r in rows]),
        content=np.array([r[3] for r in rows]),
        arrival=np.zeros(count, dtype=np.int64),
        record=np.full(count, 7),
        branch=np.zeros(count, dtype=np.int64),
        multiplicity=np.ones(count, dtype=np.int64),
    )
    removed = store.merge(N)
    assert removed == {(7, 2, 1): 2, (7, 2, 3): 4}
    left = [(r.node, r.phase, r.amount, r.content) for r in store.rows()]
    assert left == [((1, 1, 0), 5, 2, 1)]


def test_a_lamp_short_of_one_quantum_per_direction_is_refused():
    """(i)."""

    def lamp(content: int) -> dict[str, object]:
        return {
            "law": "beam",
            "model_id": "amplitude-short-lamp",
            "shape": [5, 5, 1],
            "boundary": {"z": "periodic"},
            "ticks": 4,
            "K": 2,
            "N": N,
            "release": [0, 1],
            "suspension": 0,
            "families": [{"name": "light", "quantum": 1}],
            "measured": [
                {
                    "position": [0, 0, 0],
                    "family": "light",
                    "amount": content,
                    "fixed": True,
                    "lamp": {"rate": [1, 1], "directions": [[1, 0, 0], [0, 1, 0]]},
                }
            ],
        }

    short = NatureBeamSimulation(parse_nature_beam_world(lamp(1)))
    short.step()
    with pytest.raises(ValueError, match=r"lamp of measured event 1 at \[0, 0, 0\] holds 1 of light"):
        short.step()
    whole = run_world(lamp(2), 2)
    rows = whole.stores[0].rows()
    assert sorted((r.record, r.multiplicity, r.amount) for r in rows) == [((1 << 32) + 1, 2, 1)] * 2
    assert whole.layer is not None and whole.layer.born == 1


def test_a_sum_set_records_the_square_at_the_record_scope():
    """(j)."""
    simulation, lines = observed({**GENERATOR.mach_zehnder("mz_equal"), "ticks": 12})
    records = [line for line in lines if line.get("event") == "record" and line.get("reading") == "sum"]
    assert records, "no sum record line"
    first = records[0]
    assert first["scope"] == "record" and first["detector"] == "D1" and first["of"] == (1 << 32) + 1
    x, y = first["pointer"]  # type: ignore[misc]
    assert first["record"] == x * x + y * y and first["multiplicity"] == 1682
    assert simulation.detector_sets[0].scope == "record"
    assert simulation.detector_sets[2].scope == "crowd"


def rebirth_world() -> dict[str, object]:
    """A lamp into a `sum` re-emitter of two directions and two absorbers."""
    return {
        "law": "beam",
        "model_id": "amplitude-rebirth",
        "shape": [5, 3, 1],
        "boundary": {"z": "periodic"},
        "ticks": 80,
        "K": 1 << 20,
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "light", "quantum": 1}],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "light",
                "amount": 1 << 20,
                "fixed": True,
                "lamp": {"rate": [1, 1], "directions": [[1, 0, 0]]},
            },
            {
                "position": [2, 0, 0],
                "family": "light",
                "amount": 1,
                "fixed": True,
                "table": {"light": "rerelease"},
                "directions": [[1, 0, 0], [0, 1, 0]],
            },
            {"position": [4, 0, 0], "family": "light", "amount": 1, "fixed": True},
            {"position": [2, 2, 0], "family": "light", "amount": 1, "fixed": True},
        ],
        "detectors": [
            {"name": "gate", "positions": [[2, 0, 0]], "reading": "sum"},
            {"name": "a", "positions": [[4, 0, 0]], "reading": "sum"},
            {"name": "b", "positions": [[2, 2, 0]], "reading": "sum"},
        ],
    }


def test_a_rebirth_is_one_record_of_all_its_rows():
    """(k)."""
    simulation, lines = observed(rebirth_world())
    assert simulation.layer is not None
    gathers = simulation.layer.gathers
    at_gate = [g for g in gathers if g["chosen"] == [["gate", 0, "0"]]]
    reborn = [g for g in gathers if g["record"] >> 32 == 2]
    assert len(at_gate) >= BIRTHS and len(reborn) >= BIRTHS
    for gather in reborn[:BIRTHS]:
        assert [cell[1] for cell in gather["cells"]] == [32, 64]  # type: ignore[index]
        assert [cell[0][0][0] for cell in gather["cells"]] == ["a", "b"]  # type: ignore[index]
        # The rebirth's u is the re-emitter's count of births (stage (vii),
        # step 2): uniform over the rebirths, half to a and half to b.
        assert gather["chosen"] == [["a" if gather["u"] < 32 else "b", 0, "0"]]  # type: ignore[operator]
    assert sorted(g["u"] for g in reborn[:BIRTHS]) == list(range(BIRTHS))
    assert Counter(str(g["chosen"][0][0]) for g in reborn[:BIRTHS]) == {"a": 32, "b": 32}  # type: ignore[index]
    splits = [line for line in lines if line.get("event") == "split" and line.get("rebirth")]
    assert len(splits) >= BIRTHS
    first = reborn[0]["record"]
    assert [line["born"] for line in splits if line["record"] == first] == [2]
    assert simulation.layer.born >= 2 * BIRTHS


def free_crowd_world() -> dict[str, object]:
    """A source of a free family into a `rerelease` on two directions."""
    return {
        "law": "beam",
        "model_id": "amplitude-free-crowd",
        "shape": [5, 3, 1],
        "boundary": {"z": "periodic"},
        "ticks": 12,
        "K": 1 << 20,
        "N": N,
        "release": [1, 1],
        "suspension": 0,
        "families": [{"name": "wind", "quantum": 0}, {"name": "light", "quantum": 1}],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "wind",
                "amount": 3,
                "fixed": True,
                "directions": [[1, 0, 0]],
            },
            {
                "position": [2, 0, 0],
                "family": "light",
                "amount": 1,
                "fixed": True,
                "table": {"wind": "rerelease"},
                "directions": [[1, 0, 0], [0, 1, 0]],
            },
        ],
    }


def test_a_free_crowd_keeps_the_unkeyed_apportioning():
    """(l)."""
    simulation, lines = observed(free_crowd_world())
    rows = sorted((r.node, r.direction, r.amount, r.phase) for r in simulation.stores[0].rows())
    released = [(line["tick"], line["amount"]) for line in lines if line.get("event") == "rerelease"]
    assert released
    assert {1, 2} <= {r[2] for r in rows}
    assert all(r.record == 0 and r.multiplicity == 1 for r in simulation.stores[0].rows())
    assert all("record" not in line for line in lines if line.get("event") == "rerelease")


def test_a_dead_window_and_a_reserved_name_are_refused():
    """(m)."""
    world = GENERATOR.mach_zehnder("dead")
    measured = world["measured"]
    assert isinstance(measured, list)
    measured[1]["table"]["light"] = {"rule": "rerelease", "phase_window": 3}
    with pytest.raises(ValueError, match=r"phase_window is dead: a split takes no gate"):
        parse_nature_beam_world(world)
    world = GENERATOR.mach_zehnder("reserved")
    detectors = world["detectors"]
    assert isinstance(detectors, list)
    detectors[0]["name"] = "measured:3"
    with pytest.raises(ValueError, match=r"name 'measured:3' is reserved"):
        parse_nature_beam_world(world)
