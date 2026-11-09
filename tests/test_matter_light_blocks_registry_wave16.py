"""WAVE 16 registry additions (r67): r71's PRESCRIBED metric tensor in a DECLARED chart (light.radar_tensor_station@1):
a station of 26 staircase radar arms around a standard ring clock, the Manhattan control and the two-station time board,
read by a clicks-only observer given a declaration (exp.metric_tensor_declared_chart@1)."""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import unittest

from research.matter_light_blocks_v1.registry import compositions as CP
from research.matter_light_blocks_v1.registry import guides as G
from research.matter_light_blocks_v1.registry.compose import compose, init_data

# r71's time_v2 init file (runs/matter_light_v1/r71/time_v2.init.json; r71's time_board v2), harness form, T = 568
TIME_V2_INIT = "ec962966fa30faa4"


class Wave16Registry(unittest.TestCase):
    def test_time_board_is_r71s_init_file(self):
        spec = CP.tensor_time_spec()
        prepared, _ = compose(spec)
        data = init_data(prepared, spec["steps"])
        self.assertEqual((spec["board"]["side"], spec["steps"]), (674, 568))
        blob = (json.dumps(data, indent=1) + "\n").encode()
        self.assertTrue(hashlib.sha256(blob).hexdigest().startswith(TIME_V2_INIT))

    def test_design_lengths(self):
        lines = CP.TENSOR_LINES13
        aniso = [CP.tensor_length(CP.TENSOR_G_ANISO, n, 400) for n in lines]
        self.assertEqual(aniso, [400, 438, 379, 632, 551, 566, 537, 551, 607, 727, 748, 704, 632])
        self.assertEqual([CP.tensor_length("manhattan", n, 100) for n in lines],
                         [100, 110, 95, 210, 210, 195, 195, 205, 205, 305, 305, 305, 305])
        for n, d in zip(lines, aniso):                                  # half-up rounding of 400 sqrt(n^T g n)
            q = 400 ** 2 * sum(CP.TENSOR_G_ANISO[i][j] * n[i] * n[j] for i in range(3) for j in range(3))
            self.assertTrue((d - Fraction(1, 2)) ** 2 <= q < (d + Fraction(1, 2)) ** 2)
        self.assertEqual(CP.tensor_length(CP.TENSOR_G_ANISO, (1, 0, 0), 96, Fraction(2, 3)), 144)

    def test_arm_geometry(self):
        spec = CP.tensor_station_spec("aniso")
        self.assertEqual((spec["board"]["side"], spec["steps"], len(spec["placements"])), (966, 1526, 27))
        arms = CP.tensor_arms(CP.TENSOR_G_ANISO, 400)
        for a, p in zip(arms, spec["placements"][1:]):
            steps = G.expand_dirs(p["params"]["paths"][0]["dirs"])
            self.assertEqual(len(steps), CP.TENSOR["port"] + a["D"])                 # port + D nodes beyond node 0
            pos = tuple(p["params"]["paths"][0]["start"])
            for d in steps:
                nxt = G.add(pos, d)
                step = [u - v for u, v in zip(nxt, pos)]                         # monotone toward n
                self.assertTrue(all(w * c >= 0 and (c or not w) for w, c in zip(step, a["n"])))
                pos = nxt
        self.assertEqual(CP.tensor_station_spec("manhattan", "manhattan")["board"]["side"], 310)


if __name__ == "__main__":
    unittest.main()
