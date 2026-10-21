"""The Lorentz form on the sign holder's four lines (covector.py; the universe file's key `form`: `lorentz` on a held row under the rotation, `loader/universe.form_of`; ALGEBRA.md #the-hypotheses-under-their-own-names, The odd line's source is the sign's own current; the covector form declared on 2026-10-21): the declaration read into the walls and the Link's read, the refusals by name; the law's exact continuity identity of a turned record's step held bit for bit at every Node over a short run, w (W(t) - W(t + 1)) = p^2 SUM_a (Phi_a(i) - Phi_a(i - a)) + Im(conj(z) (r - r')), the odd lines' source the flux Phi of that identity; the lattice Lorenz constraint 3 (L_0(t) - L_0(t - 1)) + SUM_a (L_a(i) - L_a(i - a)) at 0 at the lay and within the roundings' walk over the run; and the loader's gate at the lay, refusing by name a packet laid on the time line alone."""

import json
import math

import numpy as np
import pytest

from event_universe import board_readings, covector, world_files
from event_universe.core import paces
from event_universe.core.ports import arrival
from event_universe.core.rule3 import wall_of
from event_universe.lattice import Lattice
from event_universe.loader.derived import held_write_of
from event_universe.loader.universe import universe_of
from event_universe.records import Record
from event_universe.world_files import input_digest, load_world
from tests.laws import SINE, TURNING_FILE, TURNING_PAIR, TURNING_T

GAMMA, UNIT = 6000, 16
CLOSED = dict(x="closed", y="closed", z="closed")


def universe_with(form: str | None, on: str = "charge", pair: list[int] | None = None) -> dict:
    """turning.json's universe with the key `form` on the row `on` (absent where `form` is None), the row's pair replaced where `pair` is given."""
    document = json.loads(TURNING_FILE.read_text(encoding="utf-8"))
    for row in document["families"]:
        if row["name"] == on:
            if form is not None:
                row["held"]["form"] = form
            if pair is not None:
                row["pair"] = pair
    return document


def covector_world(tmp_path, shape, centre, profile, form="lorentz"):  # type: ignore[no-untyped-def]
    """A world on turning.json's universe with the charge holder under the form `form` and one charged record by hand at the count 1 on a closed cube, as tests/laws.sign_world lays it: the level now (L, 0) over `profile`, the level before the band's rest rotation in the sense +1."""
    (tmp_path / "u.json").write_text(json.dumps(universe_with(form)), encoding="utf-8")
    values = [int(v) for v in np.asarray(profile).ravel()]
    scale = math.isqrt(
        TURNING_T * TURNING_PAIR[1] * 1000 * 1000 // (2 * SINE * sum(v * v for v in values))
    )
    levels = [v * scale // 1000 for v in values]
    moving = dict(now=levels, before=[v * TURNING_PAIR[0] // TURNING_PAIR[1] for v in levels])
    moving.update(im_now=[0] * len(levels), im_before=[v * SINE // TURNING_PAIR[1] for v in levels])
    body = {"family": "charged", "nodes": [{"node": list(centre), "count": 1}]}
    world = dict(shape=list(shape), boundary=CLOSED, face_depth=1, intervals=8)
    world.update(universe="u.json", node_detectors=[], bodies=[body])
    (path := tmp_path / "cube.json").write_text(json.dumps(world), encoding="utf-8")
    mode = {"family": "charged", "pair": list(TURNING_PAIR), "moving": moving}
    beside = {"world_digest": input_digest(world), "bodies": [mode]}
    path.with_suffix(".mode.json").write_text(json.dumps(beside), encoding="utf-8")
    world_files.REPOSITORY_ROOT = tmp_path
    return Lattice(load_world(path))


def test_the_form_is_declared_into_the_walls_and_the_links_read_and_refused_by_name():
    """The key read: the charge holder under `lorentz` is a covector, its Link read (-2, 0), its odd lines' walls 2 den_s G^2 E_s T beside the time line's E_s T with the one source's den (charged, [4000, 6000]) and its factor 1; `positive` and the absent key the rows as the engine books them, (1, 1) and 2 E_s T; refused by name: a word outside the two, the form on a holder of the content (the act pace), on a holder with a gap."""
    integers, families = universe_of(universe_with("lorentz"))
    charge = [f.name for f in families].index("charge")
    assert families[charge].lorentz and families[charge].link_read == (-2, 0)
    write = held_write_of(families, charge, integers["quantum_action"], integers["link_unit"])
    e_s, action = families[charge].level_weight, integers["quantum_action"]
    assert e_s is not None
    odd = 2 * 6000 * UNIT * UNIT * e_s * action
    assert write.walls == (e_s * action, odd, odd, odd) * families[charge].records
    charged = [f.name for f in families].index("charged")
    assert write.factors == {charged: 1}
    for form in (None, "positive"):
        _integers, plain = universe_of(universe_with(form))
        assert not plain[charge].lorentz and plain[charge].link_read == (1, 1)
        plain_write = held_write_of(plain, charge, action, UNIT)
        assert (
            plain_write.walls == (e_s * action, 2 * e_s * action, 2 * e_s * action, 2 * e_s * action) * 2
        )
    with pytest.raises(ValueError, match="held.form is one of"):
        universe_of(universe_with("minkowski"))
    with pytest.raises(ValueError, match="the holder of the sign under the act 'rotation'"):
        universe_of(universe_with("lorentz", on="gravity"))
    with pytest.raises(ValueError, match="one covector over one massless line"):
        universe_of(universe_with("lorentz", pair=[5999, 6000]))


def test_the_continuity_identity_holds_bit_for_bit_and_the_constraint_stands(tmp_path):  # type: ignore[no-untyped-def]
    """One charged record on a closed cube of 7^3 under the Lorentz form, eight intervals: at every interval the exact continuity identity of the record's step, w (W(t) - W(t + 1)) - p_i^2 SUM_a (Phi_a(i) - Phi_a(i - a)) - Im(conj(z) (r - r')) = 0 at every Node bit for bit under the content's paces (gravity's and the binding's wells of turning.json, p_i the Node's pace, Gamma in the vacuum), Phi the flux the odd lines are written from (`covector.link_fluxes` at the pairs the step reads, `Lattice.sense_fluxes`), w the record's wall 6 den Gamma^2 G^2; the lattice Lorenz constraint of the record's row (`covector.residual`) 0 at the lay and within the roundings' walk after, at most 12 units per interval (two divisions per line, six lines), the standing record's odd lines at 0 (no current); an odd line's level along a Link read from either end the same size with the opposite sign and minus twice the +a Link's own line (`plane.link_levels` at (-2, 0), the hop's sign of Peierls' p - q A)."""
    shape, centre = (7, 7, 7), (3, 3, 3)
    d = np.abs(np.indices(shape) - 3).sum(axis=0)
    profile = np.select([d == 0, d == 1, d == 2], [1200, 600, 200], 0)
    board = covector_world(tmp_path, shape, centre, profile)
    names = [f.name for f in board.families]
    charge, charged = names.index("charge"), names.index("charged")
    holder, record = board.families[charge], board.families[charged]
    assert holder.lorentz and holder.records == 2  # the free row and the record's own
    for found in covector.residual(holder, board.states[charge].lines, board.wrap):
        assert not found.any()  # the constraint at the lay: the rests static, the odd lines at 0
    wall = wall_of(record.pair[1], GAMMA, UNIT)
    bound = 0
    for interval in range(1, 9):
        re, im = board.states[charged].lines
        kept = (re.before.copy(), im.before.copy(), re.remainder.copy(), im.remainder.copy())
        board.step()
        re_n, im_n = board.states[charged].lines
        re_t, im_t = (
            re_n.before.astype(object),
            im_n.before.astype(object),
        )  # the levels the step started from
        w_t = re_t * kept[1].astype(object) - im_t * kept[0].astype(object)
        w_n = re_n.now.astype(object) * im_t - im_n.now.astype(object) * re_t
        start = [Record(re_n.before, kept[0], kept[2]), Record(im_n.before, kept[1], kept[3])]
        flux = board_readings.sense_fluxes(board, (charged, 0), start, -1)
        divergence: object = 0
        for axis in range(3):
            f = np.asarray(flux[axis]).astype(object)
            divergence = divergence + f - arrival(f, axis, -1, board.wrap)
        remainders = re_t * (kept[3].astype(object) - im_n.remainder.astype(object)) - im_t * (
            kept[2].astype(object) - re_n.remainder.astype(object)
        )
        content, _factors = board.read(charged, -1, 0)  # the record's read at the interval's start
        square = (
            paces.link_pace_of(GAMMA, content) ** 2
        )  # the Node's pace squared, Gamma^2 in the vacuum
        residual = wall * (w_t - w_n) - square * divergence - remainders
        assert not np.asarray(residual).any(), f"the identity fails at interval {interval}"
        constraint = covector.residual(holder, board.states[charge].lines, board.wrap)[1]
        bound = max(bound, int(np.abs(constraint).max()))
        assert bound <= 12 * interval, (
            f"the constraint walks beyond the roundings at interval {interval}"
        )
    odd = [line.now for line in board.states[charge].lines[holder.width + 1 : 2 * holder.width]]
    assert not any(
        int(np.abs(level).max()) for level in odd
    )  # a standing record: no current, no odd level
    from event_universe.plane import link_levels

    levels = tuple(np.indices(shape)[axis] * (axis + 1) - axis for axis in range(3))  # a line by hand
    links = link_levels(levels, board.wrap, holder.link_read)
    for axis in range(3):
        plus, minus = np.asarray(links[2 * axis]), np.asarray(links[2 * axis + 1])
        assert np.array_equal(arrival(plus, axis, -1, board.wrap), -minus)  # n_ji = -n_ij exactly
        assert np.array_equal(
            plus, -2 * levels[axis]
        )  # minus twice the +a Link's own line, the hop's sign


def test_a_lay_that_breaks_the_constraint_is_refused_by_name(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The loader's gate at the lay: `Lattice.__init__` calls `covector.gate` on the laid board once; a packet laid on the holder's time line alone (its level now off its level before at a Node, the odd lines at 0) breaks the constraint and is refused by name with the holder, the row, the Node and the residual; the same packet on a holder without the form passes the gate, which reads no such holder."""
    shape, centre = (5, 5, 5), (2, 2, 2)
    d = np.abs(np.indices(shape) - 2).sum(axis=0)
    profile = np.select([d == 0, d == 1], [1200, 400], 0)
    calls: list[int] = []
    gate = covector.gate
    monkeypatch.setattr(covector, "gate", lambda board: calls.append(len(board.states)) or gate(board))
    board = covector_world(tmp_path, shape, centre, profile)
    assert calls == [len(board.families)]  # once, at the lay
    charge = [f.name for f in board.families].index("charge")
    time = board.states[charge].lines[0]  # the free row's time line, light's record
    now = time.now.copy()
    now[2, 2, 2] += 7
    board.states[charge].lines[0] = Record(now, time.before, time.remainder)
    with pytest.raises(
        ValueError,
        match="breaks the lattice Lorenz constraint of 'charge'.*row 0 at the Node \\(2, 2, 2\\).*= 21",
    ):
        gate(board)
    plain = covector_world(tmp_path, shape, centre, profile, form="positive")
    time = plain.states[charge].lines[0]
    now = time.now.copy()
    now[2, 2, 2] += 7
    plain.states[charge].lines[0] = Record(now, time.before, time.remainder)
    gate(plain)  # no holder under the form: nothing to refuse
