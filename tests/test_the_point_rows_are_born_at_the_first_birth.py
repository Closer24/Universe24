"""The point rows born at the first birth (2026-10-24, the architect's field view (c) on the Boss's order: the lattice's arrays grow per point and not per child, nothing at the Node naming a body): a point's records and its rows of the holder of the sign are born at its first lay by the count (`Lattice.born_point`, `emission.laid_by_count`) and not at the start, so the step before any birth pays for no empty record (0.42 s against 0.008 s per interval at the PeV den, 98 percent of the step the 52 empty records and their rows); every state the law reads and every output line the same as with every record standing from the start, by the theorem of the zero rows: an empty record enters every sum as 0, its row's write divides 0 and keeps its remainder, and its phase row is read by no level."""

import numpy as np

from event_universe import registry, world_files
from event_universe.lattice import Lattice
from event_universe.loader.derived import charged
from event_universe.world_files import load_world
from tests.laws_universe import bare_torus


def test_the_lean_board_equals_the_board_with_every_point_standing_through_the_births(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The 3-cube hole seed (SMALL, den 1,021) over 24 intervals, births at 2, 4, 6 and on: the lean board, no point record and the free row alone before the first birth, two records and three rows after it, against its twin with every point's records born at the start (the configuration to 2026-10-24, `born_point` for every charged family before the first interval), equal bit for bit on every label they share, the holders' lines and write remainders, the light, every born point's records and its rows' lines, write remainders and phase rows, and on every output line, the twin's records and rows of the unborn point carrying no level; the step back through a birth returns the lean board (`unborn_point`) and the step at the Nodes alone born again (`step` with no act) returns the board the run left."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = bare_torus(tmp_path, 3, 30)
    outputs: dict[str, list[dict]] = {"lean": [], "full": []}  # type: ignore[type-arg]
    lean = Lattice(load_world(path), output=outputs["lean"].append)
    full = Lattice(load_world(path), output=outputs["full"].append)
    for index in range(len(full.families)):
        if charged(full.families, index):
            full.born_point(index)  # every point standing from the start, as to 2026-10-24
    full.born_at.clear()
    sign = next(i for i, f in enumerate(lean.families) if f.held and f.wronskian)

    def labelled(board):  # type: ignore[no-untyped-def]
        """Every array of the board by its label: a record's lines by (family, record), a row of the sign by its owner, a holder whole."""
        found = {}
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

    def equal(interval):  # type: ignore[no-untyped-def]
        """The two boards equal on every shared label, the twin's extra labels at no level, the output lines equal."""
        mine, theirs = labelled(lean), labelled(full)
        assert set(mine) <= set(theirs), (interval, set(mine) - set(theirs))
        assert all(same(mine[k], theirs[k]) for k in mine), interval
        assert all(not np.asarray(theirs[k][0]).any() for k in set(theirs) - set(mine)), interval
        assert outputs["lean"] == outputs["full"], interval

    points = [i for i in lean.order if charged(lean.families, i)]
    assert all(registry.records_of(lean.families[i], lean.states[i].lines) == 0 for i in points)
    assert registry.records_of(lean.families[sign], lean.states[sign].lines) == 1
    equal(0)
    for _ in range(24):
        lean.step()
        full.step()
        equal(lean.interval)
    born = [i for i in points if registry.records_of(lean.families[i], lean.states[i].lines)]
    assert born and all(registry.records_of(lean.families[i], lean.states[i].lines) == 2 for i in born)
    assert registry.records_of(lean.families[sign], lean.states[sign].lines) == 1 + 2 * len(born)
    assert (
        sorted(lean.born_at)
        == sorted({line["interval"] for line in outputs["lean"] if line.get("event") == "birth"})[
            : len(lean.born_at)
        ]
    )
    first = min(lean.born_at)
    while (
        lean.interval >= first
    ):  # back through the first birth: the records and rows born there are gone
        lean.step_inverse()
    assert all(registry.records_of(lean.families[i], lean.states[i].lines) == 0 for i in points)
    assert registry.records_of(lean.families[sign], lean.states[sign].lines) == 1
