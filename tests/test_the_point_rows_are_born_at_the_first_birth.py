"""The point rows born at the first birth (2026-10-24, the architect's field view (c) on the Boss's order: the lattice's arrays grow per point and not per child, nothing at the Node naming a body): a point's records and its rows of the holder of the sign are born at its first lay by the count (`emission.born_point`, `emission.laid_by_count`) and not at the start, so the step before any birth pays for no empty record (0.42 s against 0.008 s per interval at the PeV den, 98 percent of the step the 52 empty records and their rows); every state the law reads and every output line the same as with every record standing from the start, by the theorem of the zero rows: an empty record enters every sum as 0, its row's write divides 0 and keeps its remainder, and its phase row is read by no level; the one act that read the empty records was the draw's number (their remainders at the origin as digits, the Boss's ruling of the day: a record that holds no quantum is no read of the board), so the two boards part at the first whether whose outcome those digits turned, named here and not asserted equal."""

import numpy as np

from event_universe import meeting_board, registry, seed, world_files
from event_universe.lattice import Lattice
from event_universe.loader import universe
from event_universe.loader.derived import charged
from event_universe.world_files import load_world
from tests.laws_universe import bare_torus, uniform_sea


def test_the_lean_board_equals_the_board_with_every_point_standing_through_the_births(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """SMALL (den 1,021) on the 3-cube: the lean board, no point record and the free row alone before the first birth, two records and three rows after it, against its twin with every point's records born at the start (the configuration to 2026-10-24, `born_point` for every charged family before the first interval), equal bit for bit on every label they share (the holders' lines and write remainders, the light, every born point's records and its rows' lines, write remainders and phase rows) and on every output line: under the uniform sea over 30 intervals through its births at 24 (every Node two whole quanta, no whether drawn); under the hole seed until the first draw whose outcome the twin's empty digits turn (the parting after the first birth at 2, named in the test's output and not asserted equal), the twin's unborn records and rows at no level throughout; the step back through the first birth returns the lean board's counts (`unborn_point`)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(
        universe, "volume_pair", lambda den, gamma: (den, den)
    )  # the massless holder, by name: the course's numbers were read on it (the holder gapped by the clock's level turns the hole's Node from the interval 1)
    path = bare_torus(tmp_path, 3, 40)
    drawn: list[int] = []
    read_of = meeting_board.read_of

    def spied(board, reads, label):  # type: ignore[no-untyped-def]
        drawn.append(board.interval)
        return read_of(board, reads, label)

    monkeypatch.setattr(meeting_board, "read_of", spied)

    def twins():  # type: ignore[no-untyped-def]
        outputs: dict[str, list[dict]] = {"lean": [], "full": []}  # type: ignore[type-arg]
        lean = Lattice(load_world(path), output=outputs["lean"].append)
        full = Lattice(load_world(path), output=outputs["full"].append)
        for index in range(len(full.families)):
            full.born_point(index)  # every point standing from the start, as to 2026-10-24
        full.born_at.clear()
        return lean, full, outputs

    def labelled(board):  # type: ignore[no-untyped-def]
        """Every array of the board by its label: a record's lines by (family, record), a row of the sign by its owner, a holder whole."""
        found = {}
        sign = next(i for i, f in enumerate(board.families) if f.held and f.wronskian)
        for i, (f, st) in enumerate(zip(board.families, board.states, strict=True)):
            if i == sign:
                for row, owner in enumerate(registry.rows_of(board.families, board.states)):
                    span = slice(row * f.width, (row + 1) * f.width)
                    found[("row", owner)] = (
                        [a for r in st.lines[span] for a in (r.now, r.before, r.remainder)]
                        + list(st.write_remainders[span])
                        + [a for r in st.phases[row] for a in (r.now, r.before, r.remainder)]
                    )
            elif f.quanta:
                for record in range(registry.records_of(f, st.lines)):
                    found[("record", i, record)] = [
                        a for r in board.lines_of(i, record) for a in (r.now, r.before, r.remainder)
                    ]
            else:
                found[("holder", i)] = [
                    a for r in st.lines for a in (r.now, r.before, r.remainder)
                ] + list(st.write_remainders)
        return found

    def same(a, b):  # type: ignore[no-untyped-def]
        return len(a) == len(b) and all(np.array_equal(x, y) for x, y in zip(a, b, strict=True))

    def equal(lean, full, outputs, interval):  # type: ignore[no-untyped-def]
        """The two boards equal on every shared label, the twin's extra labels at no level, the output lines equal."""
        mine, theirs = labelled(lean), labelled(full)
        assert set(mine) <= set(theirs), (interval, set(mine) - set(theirs))
        assert all(same(mine[k], theirs[k]) for k in mine), interval
        assert all(not np.asarray(theirs[k][0]).any() for k in set(theirs) - set(mine)), interval
        assert outputs["lean"] == outputs["full"], interval

    def counts(board):  # type: ignore[no-untyped-def]
        sign = next(i for i, f in enumerate(board.families) if f.held and f.wronskian)
        points = [i for i in board.order if charged(board.families, i)]
        return [
            registry.records_of(board.families[i], board.states[i].lines) for i in points
        ], registry.records_of(board.families[sign], board.states[sign].lines)

    monkeypatch.setattr(
        seed, "uniform_seed", uniform_sea
    )  # the sea: every Node two whole quanta at 24, no draw
    lean, full, outputs = twins()
    assert counts(lean) == ([0, 0], 1)
    for _ in range(30):
        lean.step()
        full.step()
        equal(lean, full, outputs, lean.interval)
    assert (
        not drawn and sorted(lean.born_at) == [24] and counts(lean) == ([0, 2], 3)
    )  # the lift point 2's two records and its two rows (the selector births the lift, 2026-10-24; the swap point -2, the first charged family, under the former clause)
    monkeypatch.undo()  # the hole seed, the law's own
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(
        universe, "volume_pair", lambda den, gamma: (den, den)
    )  # the massless holder, by name
    monkeypatch.setattr(meeting_board, "read_of", spied)
    lean, full, outputs = twins()
    parting = None
    for _ in range(24):
        lean.step()
        full.step()
        if parting is None and outputs["lean"] != outputs["full"]:
            parting = lean.interval  # the first whether whose outcome the twin's empty digits turned
            print(
                f"the hole seed's boards part at the interval {parting}, the first draw at {min(drawn)}"
            )
        if parting is None:
            equal(lean, full, outputs, lean.interval)
    first = min(lean.born_at)
    assert first == 2 and drawn and (parting is None or parting >= min(drawn) > first)
    born, rows = counts(lean)
    assert sum(1 for n in born if n) >= 1 and all(n in (0, 2) for n in born) and rows == 1 + sum(born)
    while (
        lean.interval >= first
    ):  # back through the first birth: the records and rows born there are gone
        lean.step_inverse()
    assert counts(lean) == ([0, 0], 1)
