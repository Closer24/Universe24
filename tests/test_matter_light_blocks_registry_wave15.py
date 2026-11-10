"""WAVE 15 registry additions (r67): builder F's prescribed Schwarzschild-lapse ladder (clock.lapse_ring_ladder@1, g00 only)
and the SHAPIRO-RADIAL chain, read by a clicks-only observer given a declaration (exp.lapse_ladder@1)."""
from __future__ import annotations

import hashlib
import json
import unittest

from research.matter_light_blocks_v1.registry import compositions as CP
from research.matter_light_blocks_v1.registry import guides as G
from research.matter_light_blocks_v1.registry.compose import apply_control, compose, init_data

# builder F's ladder init file (remote/builderF_FINAL/swl/config_L400.json, archived at c2b4258), harness form, T = 700
LADDER_INIT = "322e508cdbfdb209"


class Wave15Registry(unittest.TestCase):
    def test_ladder_is_builder_fs_init_file(self):
        prepared, _ = compose(CP.lapse_ladder_spec(400))
        data = init_data(prepared, 700)
        self.assertTrue(hashlib.sha256((json.dumps(data, indent=1) + "\n").encode()).hexdigest().startswith(LADDER_INIT))
        self.assertEqual(CP.lapse_ladder_spec(800)["placements"], CP.lapse_ladder_spec(400)["placements"])

    def test_node_counts_are_120_over_N(self):
        p = CP.ladder_params()
        rings = {q["name"]: len(G.expand_dirs(q["dirs"])) + 1 for q in p["paths"] if q["name"].startswith("ring_")}
        self.assertEqual(rings, {"ring_F": 120, "ring_S4": 144, "ring_S3": 150, "ring_S2": 160, "ring_S1": 180})
        self.assertEqual(sorted(p["closed"]), sorted(rings))
        self.assertEqual({q["lead"] for q in p["packets"]}, {10})
        taps = [q for q in p["paths"] if q["name"].startswith("tap_")]
        self.assertEqual({(q["at_node"], q["dir"], q["length"]) for q in taps}, {(0, 4, 370)})

    def test_shapiro_chains(self):
        spec = CP.shapiro_chain_spec(800)
        for ctl, n in (("curved", 200 + 89 + 98 + 115 + 1), ("flat", 200 + 177 + 1)):
            params = apply_control(spec, next(c for c in spec["controls"] if c["name"] == ctl))["placements"][0]["params"]
            self.assertEqual(sum(k for _, k in params["paths"][0]["dirs"]) + 1, n)
            self.assertEqual(params["packets"], [{"path": "line", "f": [1, 0, -1], "lead": 100}])


if __name__ == "__main__":
    unittest.main()
