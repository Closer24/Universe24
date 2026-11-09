"""Unit tests of the click decoder v1.0 on synthetic logs with exactly known answers, plus one official CLI log.

    python -m unittest tests.test_click_decoder_v1 -v
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from research.click_decoder_v1 import chsh, correlations, decode, read_log

ROOT = Path(__file__).resolve().parents[1]


def _write(path, events, extra=True):
    with open(path, "w", encoding="utf-8") as fh:
        for t, x, y, z, g, k, q in events:
            rec = {"step": t, "address": [x, y, z, g], "kind": k, "quotient": q}
            if extra:
                rec.update(before=[1, 2, 3], after=[4, 5, 6])
            fh.write(json.dumps(rec) + "\n")


def clock(period=5, steps=40, at=(10, 10, 10)):
    """One site clicking at phases 0 and 2 of every period, two channels."""
    return [(t, *at, g, 1 + (g % 2), 1) for t in range(1, steps + 1) for g in (0, 7) if (t - 1) % period in (0, 2)]


def glider(steps=36, start=5, every=3, side=24):
    """Two clicked sites, two apart, moving +x by one site every `every` updates; silent every third update."""
    out = []
    for t in range(1, steps + 1):
        if t % 3 == 1:
            continue
        x = start + (t - 1) // every
        out += [(t, x % side, 6, 6, 0, 1, 1), (t, (x + 2) % side, 6, 6, 0, 2, -1)]
    return out


def ray(steps=20, x0=3, side=40):
    return [(t, (x0 + t) % side, 20, 20, 5, 2, -1) for t in range(1, steps + 1)]


class Decoder(unittest.TestCase):
    def test_state_fields_dropped(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "log.jsonl"
            _write(p, clock())
            ev, info = read_log(p)
        self.assertEqual(info["fields_ignored"], ["after", "before"])
        self.assertTrue(all(len(e) == 7 for e in ev))

    def test_empty_log_is_dark(self):
        rep = decode([], side=9, horizon=12)
        self.assertEqual((rep["sources"], rep["tracks"]), ([], []))
        self.assertIn("dark", rep["summary"]["note"])

    def test_clock_period(self):
        rep = decode(clock(period=5), side=21, horizon=40)
        self.assertEqual([s["period"] for s in rep["sources"]], [5])
        s = rep["sources"][0]
        self.assertEqual((s["clicks_per_period"], s["phases"], s["composite"]), (4, [0, 2], False))
        self.assertEqual(rep["summary"]["explained_fraction"], 1.0)

    def test_glider_exact_one_third(self):
        rep = decode(glider(), side=24, horizon=36)
        movers = [t for t in rep["tracks"] if t["class"] == "matter"]
        self.assertEqual(len(movers), 1)
        self.assertEqual(movers[0]["motion"]["velocity"], ["1/3", "0", "0"])
        self.assertTrue(movers[0]["motion"]["exact"])

    def test_ray_is_light(self):
        rep = decode(ray(), side=40, horizon=20)
        self.assertEqual([(t["class"], t["motion"]["l1_speed"]) for t in rep["tracks"]], [("light", "1")])

    def test_two_far_objects_and_creation(self):
        late = [(t + 20, x, y, z, g, k, q) for t, x, y, z, g, k, q in ray(steps=10, x0=30, side=60)]
        rep = decode(sorted(clock(period=5, steps=40, at=(5, 5, 5)) + late), side=60, horizon=40)
        self.assertEqual([s["period"] for s in rep["sources"]], [5])
        tr = [t for t in rep["tracks"] if t["class"] == "light"]
        self.assertEqual(len(tr), 1)
        self.assertEqual((tr[0]["birth"]["origin"], tr[0]["birth"]["created"]), ("isolated", True))

    def test_channel_relabelled_ring(self):
        """Site pattern repeats after 6 updates, channels only after 12 (a 360/720-degree signature)."""
        ev = []
        for t in range(1, 49):
            g = 0 if (t - 1) % 12 < 6 else 14
            ev.append((t, 4 + (t - 1) % 6, 4, 4, g, 1, 1))
        rep = decode(ev, side=16, horizon=48)
        s = rep["sources"][0]
        self.assertEqual((s["period"], s["period_channels_ignored"], s["channel_period_ratio"]), (12, 6, 2))

    def test_deterministic(self):
        ev = sorted(clock(period=4, steps=40, at=(5, 5, 5)) + glider(side=40))
        a = json.dumps(decode(ev, side=40, horizon=40), sort_keys=True)
        b = json.dumps(decode(list(ev), side=40, horizon=40), sort_keys=True)
        self.assertEqual(a, b)


class Correlations(unittest.TestCase):
    def test_joint_counts(self):
        ev = [(t, 1, 1, 1, 0, 1, 1) for t in (1, 2, 3, 4)] + [(t, 8, 8, 8, 0, 2, 1) for t in (3, 4, 5)]
        spec = {"detectors": {"A": {"box": [[0, 2], [0, 2], [0, 2]]}, "B": {"sites": [[8, 8, 8]]}},
                "pairs": [["A", "B"]], "max_lag": 1}
        out = correlations(sorted(ev), spec, horizon=10, side=10)
        p = out["pairs"][0]
        self.assertEqual((p["n11"], p["n10"], p["n01"], p["n00"]), (2, 2, 1, 5))
        self.assertAlmostEqual(p["E"], (2 + 5 - 2 - 1) / 10)
        self.assertEqual(p["coincidences_by_lag"], {"-1": 1, "0": 2, "1": 3})

    def test_sides_and_chsh(self):
        ev = [(1, 0, 0, 0, 0, 1, 1), (1, 5, 0, 0, 0, 1, 1), (2, 1, 0, 0, 0, 1, 1), (2, 5, 0, 0, 0, 1, 1)]
        spec = {"detectors": {"A+": {"sites": [[0, 0, 0]]}, "A-": {"sites": [[1, 0, 0]]},
                              "B+": {"sites": [[5, 0, 0]]}, "B-": {"sites": [[6, 0, 0]]}},
                "sides": {"a": ["A+", "A-"], "b": ["B+", "B-"]}}
        s = correlations(ev, spec, horizon=2, side=10)["sides"]
        self.assertEqual((s["trials"], s["same"], s["different"], s["E"]), (2, 1, 1, 0.0))
        self.assertEqual(chsh(0.5, -0.5, 0.5, 0.5), 2.0)


class OfficialLog(unittest.TestCase):
    def test_impulse_cli_log(self):
        """examples/impulse.json: a period-6 localized orbit; decoded from the official --events log."""
        with tempfile.TemporaryDirectory() as d:
            log = Path(d) / "impulse.jsonl"
            subprocess.run([sys.executable, "-m", "universe24", "--config", str(ROOT / "examples/impulse.json"),
                            "--steps", "30", "--events", str(log)], check=True, capture_output=True, cwd=ROOT)
            out = subprocess.run([sys.executable, "-m", "research.click_decoder_v1", "decode", str(log), "--side",
                                  "9", "--horizon", "30", "--out", str(Path(d) / "rep.json")],
                                 check=True, capture_output=True, text=True, cwd=ROOT)
            rep = json.loads((Path(d) / "rep.json").read_text())
        self.assertEqual([s["period"] for s in rep["sources"]], [6])
        self.assertIn('"S0"', out.stdout)

    def test_diff_layer(self):
        with tempfile.TemporaryDirectory() as d:
            a, b, o = Path(d) / "a.jsonl", Path(d) / "b.jsonl", Path(d) / "o.jsonl"
            _write(a, clock(steps=10), extra=False)
            _write(b, clock(steps=5), extra=False)
            subprocess.run([sys.executable, "-m", "research.click_decoder_v1", "diff", str(a), str(b), "--out", str(o)],
                           check=True, capture_output=True, cwd=ROOT)
            ev, _ = read_log(o)
        self.assertEqual(sorted({e[0] for e in ev}), [6, 8])


if __name__ == "__main__":
    unittest.main()
