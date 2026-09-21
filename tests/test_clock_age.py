"""clock-age-v1, the clock's word (the model owner's decision of 2026-09-21,
record 394; docs/designs/clock_age/NOTE.md sections 2 and 7; BEAM_LAW
section 3 step 5 and note 25): every clock counts the age moment
`sum amount x age` over the rays of another number at its Node by default;
the word `presence` on a table entry selects the presence for the clock as
the law counted it before the word; `age` still selects the age moment. The
expected integers of docs/TEST_EXPECTATIONS.md ("The clock's word,
clock-age-v1"), written down first, on the bar of `tests/test_nature_beam_age.py`
(c) (a source of `m` at x = 0 of an open 5 x 1 x 1 bar at `release` [1, 1],
a fixed reader of `light` at x = 3, `suspension` [1, 4], 24 intervals):

(a) the default: a reader whose entry omits `reads` (`{"m": "read"}`) counts
    the age moment, 5 at the first arrival then 11 (the ages 5 and 6 of the
    two rays at its Node), owes as the `age` reader does and ages 1, 2, 3,
    4, 5, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11;
    its `read` records still carry the flow [Q, 0, 0] (the record's
    component is untouched by the word); an entry that reads `age`, `scalar`,
    `outside`, `here`, `vector` or `tensor` counts the same;
(b) the presence word: a reader whose entry reads `presence` counts the
    presence 2 (1 at the first arrival) and ages 1, 2, 3, 4, 5, 6, 7, 8, 8,
    9, 10, 10, 11, 12, 12, 13, 14, 14, 15, 16, 16, 17, 18, 18, the ages of
    every reader before the word; its record carries the presence (1 per
    arriving row); `count_component` maps `presence` to `scalar` and every
    other word to `age`;
(c) the edges: a reader with no crowd (the source removed) owes nothing
    under either word and ages 1 .. 24; a `reads` word the law does not
    know is refused naming the words, `presence` among them; `presence` is
    accepted on `pass` (a window is not); a world whose clocked entries
    declare `presence` parses and runs as the same world did before the
    word (series T's `presence_3`, its expectations' pin 1 + z = 1.300).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.measured import count_component
from event_universe.events.world import READS, Q
from event_universe.world_loading import load_world

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_nature_beam_age import ages_of_the_reader, bar, clock_world  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
AGE_AGES = [1, 2, 3, 4, 5, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11]
PRESENCE_AGES = [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10, 10, 11, 12, 12, 13, 14, 14, 15, 16, 16, 17, 18, 18]


def test_the_default_word_is_the_age_moment():
    """(a)."""
    ages, readings, read = ages_of_the_reader(clock_world({"m": "read"}))
    assert ages == AGE_AGES
    assert readings[5] == (6, 1, 5) and all(r[1:] == (2, 11) for r in readings if r[0] >= 7)
    assert read == [[Q, 0, 0]] * len(read)
    for word in ("age", "scalar", "outside", "here", "vector", "tensor"):
        ages, readings, _ = ages_of_the_reader(clock_world({"m": {"rule": "read", "reads": word}}))
        assert ages == AGE_AGES, word
        assert all(r[2] == 11 for r in readings if r[0] >= 7), word
    assert count_component("age") == "age"
    assert [count_component(word) for word in READS if word != "presence"] == ["age"] * 6


def test_the_presence_word_counts_the_presence_as_before():
    """(b)."""
    ages, readings, read = ages_of_the_reader(clock_world({"m": {"rule": "read", "reads": "presence"}}))
    assert ages == PRESENCE_AGES
    assert all(presence == counted for _, presence, counted in readings)
    assert read == [1] * len(read)
    assert count_component("presence") == "scalar"


def test_the_edges_of_the_word():
    """(c)."""
    reader = {"position": [3, 0, 0], "family": "light", "amount": 1, "fixed": True}
    for table in ({"m": "read"}, {"m": {"rule": "read", "reads": "presence"}}):
        world = bar(
            [5, 1, 1], measured=[{**reader, "table": table}], release=[1, 1], suspension=[1, 4], ticks=24
        )
        simulation = NatureBeamSimulation(parse_nature_beam_world(world))
        for tick in range(1, 25):
            simulation.step()
        body = simulation.measured[1]
        assert (body.age, body.waited, body.owed) == (24, 0, 0), table
    with pytest.raises(ValueError, match="reads must be one of"):
        parse_nature_beam_world(clock_world({"m": {"rule": "read", "reads": "crowd"}}))
    parsed = parse_nature_beam_world(clock_world({"m": {"rule": "pass", "reads": "presence"}}))
    assert parsed.measured[1].reads[0] == "presence" and parsed.measured[1].table[0] == "pass"
    with pytest.raises(ValueError, match="phase_window is refused on pass"):
        parse_nature_beam_world(
            clock_world({"m": {"rule": "pass", "reads": "presence", "phase_window": 8}})
        )
    folder = ROOT / "examples" / "events" / "clock_word"
    path = folder / "presence_3.json"
    loaded = load_world(path.read_bytes(), base_dir=folder, root=folder.parent).world
    lamp = loaded.measured[1]
    assert (
        lamp.reads[loaded.families.index(next(f for f in loaded.families if f.name == "mass"))]
        == "presence"
    )
    expected = json.loads((folder / "expectations.json").read_text(encoding="utf-8"))
    assert round(expected["worlds"]["presence_3"]["one_plus_z"], 3) == 1.3
