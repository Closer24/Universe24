"""The held write at the row's own paces (ALGEBRA.md, The one Node, the clause of 2026-10-23; `records.wall_rulers`, `Lattice.rulers`, `loader/derived.shared_clock`): every act of the interval sees the Node's own clock and ruler, the held rows' write among them (The same clock and the same ruler for every act), and a held row reads the content as every family does (Every row reads the content), so the write's factor of every source of a row that reads the content is scaled at the row's own paces, one wall per line, and readers at differing read weights share the row's wall and not a reader's clock; where the readers read as the row does, the number is the former's bit for bit (every shipped world). A row that reads no content, a holder of the sign reading none, keeps its sources' shared paces as the wall and the loader's gate keeps them alike by name. The sentences asserted on the 3-cube torus of tests/laws_universe.small_world with gravity gapped: (1) matter reading gravity at the weight 2 beside light at 1 loads where it was refused by name, steps, every held line's remainder in [0, wall) at every Node (the one remainder per held line, exact), and runs back to the start bit for bit; (2) the same world with the sign holder `charge` reading no content and its readers, the proton and the electron, at differing weights of gravity is refused at load by name, the sentence not holding there."""

import hashlib
import json

import numpy as np
import pytest

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests import laws_universe


def digest(board: Lattice) -> str:
    found = hashlib.sha256()
    for state in board.states:
        for line in [*state.lines, *state.write_remainders]:
            for part in (line.now, line.before, line.remainder) if hasattr(line, "now") else (line,):
                found.update(json.dumps(np.asarray(part, dtype=object).reshape(-1).tolist()).encode())
    return found.hexdigest()


def weighed(tmp_path, monkeypatch, matter: int, electron: int):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = laws_universe.small_world(tmp_path, detector=False)
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    for family in universe["families"]:
        if family["name"] == "matter":
            family["reads"]["gravity"] = matter
        if family["name"] == "electron":
            family["reads"]["gravity"] = electron
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    return load_world(path)


def test_a_reader_at_another_weight_shares_the_rows_wall_and_the_run_back_is_exact(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    board = Lattice(weighed(tmp_path, monkeypatch, 2, 1), None)
    g = board.held[0]
    assert board.families[g].pair[0] < board.families[g].pair[1]  # a gapped row
    weights = {board.families[r].name: r for r in range(len(board.families))}
    assert [r.weight for r in board.families[weights["matter"]].reads if r.family == g] == [2]
    assert [r.weight for r in board.families[weights["light"]].reads if r.family == g] == [1]
    kept = {0: digest(board)}
    for _ in range(12):
        board.step()
        kept[board.interval] = digest(board)
        assert board.fixed_walls[
            g
        ]  # the carried factor's wall fixed per Node at the start, the volume's line at Gamma times it (board.write_walls)
        for line, wall in zip(board.states[g].write_remainders, board.write_walls[g], strict=True):
            remainder = np.asarray(line, dtype=object)
            assert bool((remainder >= 0).all()) and bool(
                (remainder < np.asarray(wall, dtype=object)).all()
            )
    assert len(set(kept.values())) == 13  # the row moves under its sources
    for k in range(12):
        board.step_inverse()
        assert digest(board) == kept[12 - k - 1], board.interval


def test_a_row_reading_no_content_keeps_the_gate_where_its_sources_differ(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    with pytest.raises(
        ValueError, match="'charge' reads no content and its sources read the content at differing"
    ):
        weighed(tmp_path, monkeypatch, 1, 2)
