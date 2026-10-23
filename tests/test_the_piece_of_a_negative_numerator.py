"""The piece's momentum of a record of a negative numerator (issue #2169, finding 3; the reader's ruling of 2026-10-21; ALGEBRA.md, The tension, the dated word, and the piece's line under The lattice momentum): `node_detector.piece_momentum` guarded on the signed wall num x W(region), so a negative numerator's passage read as nothing passed and the credit line carried the piece [0, 0, 0]; the guard is on the share alone and the division by the signed wall as the law writes it, the rounding half up on the magnitude with the sign of num after (kind D as before). The builder's chain: the neutron pair [-4800, 6000] laid as a packet of three real lines at the weights (7, 7, 5), the wave [-1, 4] along +x (the band inverted, a record moving toward +x at sin k below 0), two regions of four Nodes, the window 95; at the right region's close one credit line, the piece -43,250 along x where the engine gave 0, with the fan -73,186: the law's P_a = F / num against the motion for a negative numerator, the rest at the band's top, and the piece one count's P_a with it; the integers pinned."""

from __future__ import annotations

import json
from pathlib import Path

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.node_detector import Passage, piece_momentum
from event_universe.world_files import load_world
from tests.laws import TOOL

UNIVERSE = {
    "integers": {"node_clock": 6000, "quantum_action": 32768, "width": 63, "link_unit": 16},
    "families": [
        {
            "name": "gravity",
            "pair": [6000, 6000],
            "reads": {"gravity": 1, "binding": 1},
            "held": {
                "sources": ["form", "tensions"],
                "level_weight": 1000,
                "write_weight": 1,
                "rest": 60,
            },
        },
        {
            "name": "charge",
            "pair": [6000, 6000],
            "reads": {"gravity": 1, "binding": 1},
            "held": {"sources": ["wronskian"], "level_weight": 1, "write_weight": 1},
        },
        {
            "name": "binding",
            "pair": [2400, 2401],
            "reads": {"gravity": 1, "binding": 1},
            "held": {"sources": ["form"], "level_weight": 1, "write_weight": 1},
        },
        {
            "name": "neutron",
            "pair": [-4800, 6000],
            "reads": {"gravity": 1, "binding": 1},
            "dimension": 3,
        },
        {
            "name": "proton",
            "pair": [0, 6000],
            "reads": {"gravity": 1, "binding": 1, "charge": 1},
            "dimension": ["plane", "plane", "plane"],
        },
        {
            "name": "electron",
            "pair": [4000, 6000],
            "reads": {"gravity": 1, "binding": 1, "charge": 1},
            "dimension": 2,
        },
        {
            "name": "antineutrino",
            "pair": [6000, 6000],
            "reads": {"gravity": 1, "binding": 1},
            "dimension": 1,
        },
    ],
}
WINDOW = 95
WORLD = {
    "shape": [61, 1, 1],
    "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
    "face_depth": 1,
    "intervals": WINDOW,
    "universe": "u.json",
    "bodies": [],
    "packets": [
        {
            "family": "neutron",
            "along": "x",
            "wave": [-1, 4],
            "phase": [0, 1],
            "amplitude": 12,
            "top": {"x": [20, 20], "y": [0, 0], "z": [0, 0]},
            "edge": {"x": 6, "y": 0, "z": 0},
            "weights": [7, 7, 5],
        }
    ],
    "node_detectors": [
        {"name": "left", "positions": [[x, 0, 0] for x in range(4)]},
        {"name": "right", "positions": [[x, 0, 0] for x in range(44, 48)]},
    ],
    "receding": {"x": {"sides": ["low", "high"], "largest": 400, "layers": 16}},
    "draw": {},
}
PIECE, FAN = -43250, -73186  # the chain's piece along x at the right region's close and the fan's P_x


def chain_world(folder: Path) -> Path:
    """The builder's chain world written beside its universe, its mode file the generator's."""
    (folder / "u.json").write_text(json.dumps(UNIVERSE) + "\n", encoding="utf-8")
    path = folder / "w.json"
    path.write_text(json.dumps(WORLD) + "\n", encoding="utf-8")
    TOOL.main(["--input", str(path)])
    return path


def test_the_piece_of_a_negative_numerator_is_one_counts_p_a_with_the_fans_sign(tmp_path, monkeypatch):
    """One window on the chain: the neutron packet of count 2 crosses the right region; at the close one credit line at the right region, the count moved 1, the piece's p_x PIECE below 0 and the fan's P_x FAN below 0, the two the law's P_a of a negative numerator (where the engine gave [0, 0, 0] by the guard on the signed wall); the left region books no quantum."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(chain_world(tmp_path)), (lines := []).append)
    neutron = [f.name for f in board.families].index("neutron")
    assert board.families[neutron].pair == (-4800, 6000) and board.credit.counts[neutron] == 2
    for _interval in range(WINDOW):
        board.step()
    credits = [line for line in lines if line.get("event") == "credit"]
    print(f"the credit lines at the close: {credits}")
    assert [(c["node_detector"], c["interval"], c["count"]) for c in credits] == [("right", WINDOW, 1)]
    assert credits[0]["momentum"] == [PIECE, 0, 0] and credits[0]["fan"] == [FAN, 0, 0]
    assert PIECE < 0 and FAN < 0 and board.credit.counts[neutron] == 1


def test_the_guard_is_on_the_share_alone_and_the_sign_is_nums(tmp_path, monkeypatch):
    """`piece_momentum` by its arithmetic: a positive numerator's piece as before (the division by num x W rounded half up on the magnitude with the sign after), a negative numerator's the same magnitude with the sign flipped, a share at 0 or below nothing passed, and the frozen pair num = 0 nothing passed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(chain_world(tmp_path)))
    names = [f.name for f in board.families]
    neutron, electron, proton = (names.index(n) for n in ("neutron", "electron", "proton"))
    units = board.credit.units
    passage = Passage([2118926400, 0, -2118926400], 3612117122)  # the chain's right region's sums
    assert piece_momentum(board, neutron, passage) == [PIECE, 0, -PIECE]
    expected = (2 * 2118926400 * units[electron] + 4000 * 3612117122) // (2 * 4000 * 3612117122)
    assert piece_momentum(board, electron, passage) == [expected, 0, -expected] and expected > 0
    assert piece_momentum(board, neutron, Passage([2118926400, 0, 0], 0)) == [0, 0, 0]
    assert piece_momentum(board, neutron, Passage([2118926400, 0, 0], -7)) == [0, 0, 0]
    assert piece_momentum(board, proton, passage) == [0, 0, 0]  # the frozen pair, num 0
