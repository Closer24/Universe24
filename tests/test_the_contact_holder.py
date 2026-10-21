"""The contact holder, a held row at the frozen pair [0, den] (2026-10-21; ALGEBRA.md, The conversion: "a contact coupling 3 / kappa^2 would need a range below one Link", the row at the pair [0, den] being that range; The frozen Node has no share): sourced by the Wronskian like the sign holder and read by a plane under the act `pace`, its hop coefficient R_ij = 2 num p_i^2 Q_ij is 0, so no read stands on any Port, the start's fine unit for its rest is bounded by the line's own wall (features/start `unit_from_bound`, where the six reads bound nothing), its rest is the source over 2 at the sourcing Node and the integer 0 elsewhere, exactly, where a massless holder of the sign at the same write weight rests as Coulomb's over the board, and over the run its one write stands where the record's pair has reached and nowhere else, now and before, bit for bit (the row has no hop); a row of the same pair that nothing sources stands at 0 everywhere."""

import json

import numpy as np

from event_universe import records, world_files
from event_universe.core.integer import MAX_WORK_INT
from event_universe.features.start import unit_from_bound
from event_universe.lattice import Lattice
from event_universe.loader.universe import universe_of
from event_universe.world_files import load_world
from tests.laws import TURNING_FILE, TURNING_T, sign_world

HELD = {
    "sources": ["wronskian"],
    "level_weight": 1,
    "write_weight": 96,
    "act": "pace",
}  # k_W 96: one quantum's Wronskian T / 2 over the wall T writes 48 levels per interval at the Node (a quarter of a level at k_W 1, stored 0 and dithered, ALGEBRA.md, The law's alpha is a coefficient of the file)
WEAK = {"name": "weak", "pair": [0, 6000], "reads": {}, "held": HELD}  # the contact holder
NEAR = {**WEAK, "name": "near", "pair": [6000, 6000]}  # the same row with the hop: Coulomb's rest
UNREAD = {**WEAK, "name": "unread"}  # a contact holder no family reads: sourced by nothing
OPEN = dict(x="open", y="open", z="open")
SHAPE, CENTRE = (7, 7, 7), (3, 3, 3)


def universe_with(folder, *rows):  # type: ignore[no-untyped-def]
    """turning.json's universe with `rows` added and the charged plane reading `weak` and `near` at 1, and so sourcing each by its Wronskian (the held write's reciprocity), written beside the world as its `u.json`."""
    document = json.loads(TURNING_FILE.read_text(encoding="utf-8"))
    charged = next(row for row in document["families"] if row["name"] == "charged")
    charged["reads"].update({row["name"]: 1 for row in rows if row["name"] != "unread"})
    document["families"] += list(rows)
    (folder / "u.json").write_text(json.dumps(document), encoding="utf-8")
    return universe_of(document)[1]


def test_the_row_at_the_frozen_pair_rests_at_its_source_alone_and_its_write_spreads_nowhere(
    tmp_path, monkeypatch
):
    """The loader admits a held row at the pair [0, den] sourced by the Wronskian, one row per charged record beside its free row; the start's fine unit for a row with no read on any Port is bounded by the line's own wall (`unit_from_bound`: 0 from the six reads, a unit from the wall); on an open 7-cube with one charged record of count 1 at the centre, the weak row rests at the source over 2 at the record's Node, now and before alike, and at the integer 0 at every other Node, while the massless row `near`, sourced by the same Wronskian at the same write weight, rests over the board as Coulomb's; over three intervals the weak row holds the integer 0, now and before, at every Node the record's pair has not reached (its Wronskian 0 before and after every step, so no write took a booking there), while the record spreads by its hop, and the row `unread` stands at 0 everywhere."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    d = np.abs(np.indices(SHAPE) - 3).sum(axis=0)
    path = sign_world(tmp_path, "contact", SHAPE, OPEN, 3, CENTRE, np.where(d == 0, 1200, 0))
    families = universe_with(tmp_path, WEAK, NEAR, UNREAD)
    names = [family.name for family in families]
    weak, near, unread, charged = (names.index(n) for n in ("weak", "near", "unread", "charged"))
    assert families[weak].held and families[weak].wronskian and families[weak].pair == (0, 6000)
    assert families[weak].records == 2  # the free row and the one charged record's own
    assert unit_from_bound(12, (0, 6000), MAX_WORK_INT, 6000) >= 1  # the unit from the line's wall
    board = Lattice(load_world(path))
    sourced = np.asarray(records.wronskian(board.lines_of(charged, 0), True)) != 0
    assert sourced.sum() == 1 and sourced[CENTRE]  # the one-Node record sources at its Node alone
    level, spread = board.record(weak)[0], board.record(near)[0]
    wronskian = int(np.asarray(records.wronskian(board.lines_of(charged, 0), True))[CENTRE])
    assert int(level.now[CENTRE]) == round(96 * wronskian / TURNING_T / 2) > 10  # the source over 2
    assert np.array_equal(level.now, level.before) and not level.now[~sourced].any()
    assert np.count_nonzero(np.asarray(spread.now)[~sourced]) > 100  # the hop's rest spreads
    assert int(spread.now[CENTRE]) > int(spread.now[3, 3, 4]) > 0 and int(spread.now[0, 0, 0]) == 0
    assert not board.record(unread)[0].now.any()  # sourced by nothing: 0 everywhere
    ever = sourced.copy()
    for _interval in range(3):
        board.step()
        ever |= (
            np.asarray(records.wronskian(board.lines_of(charged, 0), True)) != 0
        )  # the step's booking
        level = board.record(weak)[0]
        assert not level.now[~ever].any() and not level.before[~ever].any()
        assert not board.record(unread)[0].now.any() and not board.record(unread)[0].before.any()
    assert (
        int(np.abs(level.now[CENTRE])) > 0 and ever.sum() > 1
    )  # the record spreads, the row follows it
