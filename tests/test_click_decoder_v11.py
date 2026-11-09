"""Unit tests of click decoder v1.1 and its layers on synthetic logs with exactly known answers.

    python -m unittest tests.test_click_decoder_v11 -v
"""
from __future__ import annotations

import json
from pathlib import Path
import unittest

from research.click_decoder_v1 import decoder_v11 as D
from research.click_decoder_v1 import layers

ROOT = Path(__file__).resolve().parents[1]
CFG = D.load_config()


class Table(unittest.TestCase):
    def test_c_image_table_is_z_times_g(self):
        """The fixed 48-entry table in the config is left multiplication by the central z = 14 of 2O."""
        from universe24.core.group_2o import group      # the only import of universe24 in the decoder package
        m = group().multiplication
        self.assertEqual(CFG["c_image_table"], [m[CFG["c_image_z"]][g] for g in range(48)])
        self.assertTrue(all(CFG["c_image_table"][CFG["c_image_table"][g]] == g for g in range(48)))


def clock(period=5, steps=40, at=(10, 10, 10)):
    return [(t, *at, g, 1 + (g % 2), 1) for t in range(1, steps + 1) for g in (0, 7) if (t - 1) % period in (0, 2)]


class Decoder(unittest.TestCase):
    def test_longest_explaining_period(self):
        """(a) A site identical on 4 consecutive updates of a 6-cycle has period 6, not 1."""
        ev = [(t, 3, 3, 3, 0, 1, 1 if (t - 1) % 6 < 4 else 2) for t in range(1, 37)]
        rep = D.decode(ev, side=12, horizon=36)
        self.assertEqual([s["period"] for s in rep["sources"]], [6])

    def test_c_image_ring(self):
        """(i) Site pattern repeats after a lap of 6 with channels relabelled by C, so the period is 12."""
        tab = CFG["c_image_table"]
        ev = []
        for t in range(1, 61):
            lap = (t - 1) // 6
            g = 5 if lap % 2 == 0 else tab[5]
            ev.append((t, 4 + (t - 1) % 6, 4, 4, g, 1, 1))
        rep = D.decode(sorted(ev), side=16, horizon=60)
        s = rep["sources"][0]
        self.assertEqual((s["period"], s["period_channels_ignored"]), (12, 6))
        self.assertEqual((s["c_image"]["lap"], s["c_image"]["z"]), (6, 14))
        self.assertGreaterEqual(s["c_image"]["laps_verified"], 3)

    def test_relabel_that_is_not_c(self):
        """A relabelling g -> g + 1 is not the C image: no c_image block."""
        ev = [(t, 4 + (t - 1) % 6, 4, 4, 5 if ((t - 1) // 6) % 2 == 0 else 6, 1, 1) for t in range(1, 61)]
        s = D.decode(ev, side=16, horizon=60)["sources"][0]
        self.assertIsNone(s["c_image"])

    def test_sheet_comover(self):
        """(e) A board-wide plane (all y, z) moving +x one site every 2 updates: exact velocity 1/2."""
        L = 8
        ev = sorted((t, (t // 2) % L, y, z, g, 2, -1) for t in range(1, 25) for y in range(L) for z in range(L)
                    for g in (0, 1))
        tr = [t for t in D.decode(ev, side=L, horizon=24)["tracks"] if t["motion"]["exact"]]
        self.assertTrue(tr)
        self.assertEqual(tr[0]["motion"]["velocity"], ["1/2", "0", "0"])

    def test_velocity_change_split(self):
        """(g) One linked track: speed 1 for 12 updates, then speed 1/3 for 24: two tracks, the second born
        from the first."""
        ev, x = [], 5
        for t in range(1, 13):
            ev.append((t, x, 9, 9, 0, 1, 1))
            x += 1
        for t in range(13, 37):
            if t % 3 == 0:
                x += 1
            ev.append((t, x, 9, 9, 0, 2, -1))
        rep = D.decode(ev, side=80, horizon=36)
        speeds = sorted(t["motion"]["l1_speed"] for t in rep["tracks"] if t["class"] in ("light", "matter"))
        self.assertIn("1", speeds)
        self.assertTrue(any(abs(float(eval(s)) - 1 / 3) < 0.05 for s in speeds))

    def test_c_light_class(self):
        ev = [(t, 2 + int(t * 0.57735 // 1), 5, 5, 0, 1, 1) for t in range(1, 60)]
        rep = D.decode(ev, side=80, horizon=59, c=0.57735)
        self.assertEqual([t["class"] for t in rep["tracks"]], ["c-light"])

    def test_report_has_no_path(self):
        rep = D.decode(clock(), side=21, horizon=40, log_info={"path": "/a/b/log.jsonl", "sha256": "x", "events": 1})
        self.assertEqual(rep["input"]["log"]["name"], "log.jsonl")
        self.assertNotIn("path", rep["input"]["log"])

    def test_empty_summary_schema(self):
        a = set(D.decode([], side=9, horizon=4)["summary"])
        b = set(D.decode(clock(), side=21, horizon=40)["summary"])
        self.assertTrue({"tracks", "created", "explained_fraction", "c_light", "wrap_bound"} <= a & b)

    def test_deterministic(self):
        ev = sorted(clock(period=5, steps=40, at=(5, 5, 5)) + [(t, (t + 3) % 40, 20, 20, 1, 1, 1) for t in range(1, 41)])
        self.assertEqual(json.dumps(D.decode(ev, side=40, horizon=40), sort_keys=True),
                         json.dumps(D.decode(list(ev), side=40, horizon=40), sort_keys=True))


class Layers(unittest.TestCase):
    def test_peak_arrival_rule(self):
        """r14's rule: largest local maximum of sum |q| over [t-8, t+8] with t + 8 <= last step."""
        ev = [(t, 1, 0, 0, g, 1, q) for t, g, q in ((3, 2, 5), (3, 1, -5), (5, 0, 9), (20, 0, 9), (30, 4, 1))]
        recs = layers.peak_arrival(sorted(ev))
        self.assertEqual([(r["step"], r["address"], r["weight"]) for r in recs], [(3, [1, 0, 0, 1], 10)])

    def test_quotient_field_matches_r24_definition(self):
        ev = [(1, 2, 2, 2, 0, 1, 3), (2, 2, 2, 2, 5, 2, -1), (2, 3, 2, 2, 0, 1, 2)]
        f = layers.quotient_field(ev, side=5, centre=(2, 2, 2))
        self.assertEqual(f["sum"], {"2,2,2": 2, "3,2,2": 2})
        self.assertAlmostEqual(f["profile_Qbar"]["0"], 2 / 96)
        self.assertAlmostEqual(f["profile_Qbar"]["1"], (2 / 96) / 18)   # shell 1: 6 + 12 sites (radius 1, sqrt 2)


if __name__ == "__main__":
    unittest.main()
