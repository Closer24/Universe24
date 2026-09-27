"""The source's folder (ALGEBRA.md #the-primitives row "the source"; ALGEBRA.md #the-paces): the line's integers on the run files' numbers, the carried remainder's exact floor, the table form, the write's locality, the inverse bit for bit, the refusals by name, the hand identity, the run file's record against the README's counts, the declaration the ledger's row."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.register import discover, folder_of
from event_universe.features.source import (
    DECLARATION,
    THE_WORD,
    SourceOwn,
    SourceStart,
    SourceTerm,
    apply,
    hand_identity,
    invert,
)
from event_universe.world_files import parse_nature_beam_world
from tests.worlds import emitter_world

ROOT = Path(__file__).resolve().parents[1]
SHAPE = (2, 3, 1)
SCALE = 18_910  # E_s of the run files (D_peak 1,891,072 div 100)
PEAK = 1_891_072
PLAIN = SourceTerm(target=3, of=2, weight=1, scale=SCALE)
TABLE = SourceTerm(target=4, of=2, weight=1, scale=SCALE, cap=60)


def argument(*values: int) -> np.ndarray:
    return np.array(values, dtype=np.int64).reshape(SHAPE)


def zeros() -> SourceOwn:
    return SourceOwn(np.zeros(SHAPE, dtype=np.int64))


def test_the_line_on_the_run_files_numbers():
    """s_i = D_i div E_s at the peak: 1,891,072 div 18,910 = 100 with the remainder 72; a Node
    with D_i below E_s adds nothing and keeps D_i as its remainder; a Node with D_i = 0 adds
    nothing and is outside the write."""
    start = SourceStart(SHAPE, argument(PEAK, 18_909, 0, 37_820, 1, 18_910))
    writes = apply(PLAIN, start, zeros())
    assert writes.counts.ravel().tolist() == [100, 0, 0, 2, 0, 1]
    assert writes.remainders.ravel().tolist() == [72, 18_909, 0, 0, 1, 0]
    assert writes.at.ravel().tolist() == [True, False, False, True, False, True]
    assert writes.integers.ravel().tolist() == [100, 0, 0, 2, 0, 1]
    weighted = apply(SourceTerm(3, 2, -3, SCALE), start, zeros())
    assert weighted.integers.ravel().tolist() == [-300, 0, 0, -6, 0, -3]
    assert weighted.counts.ravel().tolist() == writes.counts.ravel().tolist()


def test_the_remainder_is_carried_so_the_sum_of_the_counts_is_the_exact_floor():
    """Over k intervals with the same D_i the counts sum to floor(k D_i / E_s), never less: at
    the peak 100 per interval plus one more every 263 intervals (72 x 263 = 18,936 > 18,910);
    on a Node with D_i = 7 the first count comes at the 2702nd interval."""
    start = SourceStart(SHAPE, argument(PEAK, 7, 0, 0, 0, 0))
    own = zeros()
    total = np.zeros(SHAPE, dtype=np.int64)
    for k in range(1, 3001):
        writes = apply(PLAIN, start, own)
        total += writes.counts
        own = SourceOwn(writes.remainders)
        for node, d in ((0, PEAK), (1, 7)):
            expected = Fraction(k * d, SCALE)
            assert int(total.ravel()[node]) == expected.numerator // expected.denominator
        assert 0 <= int(own.remainders.min()) and int(own.remainders.max()) < SCALE
    assert int(total.ravel()[0]) == 300_000 + 11 and int(total.ravel()[1]) == 1


def test_the_table_form_saturates_and_keeps_no_remainder():
    """s_i = s_cap D_i div (s_cap E_s + D_i): 60 x 1,891,072 div (60 x 18,910 + 1,891,072) = 37
    (the README's number); the count never reaches the cap; twice the argument gives 46, not
    74; the remainder stays zero whatever the start's remainder says."""
    start = SourceStart(SHAPE, argument(PEAK, 2 * PEAK, 18_910, 0, 10**12, 1))
    own = SourceOwn(argument(5, 5, 5, 5, 5, 5))
    writes = apply(TABLE, start, own)
    assert writes.counts.ravel().tolist() == [37, 46, 0, 0, 59, 0]
    assert writes.remainders.ravel().tolist() == [0] * 6
    assert int(writes.counts.max()) < TABLE.cap


def test_the_inverse_returns_the_start_bit_for_bit():
    """The same integers subtracted and the remainder before restored, for both forms and for
    a carried remainder."""
    start = SourceStart(SHAPE, argument(PEAK, 7, 0, 37_820, 18_909, 1))
    for term in (PLAIN, TABLE, SourceTerm(3, 2, -2, 977)):
        own = SourceOwn(
            argument(72, 3, 0, 500, 0, 976) if term.cap is None else argument(0, 0, 0, 0, 0, 0)
        )
        level = argument(10, -20, 30, 0, 5, 6)
        writes = apply(term, start, own)
        after = level.copy()
        after[writes.at] += writes.integers[writes.at]
        undo, before = invert(term, start, SourceOwn(writes.remainders), writes)
        restored = after.copy()
        restored[writes.at] += undo[writes.at]
        assert np.array_equal(restored, level) and np.array_equal(before.remainders, own.remainders)


def test_the_refusals_by_name():
    start = SourceStart(SHAPE, argument(1, 2, 3, 4, 5, 6))
    with pytest.raises(ValueError, match="scale E_s is 0"):
        apply(SourceTerm(3, 2, 1, 0), start, zeros())
    with pytest.raises(ValueError, match="weight is 0"):
        apply(SourceTerm(3, 2, 0, SCALE), start, zeros())
    with pytest.raises(ValueError, match="cap s_cap is 0"):
        apply(SourceTerm(3, 2, 1, SCALE, cap=0), start, zeros())
    # a negative D_i is admitted (no refusal beyond the ledger's row): the plain form floors it
    negative = apply(PLAIN, SourceStart(SHAPE, argument(1, -1, 0, 0, 0, 0)), zeros())
    assert int(negative.counts.ravel()[1]) == -1 and int(negative.remainders.ravel()[1]) == SCALE - 1
    with pytest.raises(ValueError, match="weight x count"):
        apply(
            SourceTerm(3, 2, 1 << 40, 1),
            SourceStart(SHAPE, argument(1 << 30, 0, 0, 0, 0, 0)),
            zeros(),
        )
    with pytest.raises(ValueError, match="shaped by the GameBoard"):
        apply(PLAIN, SourceStart((3, 2, 1), argument(1, 2, 3, 4, 5, 6)), zeros())
    with pytest.raises(ValueError, match="int64"):
        apply(PLAIN, SourceStart(SHAPE, np.zeros(SHAPE, dtype=np.int32)), zeros())
    with pytest.raises(ValueError, match="leave the bound"):
        apply(
            SourceTerm(3, 2, 1, SCALE, cap=1 << 40),
            SourceStart(SHAPE, argument(1 << 30, 0, 0, 0, 0, 0)),
            zeros(),
        )


def test_the_trace_hand_identity_at_a_node():
    assert hand_identity(PLAIN, PEAK, 0, 596, 696)
    assert hand_identity(PLAIN, PEAK, 18_900, 596, 697)  # the carried remainder tips one more
    assert not hand_identity(PLAIN, PEAK, 0, 596, 697)
    assert hand_identity(TABLE, PEAK, 0, 300, 337)
    assert hand_identity(SourceTerm(3, 2, -3, SCALE), PEAK, 72, 0, -300)


def test_the_declaration_is_the_ledgers_row_and_the_register_binds_its_function():
    assert DECLARATION.name == "the source" and folder_of(DECLARATION.name) == "source"
    assert DECLARATION.place == "(iv)" and DECLARATION.word == "the right side"
    assert DECLARATION.writes == ("a family's level at a Node", "the record's remainder")
    assert (
        "D_i" in DECLARATION.reads[0] and "E_s" in DECLARATION.reads and "s_cap" in DECLARATION.reads[2]
    )
    assert THE_WORD in DECLARATION.section and "#the-primitives" in DECLARATION.section
    register = discover()
    declaration = register.declarations["the source"]
    assert declaration.section == DECLARATION.section and declaration.function is apply
    step = parse_nature_beam_world(emitter_world(stock=1, ticks=2)).step
    assert register.writers("a family's level at a Node", "(iv)", step) == ("the hold", "the source")
