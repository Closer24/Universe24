"""The piece's momentum of a record of a negative numerator (issue #2169, finding 3; the reader's ruling of 2026-10-21; ALGEBRA.md, The tension, the dated word, and the piece's line under The lattice momentum): `node_detector.piece_momentum` guarded on the signed wall num x W(region), so a negative numerator's passage read as nothing passed and the credit line carried the piece [0, 0, 0]; the guard is on the share alone and the division by the signed wall as the law writes it, the rounding half up on the magnitude with the sign of num after (kind D as before). Posed on the small torus with the universe file (tests/laws_universe.small_world) with a neutron row [-800, 1000] added to the universe, three real lines at the inverted band, by the arithmetic alone on a hand-written passage. The builder's chain, named (left on 2026-10-24, every world but Universe24 cancelled; its electron [4000, 6000] refused at load since that day, the sign's reader Pythagorean): the neutron [-4800, 6000] laid as a packet of three real lines at the weights (7, 7, 5), the wave [-1, 4] along +x on the chain of 61 toward a region of its last four Nodes, the derived window 59, one credit line at the close 118 with the piece and the fan below 0 (the piece -43,250 along x by the arithmetic where the engine gave 0; -42,370 and -77,974 at the close 95 under the declared window to 2026-10-23)."""

from __future__ import annotations

import json
from pathlib import Path

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.node_detector import Passage, piece_momentum
from event_universe.world_files import load_world
from tests.laws import family
from tests.laws_universe import GAMMA, small_world

NEUTRON = {"name": "neutron", "pair": [-800, GAMMA], "reads": {"gravity": 1}, "dimension": 3}
PASSAGE = Passage(
    [2118926400, 0, -2118926400], 3612117122
)  # the chain's right region's sums at its close, the hand-written passage of 2026-10-21
FORMER_PIECE = -43250  # the piece of this passage by the arithmetic on the chain's integers (the neutron's count unit at [-4800, 6000], T 32,768), 2026-10-21


def test_the_guard_is_on_the_share_alone_and_the_sign_is_nums(tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """`piece_momentum` by its arithmetic on the small torus with the universe file and the neutron row: the electron's piece, a positive numerator's, the division by num x W rounded half up on the magnitude with the sign after; the neutron's, a negative numerator's, the same magnitude with the sign flipped (the two pairs' sines equal, 0.6, so one count unit, and the piece one count's P_a pointing against the motion); a share at 0 or below nothing passed; and the frozen pair num = 0, the proton's, nothing passed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = small_world(tmp_path, detector=False)
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    universe["families"].append(NEUTRON)
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    board = Lattice(load_world(path))
    neutron, electron, proton = (family(board, n) for n in ("neutron", "electron", "proton"))
    assert board.families[neutron].pair == (-800, GAMMA) and board.families[electron].pair == (
        800,
        GAMMA,
    )
    units = board.credit.units
    assert units[neutron] == units[electron] == 3 * GAMMA * board.world.quantum_action * 600 // GAMMA
    expected = (2 * PASSAGE.momenta[0] * units[electron] + 800 * PASSAGE.share) // (
        2 * 800 * PASSAGE.share
    )
    assert expected > 0 and piece_momentum(board, electron, PASSAGE) == [expected, 0, -expected]
    assert piece_momentum(board, neutron, PASSAGE) == [-expected, 0, expected]  # the sign num's
    assert piece_momentum(board, neutron, Passage([PASSAGE.momenta[0], 0, 0], 0)) == [0, 0, 0]
    assert piece_momentum(board, neutron, Passage([PASSAGE.momenta[0], 0, 0], -7)) == [0, 0, 0]
    assert piece_momentum(board, proton, PASSAGE) == [0, 0, 0]  # the frozen pair, num 0
    assert FORMER_PIECE < 0  # the former course's sign the same
    print(
        f"the piece on the small torus {piece_momentum(board, neutron, PASSAGE)} (the chain's {FORMER_PIECE})"
    )
