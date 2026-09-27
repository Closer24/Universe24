"""THE LEDGER'S ITEMS, EACH WITH ITS SMALL TEST WRITTEN BEFORE THE BUILD (the Boss's record 2199,
the model owner's word of 2026-09-26: "reach an engine that supports what we need, the fastest
way"; docs/designs/generic_engine/ENGINE_LEDGER.md sections 2 and 3). One test per item of the
shortest path, in its order; a test of a support not built yet is marked xfail strict: it turns
green the day the support lands and the mark comes off (the item moves to "implemented"). Every
test speaks the run's files alone: a world, a universe entry, a start file; no engine name.

The items, top down: (1) the output declared in one format; (2) the loader reading every
declaration as a generic term, the step's four included; (3) the source verb and the two-sided
guard (the signed read is tests/test_engine_acceptance.py test (d)); (4) the click that keeps
the momentum with its recoil's store; (5) a click's change after all advances and a run-time
overflow bound; (6) no identity string, version, flag or default in the code (the acceptance
tests (e1) to (e4)); (7) the trace; (8) the speed items."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import parse_nature_beam_world
from tests.running import run_world, stamped
from tests.worlds import emitter_world, family_entry

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

STEPS = 120
READING_KINDS = {"DETECTOR", "GAMEBOARD", "HOST"}


def families_of(document: dict) -> list[dict]:
    entries = document["universe"]
    assert isinstance(entries, list)
    return entries


def digests(document: dict, steps: int) -> tuple[list, list]:
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    lines: list[dict] = []
    simulation.record = lines.append
    for _ in range(steps):
        simulation.step()
    state = [
        (identity, live.now.copy(), live.remainder.copy())
        for identity, live in sorted(simulation.records.items(), key=lambda item: str(item[0]))
    ]
    return state, lines


def same(a: tuple[list, list], b: tuple[list, list]) -> bool:
    if a[1] != b[1] or len(a[0]) != len(b[0]):
        return False
    return all(
        x[0] == y[0] and np.array_equal(x[1], y[1]) and np.array_equal(x[2], y[2])
        for x, y in zip(a[0], b[0], strict=True)
    )


# (1) THE OUTPUT DECLARED IN ONE FORMAT (records 2191, 2199; the ledger's run declarations)


def test_1_the_output_holds_exactly_the_declared_readings_each_labelled_by_kind(tmp_path):
    """Every line the run writes is a reading the world file declared, labelled by its kind
    (DETECTOR, GAMEBOARD or HOST); one format for every experiment; the clicks of a declared
    detector are its DETECTOR reading."""
    document = emitter_world(stock=2, ticks=STEPS)
    document["readings"] = [
        {"name": "screen_clicks", "kind": "clicks", "detector": "screen"},
        {"name": "emitter_centre", "kind": "centre", "body": 0, "every": 40},
    ]
    stamped(document)
    output = run_world(document, tmp_path)
    readings = output["readings"]
    assert isinstance(readings, list) and {r["name"] for r in readings} == {
        "screen_clicks",
        "emitter_centre",
    }
    assert all(r["label"] in READING_KINDS for r in readings)
    clicks = next(r for r in readings if r["name"] == "screen_clicks")
    centre = next(r for r in readings if r["name"] == "emitter_centre")
    assert clicks["label"] == "DETECTOR" and centre["label"] == "GAMEBOARD"
    assert all({"interval", "node"} <= set(line) for line in clicks["lines"])
    assert [line["interval"] for line in centre["lines"]] == list(range(0, STEPS + 1, 40))


# (2) THE LOADER READS EVERY DECLARATION AS A GENERIC TERM (ALGEBRA.md 9.110 item 7; record 2186)


@pytest.mark.xfail(
    strict=True,
    reason="item 2 of record 2199: the loader admits `reads`, not the term form "
    "[kind, target, of, degree, weight, table]",
)
def test_2a_a_read_written_as_a_term_runs_bit_for_bit_with_the_reads_form():
    """A family's `reads` entry and the same coupling as a term of kind READ give the same
    records, remainders and lines."""
    document = emitter_world(stock=2, ticks=STEPS)
    as_terms = json.loads(json.dumps(document))
    for entry in families_of(as_terms):
        reads = entry.pop("reads", [])
        entry["terms"] = [
            [
                "read",
                "pace",
                read["family"],
                1,
                read["weight"],
                None,
                read.get("twist", "own"),
                read.get("by", 1),
            ]
            for read in reads
        ]
    stamped(as_terms)
    assert same(digests(document, STEPS), digests(as_terms, STEPS))


@pytest.mark.xfail(
    strict=True,
    reason="item 2 of record 2199: the step's four declarations (send, receive, wait, operation) "
    "are not read from universe.json",
)
def test_2b_the_step_declared_as_the_laws_own_four_runs_bit_for_bit_with_today():
    """The step declared in the files as the rule 9.57 (1) itself: every family's level and
    pair sent on all six Ports, the receive rotated by the Port's accumulator, the wait 1, the
    operation the rule's weighted sum with the remainder kept: bit for bit with the engine's
    step of today (the ledger's primitives 13 to 16; record 2186)."""
    document = emitter_world(stock=2, ticks=STEPS)
    declared = json.loads(json.dumps(document))
    declared["step"] = {
        "send": ["level", "pair", "accumulator"],
        "ports": ["+x", "-x", "+y", "-y", "+z", "-z"],
        "receive": "rotated",
        "wait": 1,
        "operation": "rule",
    }
    stamped(declared)
    assert same(digests(document, STEPS), digests(declared, STEPS))


def test_2c_a_one_sided_send_is_refused_by_the_loader():
    """The send declaration admits a symmetric set of Ports alone: an axis on or off; a
    one-sided send (five Ports) is refused by name (docs/designs/rule_alone/README.md
    section 13: a one-sided send is a gain, the rule's step amplifies without bound)."""
    document = emitter_world(stock=1, ticks=10)
    document["step"] = {
        "send": ["level", "pair", "accumulator"],
        "ports": ["-x", "+y", "-y", "+z", "-z"],
        "receive": "rotated",
        "wait": 1,
        "operation": "rule",
    }
    stamped(document)
    with pytest.raises(ValueError, match="step|ports|unknown keys"):
        parse_nature_beam_world(document)


# (3) THE SOURCE VERB AND THE TWO-SIDED GUARD (ALGEBRA.md 9.98 (11) (b), 9.108 items 11 and 12)


def test_3a_a_sourced_family_is_written_where_its_records_are_and_nowhere_else():
    """A field family sourced by the matter records: after the first intervals its level is
    nonzero (the source's act through the folder, the count D_i of the body's own record); the
    same family sourced by a family with no record stays exactly zero everywhere (the leak test)."""
    document = emitter_world(stock=2, ticks=STEPS)
    well = {
        **family_entry("well", [1000, 1019], [], clock=[512, 1]),
        "sourced": {"of": "matter", "weight": 1, "scale": 1000},
    }
    null = {**well, "name": "null", "sourced": {**well["sourced"], "of": "charge"}}
    families_of(document).extend([well, null])
    stamped(document)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    for _ in range(20):
        simulation.step()
    names = [family.name for family in simulation.families]
    well_index, null_index = names.index("well"), names.index("null")
    assert int(np.abs(simulation.sourced_records[well_index].now).sum()) > 0
    assert int(np.abs(simulation.sourced_records[null_index].now).sum()) == 0


@pytest.mark.xfail(
    strict=True,
    reason="item 3 of record 2199: the guard is the load's alone, from below; a pace above Gamma "
    "at run time is not refused",
)
def test_3b_a_content_below_zero_at_run_time_ends_the_run_with_the_guards_line():
    """The pace is bounded on both sides, 0 < p <= Gamma (ALGEBRA.md 9.108 item 12 (i)): a hill
    whose weight makes the content negative at some Node ends the run with a line naming the
    guard and the side; no level is written past it."""
    document = emitter_world(stock=2, ticks=STEPS)
    matter = next(f for f in families_of(document) if f["name"] == "matter")
    for read in matter["reads"]:
        read["weight"] = -read["weight"] if isinstance(read["weight"], int) else read["weight"]
    stamped(document)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    with pytest.raises(ValueError, match="guard.*above Gamma|pace.*above Gamma"):
        for _ in range(STEPS):
            simulation.step()


# (4) THE CLICK THAT KEEPS THE MOMENTUM, WITH ITS RECOIL'S STORE (ALGEBRA.md 9.109 item 2, 9.111 item 2)


@pytest.mark.xfail(
    strict=True,
    reason="item 4 of record 2199: the recoil is not built; a body's held momentum does not move "
    "at a click",
)
def test_4_a_giving_click_moves_the_bodys_held_momentum_by_the_algebras_integer():
    """At a giving the body's held vector n changes along the click's axis by
    sigma_a x (W x P_body) div (M x lambda_q), the remainder on the body's record; the taker
    with the opposite sign (ALGEBRA.md 9.91 (4) with the sign of 9.111 item 1)."""
    document = emitter_world(stock=2, ticks=STEPS)
    stamped(document)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    before = list(simulation.body_momentum(0))
    lines: list[dict] = []
    simulation.record = lines.append
    for _ in range(STEPS):
        simulation.step()
    givings = [line for line in lines if line.get("kind") == "giving"]
    assert givings, "the emitter gave nothing in the run"
    after = list(simulation.body_momentum(0))
    assert after != before
    assert all(isinstance(v, int) for v in after)


# (5) A CLICK'S CHANGE AFTER ALL ADVANCES; A RUN-TIME OVERFLOW BOUND (record 2185)


@pytest.mark.xfail(
    strict=True,
    reason="item 5 of record 2199: the trace that shows the interval's order is not built",
)
def test_5a_a_clicks_held_change_is_written_after_every_advance_of_its_interval(tmp_path):
    """Within one interval the trace's order is: the steps (i), the bookings and the clicks
    (ii), the held families' step (iii), the holds with the clicks' changes (iv); a click's
    change of M enters the hold after every advance (ALGEBRA.md 9.91 (8), 9.85 (2))."""
    document = emitter_world(stock=2, ticks=STEPS)
    output = run_world(
        document, tmp_path, start={"mode": "check", "trace": {"primitives": ["step", "click", "hold"]}}
    )
    trace = [
        json.loads(line) for line in (tmp_path / "out" / "world.trace.jsonl").read_text().splitlines()
    ]
    intervals = sorted({line["interval"] for line in trace if line["primitive"] == "click"})
    assert intervals, "no click in the traced run"
    order = {"step": 0, "click": 1, "hold": 2}
    for t in intervals:
        ranks = [order[line["primitive"]] for line in trace if line["interval"] == t]
        assert ranks == sorted(ranks)
    assert output["verdict"] == "LAWFUL"


def test_5b_the_loads_bound_holds_at_run_time_no_level_leaves_the_integer_range():
    """A run-time overflow bound: on a shipped world every level and remainder the run writes
    stays within 2^62 in magnitude at every interval, so no int64 wrap can pass unseen (record
    2185; the load's bound of world.py checks the start alone)."""
    document = emitter_world(stock=2, ticks=STEPS)
    stamped(document)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    bound = 1 << 62
    for _ in range(STEPS):
        simulation.step()
        for live in simulation.records.values():
            assert int(np.abs(live.now).max(initial=0)) < bound
            assert int(np.abs(live.remainder).max(initial=0)) < bound


# (7) THE TRACE (record 2187)


@pytest.mark.xfail(
    strict=True,
    reason="item 7 of record 2199: the start file's `trace` is not read; nothing is traced",
)
def test_7_a_traced_run_is_bit_for_bit_the_untraced_one_and_the_trace_only_reads(tmp_path):
    """The start file asks for a trace of the step at three Nodes; the run's output equals the
    untraced run's (the same stamp, the same clicks, the same state); the trace file holds one
    line per act with the interval, the Node, the Port, the primitive, the integers read and
    written and the remainder kept."""
    plain = run_world(emitter_world(stock=2, ticks=STEPS), tmp_path / "plain")
    traced = run_world(
        emitter_world(stock=2, ticks=STEPS),
        tmp_path / "traced",
        start={
            "mode": "check",
            "trace": {"primitives": ["step"], "nodes": [[5, 0, 0], [20, 0, 0], [70, 0, 0]]},
        },
    )
    for key in ("clicks", "verdict", "digest"):
        assert plain.get(key) == traced.get(key)
    lines = (tmp_path / "traced" / "out" / "world.trace.jsonl").read_text().splitlines()
    assert lines
    first = json.loads(lines[0])
    assert {"interval", "node", "port", "primitive", "read", "written", "remainder"} <= set(first)


# (8) THE SPEED ITEMS: THE PARALLEL AND THE ACTIVE PATHS (record 2185)


@pytest.mark.xfail(
    strict=True,
    reason="item 8 of record 2199: no parallel or active path; the start file's keys are refused",
)
@pytest.mark.parametrize("start", [{"mode": "check", "parallel": 2}, {"mode": "check", "active": True}])
def test_8_the_parallel_and_the_active_paths_are_bit_for_bit_the_plain_one(tmp_path, start):
    """Records advanced in parallel and merged in identity order, or the active box from the
    real support, give the same output as the plain path on a shipped world."""
    plain = run_world(emitter_world(stock=2, ticks=STEPS), tmp_path / "plain")
    other = run_world(emitter_world(stock=2, ticks=STEPS), tmp_path / "other", start=start)
    for key in ("clicks", "verdict", "digest"):
        assert plain.get(key) == other.get(key)
