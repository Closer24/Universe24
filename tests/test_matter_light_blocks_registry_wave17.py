"""WAVE 17 registry additions (r67): builder C's GS-2b, a relay tree of fibre light whose node counts were PRESCRIBED from
Schwarzschild's formulas (light.radial_relay_tree@1), read in clicks by a declared observer
(exp.schwarzschild_radial_profile@1)."""
from __future__ import annotations

import hashlib
import json
import unittest

from research.matter_light_blocks_v1.registry import compositions as CP
from research.matter_light_blocks_v1.registry import guides as G
from research.matter_light_blocks_v1.registry.compose import compose, init_data

# builder C's GS2b_S init file (preparations2b/GS2b_S.json; rebuild_grs.py EXPECTED), harness form, T = 4334
GS2B_S_INIT = "b162549ec9b46c4c"


class Wave17Registry(unittest.TestCase):
    def test_gs2b_s_is_builder_cs_init_file(self):
        spec = CP.gs2b_spec("GS2b_S")
        self.assertEqual((spec["board"]["side"], spec["steps"], len(spec["placements"])), (1024, 4334, 8))
        prepared, _ = compose(spec)
        blob = (json.dumps(init_data(prepared, spec["steps"]), indent=1) + "\n").encode()
        self.assertTrue(hashlib.sha256(blob).hexdigest().startswith(GS2B_S_INIT))

    def test_design_integers(self):
        d = CP.gs2b_design("S")
        self.assertEqual(d["clock_nodes"], [800, 684, 626, 592, 570, 554])
        self.assertEqual(d["J"], [20, 142, 250, 351, 448, 548])
        self.assertEqual(d["C"], [2094, 2258, 2545, 2895, 3284, 3723])
        self.assertEqual(CP.gs2b_horizon(), 4334)
        self.assertEqual([round(r, 2) for r in d["r"]], [200.0, 252.2, 310.64, 373.63, 440.08, 513.43])
        self.assertEqual(CP.gs2b_design("F")["clock_nodes"], [480] * 6)

    def test_rings_and_branches(self):
        for n, (a, b) in CP.GS2B["ring"].items():                       # closed rectangles of n nodes
            self.assertEqual(2 * (a + b), n)
        net = CP.gs2b_spec("GS2b_S")["placements"][0]["params"]
        d = CP.gs2b_design("S")
        for i, p in enumerate(net["paths"][1:]):                         # each branch runs past its port B_i
            self.assertEqual((p["branch_of"], p["at_node"]), ("spoke", d["J"][i]))
            self.assertGreater(len(G.expand_dirs(p["dirs"])), 3 + d["C"][i])
        self.assertEqual(net["packets"], [{"path": "spoke", "f": [1, 0, -1], "lead": 4}])


if __name__ == "__main__":
    unittest.main()
