"""The host's batches and memos of 2026-09-21 (the model owner's order,
"optimization and simplify"; docs/MIGRATION.md, "The host's batches and
memos"): the same integers, computed once. The expected results of
docs/TEST_EXPECTATIONS.md ("The host's batches and memos"), written down
first: (a) `NatureBeamStore.extend` over batches leaves every field equal
to one `append` per batch in the same order, the defaults of the
amplitude columns and the hand filled per batch, an empty batch adding
nothing; (b) `Measured.charges` returns the pairs a fresh computation
returns, on the shipped J3 world after 3 intervals for every body, and
follows a change of what is held and of the units clicked; (c) the
world's `handed` reads the same value twice and is kept on the world
after the first read.
"""

from __future__ import annotations

import copy
from pathlib import Path

import numpy as np

from event_universe.events import NatureBeamSimulation
from event_universe.events.nature_beam import FIELDS, NatureBeamStore
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
J3 = ROOT / "examples" / "events" / "weak" / "j3_deuteron.json"


def batch(seed: int, count: int, full: bool) -> dict[str, np.ndarray]:
    rng = np.random.RandomState(seed)
    names = (
        FIELDS
        if full
        else ("node", "direction", "age", "phase", "number", "amount", "content", "arrival")
    )
    return {name: rng.randint(0, 1000, size=count).astype(np.int64) for name in names}


def test_extend_appends_the_batches_as_one_append_each_in_order():
    """(a)."""
    batches = [batch(1, 5, True), batch(2, 0, True), batch(3, 3, False), batch(4, 7, True)]
    one_by_one = NatureBeamStore((3, 3, 2))
    for columns in batches:
        one_by_one.append(**{name: values.copy() for name, values in columns.items()})
    at_once = NatureBeamStore((3, 3, 2))
    at_once.extend([{name: values.copy() for name, values in columns.items()} for columns in batches])
    assert at_once.size == one_by_one.size == 15
    for name in FIELDS:
        assert np.array_equal(getattr(at_once, name), getattr(one_by_one, name)), name
    empty = NatureBeamStore((3, 3, 2))
    empty.extend([])
    assert empty.size == 0


def fresh_charges(entry: object, for_push: bool) -> list[tuple[int, int]]:
    """The charges computed again from the same inputs, the memo cleared."""
    twin = copy.copy(entry)
    twin._charges_cache = None  # type: ignore[attr-defined]
    return twin.charges(for_push)  # type: ignore[attr-defined, no-any-return]


def test_the_charges_memo_returns_the_fresh_pairs_and_follows_every_change():
    """(b)."""
    loaded = load_world(J3.read_bytes(), base_dir=J3.parent)
    simulation = NatureBeamSimulation(loaded.world)
    for _ in range(3):
        simulation.step()
    entries = list(simulation.measured.values())
    assert entries
    checked = 0
    for entry in entries:
        for for_push in (False, True):
            assert entry.charges(for_push) == fresh_charges(entry, for_push)
            assert entry.charges(for_push) == fresh_charges(entry, for_push)
        checked += 1
    assert checked == len(entries)
    entry = next(e for e in entries if any(e.held))
    before = entry.charges()
    family = next(f for f, held in enumerate(entry.held) if held)
    entry.held[family] += 1
    assert entry.charges() == fresh_charges(entry, False)
    assert entry.charges(True) == fresh_charges(entry, True)
    assert entry.charges() != before
    entry.held[family] -= 1
    assert entry.charges() == before
    charged = [f for f, (numerator, _) in enumerate(entry.unit_charges) if numerator]
    if charged:
        entry.clicks[charged[0]] += 1
        assert entry.charges() == fresh_charges(entry, False)
        assert entry.charges() != before
        entry.clicks[charged[0]] -= 1
        assert entry.charges() == before


def test_the_world_reads_handed_once():
    """(c)."""
    loaded = load_world(J3.read_bytes(), base_dir=J3.parent)
    world = loaded.world
    assert "handed" not in vars(world)
    first = world.handed
    assert "handed" in vars(world)
    assert world.handed is first
