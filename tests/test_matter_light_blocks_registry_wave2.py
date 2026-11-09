"""Registry WAVE 2 (r21): generic guide generator, gauge transport, includes, one-tensor rule.

Tracked code only (research.matter_light_blocks_v1.registry, universe24, research.components).
"""
import json
import unittest

from research.matter_light_blocks_v1 import verify as V
from research.matter_light_blocks_v1.registry import BLOCKS, compose, compositions as CP, symmetry as SY
from research.matter_light_blocks_v1.registry.compose import expand


class PublishedGuides(unittest.TestCase):
    def test_published_guide_blocks_regenerate_exactly(self):
        for name, spec in CP.published_guide_specs().items():
            with self.subTest(block=name):
                prepared, _ = compose(spec)
                engine, initial, _, _ = V.load(name)
                self.assertEqual(prepared.initial, initial)
                self.assertEqual(prepared.engine.coupling.fingerprint, engine.coupling.fingerprint)


class Gauge(unittest.TestCase):
    def test_gauge_transport_is_exact_natively(self):
        """+++ fibre packet moved to (-,+,+) as data: S'(t) == G(S(t)) at every update (exact inverse checked)."""
        spec = CP.published_guide_specs()["fiber_x_packet"]
        ref, _ = compose(spec)
        moved = json.loads(json.dumps(spec))
        moved["board"]["coupling"]["signs"] = [-1, 1, 1]
        for p in moved["placements"]:
            p["native_signs"], p["gauge"] = [1, 1, 1], {"character": True, "staggered": True}
        gau, _ = compose(moved)
        self.assertEqual(gau.initial, SY.gauge_state(ref.initial, True, True))
        s, g = ref.initial, gau.initial
        for _ in range(12):
            s2, g2 = ref.engine.advance(s), gau.engine.advance(g)
            self.assertEqual(ref.engine.rewind(s2), s)
            self.assertEqual(gau.engine.rewind(g2), g)
            self.assertEqual(g2, SY.gauge_state(s2, True, True))
            s, g = s2, g2

    def test_one_tensor_per_board_and_gauge_classes(self):
        spec = CP.published_guide_specs()["fiber_x_packet"]
        bad = json.loads(json.dumps(spec))
        bad["board"]["coupling"]["signs"] = [-1, 1, 1]
        for p in bad["placements"]:
            p["native_signs"] = [1, 1, 1]
        with self.assertRaises(ValueError):           # no gauge given: one tensor per board
            compose(bad)
        for p in bad["placements"]:
            p["gauge"] = "auto"
        compose(bad)                                  # +++ -> -++ inside class B
        bad["board"]["coupling"]["signs"] = [1, -1, 1]
        with self.assertRaises(ValueError):           # class B -> class F is not a gauge
            compose(bad)
        self.assertEqual(SY.gauge_for((1, 1, 1), (-1, 1, 1)), (True, True))
        self.assertIsNone(SY.gauge_for((1, 1, 1), (1, 1, -1)))


class Includes(unittest.TestCase):
    def test_gauged_include_equals_gauge_image(self):
        w9 = CP.w9_two_detector_spec(41, side=160, zc=0, x0=1, x1=158)
        host = {"format": CP.FORMAT, "id": "host", "board": {"side": 160, "background": [0, 0, 2],
                                                             "coupling": {"signs": [-1, 1, 1], "variant": None}},
                "placements": [{"name": "w9", "include": w9, "at": [0, 0, 80],
                                "gauge": {"character": True, "staggered": True}}]}
        flat = json.loads(json.dumps(w9))
        for p in flat["placements"]:
            p["at"] = [p["at"][0], p["at"][1], p["at"][2] + 80]
        ref, _ = compose(flat)
        prepared, report = compose(host)
        self.assertTrue(report["beside_fibre_ok"])
        self.assertEqual(prepared.initial, SY.gauge_state(ref.initial, True, True))
        self.assertEqual(len(expand(host)["placements"]), 4)


class Preconditions(unittest.TestCase):
    def test_new_generators_check_their_preconditions(self):
        board = {"side": 64, "signs": (1, 1, 1), "background": (0, 0, 2)}
        with self.assertRaises(ValueError):
            BLOCKS["phase_gate@2"](board, phase=0, offset=(0, 1, 0))
        with self.assertRaises(ValueError):
            BLOCKS["pulse_train@1"](board, length=40, node=30, first=10, period=3, count=3)
        with self.assertRaises(ValueError):
            BLOCKS["all48_site@1"](board, triple=(-1, -1, 0), phase=0)
        with self.assertRaises(ValueError):
            BLOCKS["pulse_train@1"](board, length=40, g0=2)          # label 2 is not straight along x
        # phases 0/2 need no halo (S_HIST = 0); phases 1/3 carry the history halo on all 6 x 48 port receivers
        self.assertEqual([len(BLOCKS["phase_gate@2"](board, phase=ph).cells) for ph in range(4)], [48, 336, 48, 336])


if __name__ == "__main__":
    unittest.main()
