"""The amplitude law's key and the record on the row (`amplitude-v1`, the
model owner, 2026-09-20, Highlights 5.4, "DECIDED: `amplitude-v1` is
built"; the design, scratchpad/amplitude/DESIGN.md sections 1 and 2.3;
docs/BEAM_LAW.md note 37): the world key `amplitude`, the three columns
`record`, `branch` and `multiplicity` of the store, and the merge's normal
form (the cancel of antiphase rows of one record). The expected integers of
docs/TEST_EXPECTATIONS.md ("The amplitude law: the record"), written down
before the first run:

(a) the key: absent it is false, `hypotheses` is empty and `run.json`
    carries `amplitude` false; declared true it is true and `hypotheses` is
    ["amplitude-v1"]; refused naming the key: a value that is not true or
    false, N below 4 under the key (the quarter turn of a reflection), a
    lamp's `rate` other than [1, 1] under the key (one record per
    self-creation); a world with N 4 and a lamp at [1, 1] is accepted;
(b) the columns: every row of a world without the key carries record 0,
    branch 0 and multiplicity 1 (the store's columns after 5 intervals of a
    lamp of the design's Mach-Zehnder kind), `state.json`'s rows carry no
    `record`, `branch` or `multiplicity` key, and under the key they carry
    the three; the packed merge key of a store whose three columns are at
    their defaults equals the key packed from the six fields of the law as
    it was (the three add 0 bits), so the order of the merge is unchanged;
(c) the normal form (the store's `merge` with the circle's N = 64): rows of
    one record and multiplicity equal in every field but a phase
    difference of exactly 32 cancel: amounts 3 at 5 and 2 at 37 leave one
    row of amount 1 at phase 5 (4 units cancelled); 1 at 9 and 1 at 41
    leave nothing (2 cancelled); 1 at 40 and 2 at 8 leave 1 at 8 (the
    larger side's phase; 2 cancelled); rows of no record at 9 and 41 stay
    two rows; two rows of one record at phases 5 and 21 (a quarter turn)
    stay two rows; two rows of one record at one phase merge to one row
    of amount 2 (the merge as it was); rows of one record at the same
    phase with multiplicities 2 and 4 stay two rows; without the key
    (modulus 0) nothing cancels and the antiphase pair stays two rows; the
    merge returns the units cancelled per (record, direction), {(7, 2):
    (4, 4), (8, 2): (2, 2), (9, 2): (2, 2)} with the content carried.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import NatureBeamStore
from event_universe.events.run import execute_nature_beam_run
from event_universe.events.world import AMPLITUDE_RULE

N = 64


def lamp_world(**overrides: object) -> dict[str, object]:
    """A 5 x 5 plane with one lamp of `light` releasing one row per
    self-creation on +x and +y at the turn 1 (K 1), and a detector."""
    world: dict[str, object] = {
        "law": "beam",
        "model_id": "amplitude-record-test",
        "shape": [5, 5, 1],
        "boundary": {"z": "periodic"},
        "ticks": 5,
        "K": 1,
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "light", "quantum": 1}],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "light",
                "amount": 8,
                "fixed": True,
                "lamp": {"rate": [1, 1], "directions": [[1, 0, 0], [0, 1, 0]]},
            },
            {"position": [4, 0, 0], "family": "light", "amount": 1, "fixed": True},
        ],
        "detectors": [{"name": "d1", "positions": [[4, 0, 0]]}],
    }
    world.update(overrides)
    return world


def test_the_key_its_default_its_identity_and_its_refusals(tmp_path: Path):
    """(a)."""
    plain = parse_nature_beam_world(lamp_world())
    assert plain.amplitude is False and plain.hypotheses == []
    keyed = parse_nature_beam_world(lamp_world(amplitude=True))
    assert keyed.amplitude is True and keyed.hypotheses == [AMPLITUDE_RULE]
    for world, expected in ((plain, False), (keyed, True)):
        out = tmp_path / ("keyed" if expected else "plain")
        out.mkdir()
        execute_nature_beam_run(world, b"{}", out, "test", 2)
        record = json.loads((out / "run.json").read_text())
        assert record["amplitude"] is expected
        assert record["hypotheses"] == ([AMPLITUDE_RULE] if expected else [])
    with pytest.raises(ValueError, match="amplitude must be true or false"):
        parse_nature_beam_world(lamp_world(amplitude=1))
    with pytest.raises(ValueError, match="amplitude is refused with N 2"):
        parse_nature_beam_world(lamp_world(amplitude=True, N=2))
    rate_world = lamp_world(amplitude=True)
    measured = rate_world["measured"]
    assert isinstance(measured, list)
    measured[0] = {**measured[0], "lamp": {"rate": [2, 1], "directions": [[1, 0, 0]]}}
    with pytest.raises(ValueError, match=r"rate \[2, 1\] is refused under amplitude"):
        parse_nature_beam_world(rate_world)
    small = lamp_world(amplitude=True, N=4)
    measured = small["measured"]
    assert isinstance(measured, list)
    measured[0] = {**measured[0], "amount": 1}
    assert parse_nature_beam_world(small).phase_steps == 4


def test_the_three_columns_default_to_no_record_and_leave_the_merge_key(tmp_path: Path):
    """(b)."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(lamp_world()))
    for _ in range(5):
        simulation.step()
    store = simulation.stores[0]
    assert store.size > 0
    assert (store.record == 0).all() and (store.branch == 0).all()
    assert (store.multiplicity == 1).all()
    assert all(beam.record == 0 and beam.multiplicity == 1 for beam in store.rows())
    for keyed in (False, True):
        out = tmp_path / ("keyed" if keyed else "plain")
        out.mkdir()
        execute_nature_beam_run(
            parse_nature_beam_world(lamp_world(amplitude=keyed)), b"{}", out, "test", 5
        )
        state = json.loads((out / "state.json").read_text())
        rows = [ray for node in state["nodes"] for f in node["families"] for ray in f["rays"]]
        assert rows
        assert all(("record" in ray) is keyed for ray in rows)
        assert all(("multiplicity" in ray) is keyed for ray in rows)
    # The packed key with the three default columns equals the six-field key.
    columns, sign = store.identity_columns()
    assert (sign == 1).all()
    packed = store.merge_key(columns)
    assert packed is not None
    six = store.merge_key(columns[:6])
    assert six is not None and (packed == six).all()


def store_of(rows: list[tuple[int, int, int, int]]) -> NatureBeamStore:
    """Rows (phase, amount, record, multiplicity) at one Node on +x."""
    store = NatureBeamStore((3, 3, 1))
    count = len(rows)
    store.append(
        node=np.full(count, 4),
        direction=np.full(count, 2),
        age=np.full(count, 3),
        phase=np.array([r[0] for r in rows]),
        number=np.full(count, 1),
        amount=np.array([r[1] for r in rows]),
        content=np.full(count, 1),
        arrival=np.zeros(count, dtype=np.int64),
        record=np.array([r[2] for r in rows]),
        branch=np.zeros(count, dtype=np.int64),
        multiplicity=np.array([r[3] for r in rows]),
    )
    return store


def rows_of(store: NatureBeamStore) -> list[tuple[int, int, int, int]]:
    return sorted((beam.phase, beam.amount, beam.record, beam.multiplicity) for beam in store.rows())


def test_the_normal_form_cancels_antiphase_rows_of_one_record():
    """(c)."""
    store = store_of(
        [
            (5, 3, 7, 2),
            (37, 2, 7, 2),
            (9, 1, 8, 1),
            (41, 1, 8, 1),
            (9, 1, 0, 1),
            (41, 1, 0, 1),
            (40, 1, 9, 1),
            (8, 2, 9, 1),
            (5, 1, 10, 1),
            (21, 1, 10, 1),
            (3, 1, 11, 1),
            (3, 1, 11, 1),
            (12, 1, 12, 2),
            (12, 1, 12, 4),
        ]
    )
    removed = store.merge(N)
    assert removed == {(7, 2): (4, 4), (8, 2): (2, 2), (9, 2): (2, 2)}
    assert rows_of(store) == [
        (3, 2, 11, 1),
        (5, 1, 7, 2),
        (5, 1, 10, 1),
        (8, 1, 9, 1),
        (9, 1, 0, 1),
        (12, 1, 12, 2),
        (12, 1, 12, 4),
        (21, 1, 10, 1),
        (41, 1, 0, 1),
    ]
    assert (store.arrival == 0).all()
    plain = store_of([(9, 1, 8, 1), (41, 1, 8, 1)])
    assert plain.merge() == {}
    assert rows_of(plain) == [(9, 1, 8, 1), (41, 1, 8, 1)]
