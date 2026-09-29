"""THE CLICK IS THE COUNT'S LINE FOR EVERY RECORD (the model owner's word of 2026-09-29 on #1495, finding 10; ALGEBRA.md #the-counts-line, the free record): a bound body gives at its click, the given record laid with one quantum from its form; the count's line moves the record's quanta, conserved to the bit; a detector's Node reports each quantum standing on it to its body, the books with it, and the record ends where its last quantum left it; the inverse returns the counts of an interval with no report."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

import event_universe.world_files as world_files
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world
from tests.laws import chain_body_world, load_file

TOOL = load_file("pixel_mode", Path(__file__).resolve().parents[1] / "tools" / "pixel_mode.py")
# the giver: body 0 on the chain's middle Node, its charge's stock and its moment (the charge is a vector family)
GIVER = {
    "q": 1,
    "moment": [0, 0, 1],
    "stocks": {"charge": 64},
    "emitter": {"family": "charge", "weight": 1},
}
TAKER_AT, TAKER, INTERVALS = 200, 1, 400  # the taker body 1 at x = 200 with its set "taker"


@pytest.fixture(scope="module")
def world(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, Path]:
    """The chain of two bodies laid once by the pixel tool: the giver at x = 120 and the taker at x = 200."""
    folder = tmp_path_factory.mktemp("click")
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(world_files, "REPOSITORY_ROOT", folder)
        return folder, chain_body_world(folder, TOOL, giver=GIVER, taker_at=TAKER_AT)


def loaded(world: tuple[Path, Path], lines: list[dict[str, object]]) -> DetectorLawSimulation:
    folder, path = world
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(world_files, "REPOSITORY_ROOT", folder)
        return DetectorLawSimulation(load_world(path), observer=lines.append)


def totals(simulation: DetectorLawSimulation) -> dict[int, int]:
    """SUM (W_c c + r) over the board of every free record, by its identity."""
    found = {}
    for live in simulation.records.values():
        if live.counts is not None and live.count_remainder is not None:
            wall = simulation.pair_count_wall(simulation.record_pair(live), "the test")
            found[live.identity] = int((wall * live.counts + live.count_remainder).sum(dtype=object))
    return found


@pytest.fixture(scope="module")
def run(world: tuple[Path, Path]) -> dict[str, object]:
    """The run of INTERVALS intervals with its readings per interval: the givings with the born record's count and the giver's stock around them, every free record's conserved total and least count, the reports with the taker's content around them and whether the record left."""
    lines: list[dict[str, object]] = []
    simulation = loaded(world, lines)
    charge = [family.name for family in simulation.families].index("charge")
    born, conserved, least, reports, reported = [], {}, [], [], set()
    for _ in range(INTERVALS):
        stock, taken = simulation.held[0][charge], simulation.held[TAKER][charge]
        simulation.step()
        now = [line for line in lines if line["tick"] == simulation.tick]
        givings = [line for line in now if line["event"] == "giving"]
        gathers = [line for line in now if line["event"] == "gather"]
        for giving in givings:
            live = simulation.records[int(giving["record"])]
            assert live.counts is not None
            born.append((int(live.counts.sum()), stock - simulation.held[0][charge], len(givings)))
        reported |= {int(line["record"]) for line in gathers}
        for identity, total in totals(simulation).items():
            if identity not in reported:
                conserved.setdefault(identity, set()).add(total)
        least.extend(
            int(live.counts.min()) for live in simulation.records.values() if live.counts is not None
        )
        if gathers:
            mask = simulation.blocks[TAKER].mask
            reports.append(
                {
                    "gathers": gathers,
                    "raised": simulation.held[TAKER][charge] - taken,
                    "on_the_set": all(mask[tuple(line["node"])] for line in gathers),
                    "left": [int(line["record"]) not in simulation.records for line in gathers],
                }
            )
    books = simulation.books()
    return {"born": born, "conserved": conserved, "least": least, "reports": reports, "books": books}


def test_every_giving_lays_one_quantum_and_lowers_the_givers_stock_by_one(run):
    """(a) At the body's click the given record carries exactly one quantum laid from its form, and the giver's charge stock falls by one per giving."""
    born = run["born"]
    assert born and all(count == 1 for count, _, _ in born)
    assert all(lowered == givings for _, lowered, givings in born)


def test_the_count_of_a_free_record_is_conserved_to_the_bit_and_never_below_minus_one(run):
    """(b) SUM (W_c c + r) over the board of every free record is one integer from its birth until its report (the line is the exact continuity of the currents), and its count never falls below -1."""
    assert run["conserved"] and all(len(values) == 1 for values in run["conserved"].values())
    assert min(run["least"]) >= -1


def test_a_quantum_is_reported_at_the_taker_and_the_record_ends(run):
    """(c) A quantum arriving whole at the taker's Nodes is reported there: each report raises the taker's charge by one and writes one `gather` line naming the taker at a Node of its set, and the record whose last quantum left it leaves the GameBoard."""
    reports = run["reports"]
    assert reports
    for report in reports:
        gathers = report["gathers"]
        assert all(line["chosen"] == "taker" and line["taker"] == TAKER for line in gathers)
        assert all(line["content"] == 1 and line["giver"] == 0 for line in gathers)
        assert report["raised"] == len(gathers) and report["on_the_set"] and all(report["left"])


def test_the_books_balance(run):
    """(d) Held: initial + measured == current + spent + escaped; transit: released == current + absorbed + escaped, for every family."""
    books = run["books"]
    assert books["balanced"]
    for lines in books["families"].values():
        assert lines["measured"]["balanced"] and lines["transit"]["balanced"]


def test_the_inverse_returns_the_free_records_counts_of_an_interval_with_no_report(world):
    """(e) After a forward interval with no giving and no report, `step_inverse` returns every free record's count and remainder bit for bit (the count's line with the current reversed)."""
    lines: list[dict[str, object]] = []
    simulation = loaded(world, lines)
    for _ in range(INTERVALS):
        kept = {
            identity: (live.counts.copy(), live.count_remainder.copy())
            for identity, live in simulation.records.items()
            if live.counts is not None and live.count_remainder is not None
        }
        simulation.step()
        clicks = [line for line in lines if line["tick"] == simulation.tick and line["event"] != "block"]
        if not kept or any(line["event"] in ("giving", "gather") for line in clicks):
            continue
        simulation.step_inverse()
        for identity, (counts, remainder) in kept.items():
            live = simulation.records[identity]
            assert np.array_equal(live.counts, counts) and np.array_equal(
                live.count_remainder, remainder
            )
        return
    pytest.fail("no interval with a free record and no giving and no report")
