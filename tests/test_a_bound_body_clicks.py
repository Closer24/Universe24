"""The bound body's click as the Node's act (ALGEBRA.md, The board reads itself, the bound body's clause on the owner's sentence of 2026-10-24, 16:45 UTC: a record standing at a Node at a whole quantum of its own unit through one period of its beat is a bound body; its window one period; at the close the Node reads the light at it and its six Ports, the floor of the share over the record's unit, the remainder the whether divided by the unit once, the hole the board's own, the credit the record's; `meeting_board.bodies_closing`, `period_of`): the lone born pair on the 3-cube at den 1,021 (one birth, the selector then given no list), its two records standing at the birth Node, each clicking at the same close with its own identity, the light at the Node and its six Ports taken by the record's unit through the exact take, the quantum into the record by the click act, the credit line's eight keys the record's; and the same run bit for bit by three slabs through the first clicks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe import bound_body, meeting_board, share, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws_universe import SMALL, bare_torus

INTERVALS = 40  # the lone pairs born at one close (six Nodes under the gapped holder at 4) click within 40 intervals, one period of their beat after the light stands again at their Nodes


def lone_pair(monkeypatch: pytest.MonkeyPatch) -> None:
    """The selector given no list once a pair stands on the board (a charged family with records, `share.charged`): the lone pair, the test's seed hand in every process (every other act the engine's)."""
    real = meeting_board.child_of

    def once(board: Lattice, index: int, value: int, whole: int) -> Any:
        born = any(board.states[k].lines for k in board.order if share.charged(board.families[k]))
        return () if born else real(board, index, value, whole)

    monkeypatch.setattr(meeting_board, "child_of", once)


def test_the_lone_pairs_two_records_click_at_their_node_with_their_identities(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The records of the lone pairs are bound bodies at their birth Nodes and click there: a credit per record with its identity [family, record], its support a birth Node, both records of a Node clicking together, its windows the Node's own closes and its proper, point, kind, sense, beat and momentum keys; the light's summed share falls at the first clicking close by at least one unit per click (the exact take of each, nothing born there); the family's count in the books the children laid plus its clicks, the deficit the clicks (the quantum into the record, booked by the beam's rule where it stands above one quantum); the period of the beat read from the pair alone, 8 or 9 intervals for the two points of den 1,021."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    lines: list[dict[str, Any]] = []
    lone_pair(monkeypatch)
    board = Lattice(load_world(bare_torus(tmp_path, 3, INTERVALS)), output=lines.append)
    seed, light = board.world.seed, {}
    real = meeting_board.closed

    def spy(b: Lattice, begun: Any) -> None:
        before = int(np.asarray(b.share_of(seed)[0], dtype=object).sum())
        real(b, begun)
        light[b.interval] = (before, int(np.asarray(b.share_of(seed)[0], dtype=object).sum()))

    monkeypatch.setattr(meeting_board, "closed", spy)
    for _ in range(INTERVALS):
        board.step()
    born = {tuple(node) for row in lines if row["event"] == "birth" for node in row["nodes"]}
    first_birth = min(row["interval"] for row in lines if row["event"] == "birth")
    assert born and all(
        row["interval"] == first_birth for row in lines if row["event"] == "birth"
    )  # the one close's births: the lone pairs, one per Node born (six under the gapped holder)
    bodies = [row for row in lines if row["event"] == "credit" and row["identity"][0] != seed]
    assert bodies and all(len(row["support"]) == 3 for row in bodies)  # the bodies' Nodes the births'
    first = bodies[0]["interval"]
    at_first = [row for row in bodies if row["interval"] == first]
    assert all(
        row["identity"][1] in (0, 1) for row in bodies
    )  # the pair's two records, each its own body
    family = bodies[0]["identity"][0]
    keys = ("identity", "proper", "windows", "point", "kind", "sense", "support", "beat", "momentum")
    assert all(key in row for row in bodies for key in keys)
    assert all(row["windows"] >= 1 and row["kind"] == 2 and row["sense"] in (-1, 0, 1) for row in bodies)
    before, after = light[first]
    units = board.credit.units[family]
    assert (
        before - after >= len(at_first) * units
    )  # the light taken by a unit per click, the exact take of each
    assert not any(row["event"] == "birth" and row["interval"] == first for row in lines)
    laid = sum(
        row["children"].count(board.families[family].name) for row in lines if row["event"] == "birth"
    )
    clicks = sum(1 for row in bodies if row["identity"][0] == family)
    assert board.credit.counts[family] == laid + clicks and board.credit.deficits.get(family) == -clicks
    gamma = SMALL["integers"]["node_clock"]
    assert gamma and bound_body.period_of(board.families[family].pair) in (8, 9)
    assert bound_body.period_of(board.families[seed].pair) == 0  # the massless pair never turns: no body


def test_the_lone_pairs_clicks_run_the_same_by_three_slabs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The slabs' gate through a bound body's click (slabs.py: the bodies' standing counts exchanged with the arrays, the halo re-imposed before the close): the lone pairs on the 3-cube through their first clicks, one process against three one-layer slabs, every array, every line and the swaps' count equal."""
    from event_universe.slabs import Slabs, arrays_of

    runs = []
    for name, processes in (("one", 1), ("three", 3)):
        lines: list[dict[str, Any]] = []
        lone_pair(monkeypatch)
        folder = tmp_path / name
        folder.mkdir()
        monkeypatch.setattr(world_files, "REPOSITORY_ROOT", folder)
        board = Lattice(load_world(bare_torus(folder, 3, INTERVALS)), output=lines.append)
        slabs, states = Slabs(board, processes), []
        assert slabs.count == processes
        for _ in range(INTERVALS):
            slabs.advanced()
            states.append([np.asarray(a, dtype=object).copy() for a in arrays_of(board)])
        slabs.close()
        runs.append((states, lines, list(board.swaps), board.world.seed))
    (single, lines_one, swaps_one, seed), (three, lines_three, swaps_three, _seed) = runs
    assert all(
        np.array_equal(x, y)
        for a, b in zip(single, three, strict=True)
        for x, y in zip(a, b, strict=True)
    )
    assert lines_one == lines_three and swaps_one == swaps_three
    assert any(row["event"] == "credit" and row["identity"][0] != seed for row in lines_one)
