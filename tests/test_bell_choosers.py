"""The reader of the Bell run with the choosers on the GameBoard reads the
engine (`tools/click_readings/bell_choosers.py`; the experimenter's rule, 2026-09-20): on
a minimal case run through the runner, every reading of the tool equals the
engine's own function, and nothing of the registered worlds' numbers is
pinned. The case: the design of `examples/events/bell/make_chooser_worlds.py`
(`base`) with the two setting streams released at fixed phases (the lamps'
contents 3 and 5 at `release` [1, 1]: the turn 0 at K, so every `sa` row
carries the phase 20 and every `sb` row the phase 44; the offsets 0 and,
on the minus counters, 32), 64 pairs analysed after the design's warm-up
of 7. Expected, written down first:

(a) the tick offsets the tool reports (the smallest tick - age at each
    counter, the age a pair's birth ordinal less one off the record on
    the line; since the fraction-free law of 2026-09-20 the pair is read
    by its record, the lamp's exact clock stalling once at tick 4 on this
    lamp) equal 1 + the flight age at which the pair ray reaches each
    counter, `Flight.manhattan_steps` (the +X heading: 3 Links by
    the age 5, 6 by 10, 7 by 12, 8 by 13): 6, 11, 13, 14;
(b) one bin, (20, 44): n = 64 (the ages 6..69 by record: the six records
    born before tick 8 meet no setting, the design's warm-up of 7 by
    tick; every phase of the circle once), E = 1 - 4 x 24 / 64 = -1/2
    with the counts 8, 24, 24, 8 (the same, the different), both
    marginals 1/2, the triangle's own value the same, the warm-up 6,
    every criterion passed (the complement, the windows, one outcome per
    side per age, the escapes of the warm-up);
(c) the same design with the windows written in the file (20 and 44, the
    complements 52 and 12) gives the same bin, counts and E; the two runs
    merged (`merged`) give one bin of 128;
(d) `best_quadruple` on synthetic bins whose E are the triangle's for
    Alice's 0 and 25 with Bob's 8 and 29 reads 2 on that quadruple and
    the triangle 2; `chsh_sum` reads the same 2 and None where a bin is
    missing; `signed_sums` places the minus sign on each term in turn.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

from event_universe.events import parse_nature_beam_world
from event_universe.events.nature_beam import nature_beam_tables
from event_universe.events.run import execute_nature_beam_run

ROOT = Path(__file__).resolve().parents[1]
ALICE, BOB = 20, 44
PAIRS = 64


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def make_worlds():
    return load_script(
        "bell_make_chooser_worlds", ROOT / "examples" / "events" / "bell" / "make_chooser_worlds.py"
    )


def tool():
    return load_script("bell_choosers", ROOT / "tools" / "click_readings" / "bell_choosers.py")


def fixed_world(written: bool) -> dict[str, object]:
    """The design with fixed-phase streams: read windows, or the same
    windows written in the file."""
    m = make_worlds()
    ticks = m.FIRST + PAIRS - 1 + max(m.OFFSETS.values())
    if written:
        windows = {
            m.ALICE_PLUS: ALICE,
            m.ALICE_MINUS: (ALICE + 32) % 64,
            m.BOB_PLUS: BOB,
            m.BOB_MINUS: (BOB + 32) % 64,
        }
    else:
        windows = {
            m.ALICE_PLUS: m.reads("sa", 0),
            m.ALICE_MINUS: m.reads("sa", 32),
            m.BOB_PLUS: m.reads("sb", 0),
            m.BOB_MINUS: m.reads("sb", 32),
        }
    return m.base("test-fixed", ticks, windows, [1, 1], (m.ROWS_A, m.ROWS_B), (ALICE, BOB))


def run(document: dict[str, object], folder: Path) -> Path:
    folder.mkdir()
    source = json.dumps(document).encode("utf-8")
    execute_nature_beam_run(
        parse_nature_beam_world(document), source, folder, "test", int(document["ticks"])
    )
    return folder


def test_the_tool_reads_the_fixed_setting_streams_off_the_engine(tmp_path):
    """(a), (b), (c)."""
    m = make_worlds()
    reader = tool()
    document = fixed_world(written=False)
    checks = reader.Checks()
    read = reader.analyse(run(document, tmp_path / "read"), checks)
    # (a) The offsets: 1 + the flight age at each counter's distance from
    # the pair lamp, off the flight table of the world's +X heading.
    parsed = parse_nature_beam_world(document)
    flight = nature_beam_tables(parsed).flight
    heading = parsed.directions.index((1, 0, 0))
    ages = np.arange(0, 20, dtype=np.int64)
    links = flight.manhattan_steps(np.full(ages.shape, heading, dtype=np.int64), ages)
    expected_offsets = {}
    for name, counter in reader.counters_of(document).items():
        distance = abs(counter.node[0] - m.LAMP_X)
        expected_offsets[name] = 1 + int(ages[links >= distance][0])
    assert (
        read.offsets
        == expected_offsets
        == {
            "alice_plus": 6,
            "alice_minus": 11,
            "bob_plus": 13,
            "bob_minus": 14,
        }
    )
    # (b) One bin at the fixed settings. Under the one click (stage (vii)
    # step 4) the pair lamp's rows are records with the path phase 0, the
    # counters' windows read the path phase, and every pair lands in
    # (-1, -1): the crowd form's triangle (8, 24, 24, 8 and E = -1/2, the
    # tool's expectation) is the old law's (re-run under the one click (stage (vii) step 4); the verdict to be re-read).
    # The warm-up by record: the pairs of the ages 0 .. 5 (six records)
    # meet no setting at Alice's plus counter; the design's FIRST = 7 is
    # the first age BY TICK, and the lamp's exact clock (the fraction-free
    # law, 2026-09-20) stalls once at tick 4, so the 7th record, born at
    # tick 8, is the first with a setting: its age 6.
    assert read.first == m.FIRST - 1 == 6 and read.warm_up == 6 and read.pairs == PAIRS
    assert set(read.bins) == {(ALICE, BOB)}
    item = read.bins[(ALICE, BOB)]
    assert item.counts == {(1, 1): 0, (1, -1): 0, (-1, 1): 0, (-1, -1): 64}
    assert item.correlation == 1 and reader.expected_correlation(ALICE, BOB, 64) == Fraction(-1, 2)
    assert item.marginal(0) == item.marginal(1) == 0
    assert checks.failed == 3 and [row[0] for row in checks.rows if not row[1]] == [
        "read: record kinds",
        "read: every click inside its window, every pass outside",
        "read: E(20, 44) on the triangle",
    ]
    # (c) The windows written in the file read the same, and merge.
    checks = reader.Checks()
    written = reader.analyse(run(fixed_world(written=True), tmp_path / "written"), checks, PAIRS)
    assert checks.failed == 3, [row for row in checks.rows if not row[1]]
    assert written.bins[(ALICE, BOB)].counts == item.counts and written.first == 0
    both = reader.merged([read, written])
    assert set(both) == {(ALICE, BOB)} and both[(ALICE, BOB)].n == 2 * PAIRS
    assert both[(ALICE, BOB)].correlation == 1
    # The command line on the two runs: no quadruple with one setting per
    # side, no criterion failed.
    # The tool exits 1: its checks of the crowd form fail under the one click.
    assert reader.main([str(tmp_path / "read"), str(tmp_path / "written"), "--pairs", "64"]) == 1


def test_the_chsh_sums_over_synthetic_bins():
    """(d)."""
    reader = tool()
    bins = {}
    for a in (0, 25):
        for b in (8, 29):
            item = reader.Bin()
            e = reader.expected_correlation(a, b, 64)
            same = int(64 * (1 + e) / 2)
            item.counts = {(1, 1): same, (1, -1): 64 - same, (-1, 1): 0, (-1, -1): 0}
            bins[(a, b)] = item
    assert reader.chsh_sum(bins, ((0, 25), (8, 29))) == 2
    assert reader.chsh_sum(bins, ((0, 25), (8, 30))) is None
    largest, quadruple, triangle = reader.best_quadruple(bins, 64)
    assert (largest, quadruple, triangle) == (2, ((0, 25), (8, 29)), 2)
    e = [Fraction(1), Fraction(1, 2), Fraction(-1, 4), Fraction(0)]
    assert reader.signed_sums(e) == [Fraction(-3, 4), Fraction(1, 4), Fraction(7, 4), Fraction(5, 4)]
    assert (
        reader.in_window(15, 0, 64) and not reader.in_window(16, 0, 64) and reader.in_window(48, 0, 64)
    )
