"""WAVE 8 registry additions (r21c): the generator plane_light@1, exact body-diagonal plane light (E14, E11's main
board, the published diag_sheet) (tracked data)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

import research.matter_light_blocks_v1 as PKG
from research.matter_light_blocks_v1.registry import compositions as CP
from research.matter_light_blocks_v1.registry.compose import FORMAT, apply_control, compose, init_data

# initial-state SHA-256 (the experiments verifier's rule) of r26b's E14 runs and r25's E11 main board, each
# regenerated exactly by plane_light@1 (r21c verify_w67, wave 8: 9/9 files and run hashes)
RECORDED = {
    "e14_J109": "f964c1a9a560f6abfd713f1d33c4cf07e2dcc035be3e6d90ea8514dee1394c67",
    "e14_A": "85c1cd1d352df3f15f21335ddea6d94250d987b92da5f5f8916be703fe535147",
    "e14_J180": "e1d0f44b659c3772ce6f3ddbc4542e49ef0c6c415916dd7c776e241552d2a152",
    "e11_main_L6": "27016cc96ccc237fa9d921c7c4f1c7ffcb5e606a8032f74d2bf1417f6468916b",
}
BLOCKS_DIR = Path(PKG.__file__).resolve().parent / "blocks"          # the published blocks of the package


def state_sha256(state):
    blob = json.dumps([state.cube.side, list(state.background),
                       sorted([list(k), list(v)] for k, v in state.cells.items())], separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def composed(spec, control=None):
    if control is not None:
        spec = apply_control(spec, next(c for c in spec["controls"] if c["name"] == control))
    prepared, rep = compose(spec)
    bad = [k for k, v in rep.items() if k.endswith("_ok") and not v]
    if bad:
        raise AssertionError(f"{spec['id']}: assertions failed {bad}")
    return prepared


class Wave8Registry(unittest.TestCase):
    def test_plane_light(self):
        spec = CP.e14_two_beam_spec()
        self.assertEqual([q["block"] for q in spec["placements"]], ["plane_light@1"])
        for run in ("J109", "A", "J180"):
            self.assertEqual(state_sha256(composed(spec, run).initial), RECORDED[f"e14_{run}"], run)
        st = composed(CP.e11_main_plane_light_spec()).initial
        self.assertEqual(state_sha256(st), RECORDED["e11_main_L6"])
        self.assertEqual(st, composed(CP.e11_main_diagonal_spec()).initial)
        # one beam (1,1,1) with a delta profile is the published diag_sheet block (state, coupling, init JSON)
        sheet = {"format": FORMAT, "id": "diag_sheet", "board": CP._board(12, CP.PPP),
                 "placements": [CP.plane_light_placement("sheet", [{"sigma": [1, 1, 1], "profile": [1] + [0] * 11}])]}
        data = json.loads((BLOCKS_DIR / "light" / "diag_sheet.json").read_text(encoding="utf-8"))
        self.assertEqual(init_data(composed(sheet), data["steps"]), data)
        board = CP._board(12, CP.PPP)
        for b, beam in ((board, {"sigma": [1, 0, 1], "profile": [1, 0]}),
                        (board, {"sigma": [1, 1, 1], "profile": [1, 0, 0, 0, 0]}),
                        (CP._board(12, CP.MPP), {"sigma": [1, 1, 1], "profile": [1, 0]})):
            with self.assertRaises(ValueError):
                compose({"format": FORMAT, "id": "bad", "board": b,
                         "placements": [CP.plane_light_placement("x", [beam])]})


if __name__ == "__main__":
    unittest.main()
