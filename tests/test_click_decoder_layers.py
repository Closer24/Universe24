"""Unit tests of the click decoder's frozen read-only layers log_symmetry_v1 and beat_clock_v1 (synthetic logs).

    python -m unittest tests.test_click_decoder_layers -v

The log_symmetry_v1 cases are the synthetic part of validation/PREREGISTRATION_log_symmetry_v1.md; the beat_clock_v1
cases are r25's synthetic tests of the observer (validation/PREREGISTRATION_beat_clock_v1.md, case B4), run on the
released copy. Each layer file must match the SHA-256 pinned in its FROZEN file.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import random
import tempfile
import unittest

from research.click_decoder_v1 import beat_clock_v1 as B
from research.click_decoder_v1 import log_symmetry_v1 as S

PKG = Path(S.__file__).resolve().parent
C = 1 / math.sqrt(3)


def frozen(name):
    return json.loads((PKG / f"FROZEN_{name}.json").read_text(encoding="utf-8"))


class Frozen(unittest.TestCase):
    def test_layer_files_match_their_freeze(self):
        for name in ("log_symmetry_v1", "beat_clock_v1"):
            fz = frozen(name)
            self.assertEqual(hashlib.sha256((PKG / fz["file"]).read_bytes()).hexdigest(), fz["sha256"], name)

    def test_beat_clock_is_the_pinned_observer(self):
        """beat_clock_v1.py is byte-identical to r25's observer, whose hash experiment E11 pins."""
        self.assertEqual(frozen("beat_clock_v1")["sha256"],
                         "05d9d49565c148468c59aea4d575ea03220784d0cc4e76bc2d6480298294699b")


# ------------------------------------------------------------------ log_symmetry_v1
def random_records(rnd, n, t_lo, t_hi):
    out = set()
    while len(out) < n:
        out.add((rnd.randrange(t_lo, t_hi + 1), rnd.randrange(6), rnd.randrange(6), rnd.randrange(6), rnd.randrange(48),
                 rnd.randrange(3), rnd.choice((-2, -1, 1, 2))))
    return sorted(out)


def write_log(path, recs, extra=False):
    with open(path, "w", encoding="utf-8") as fh:
        for t, x, y, z, g, k, q in recs:
            r = {"step": t, "address": [x, y, z, g], "kind": k, "quotient": q}
            if extra:
                r.update(before=[0, 0, 4], after=[0, 1, 0])
            fh.write(json.dumps(r, separators=(",", ":")) + "\n")


class Mirror(unittest.TestCase):
    def test_mirror_integer_and_half_integer_tau(self):
        rnd = random.Random(3)
        for tau in (20, 10.5):
            half = random_records(rnd, 80, 1, int(tau))
            recs = sorted(set(half) | {S.partner(r, tau) for r in half})
            m = S.mirror(recs, tau)
            self.assertEqual(m["unpaired"], 0)
            self.assertEqual(m["steps_mirrored_n"], 2 * tau)
            b = S.best_tau(recs)
            self.assertEqual((b["tau"], b["unique"], b["unpaired"]), (tau, True, 0))
            r = recs[5]
            bad = [x for x in recs if x != r] + [r[:6] + (-r[6],)]
            self.assertEqual(S.mirror(bad, tau)["unpaired"], 2)

    def test_partner_map_and_bad_tau(self):
        self.assertEqual(S.partner((3, 1, 2, 3, 14, 1, 2), 240), (478, 1, 2, 3, 14, 2, -2))
        with self.assertRaises(ValueError):
            S.partner((3, 1, 2, 3, 14, 1, 2), 240.25)

    def test_empty(self):
        self.assertEqual(S.mirror([], 5)["unpaired"], 0)
        self.assertIsNone(S.best_tau([])["tau"])
        self.assertFalse(S.period([], 5, horizon=20)["identical"] is None)


class Period(unittest.TestCase):
    def test_cycles_moved_record_and_full_records(self):
        rnd = random.Random(5)
        seg = random_records(rnd, 30, 1, 12)
        recs = sorted((t + 12 * j, *r) for j in range(4) for t, *r in seg)
        p = S.period(recs, 12, horizon=48)
        self.assertEqual((p["cycles"], p["identical"], p["records_per_cycle"]), (4, True, [30] * 4))
        moved = list(recs)
        i = next(i for i, r in enumerate(moved) if 26 <= r[0] <= 35)
        moved[i] = (moved[i][0] + 1, *moved[i][1:])
        q = S.period(moved, 12, horizon=48)
        self.assertEqual((q["identical"], q["first_differing_cycle"]), (False, 2))
        self.assertEqual(q["differences"], [{"cycle": 2, "only_cycle_0": 1, "only_this_cycle": 1}])
        with tempfile.TemporaryDirectory() as d:
            log = Path(d) / "log.jsonl"
            write_log(log, recs, extra=True)
            f = S.period(log, 12, horizon=48, full_records=True, write_prefix=str(Path(d) / "out"))
            self.assertTrue(f["identical"])
            one = (Path(d) / "out_cycle1.jsonl").read_text()
            self.assertEqual(one, (Path(d) / "out_cycle4.jsonl").read_text())
            self.assertEqual(len(one.splitlines()), 30)
            self.assertIn('"step":', one.splitlines()[0])

    def test_split_shift_diff(self):
        a = [(1, 0, 0, 0, 3, 1, 1), (5, 0, 0, 1, 3, 2, -1)]
        b = [(1, 0, 0, 0, 3, 1, 1), (5, 0, 0, 1, 3, 1, -1)]
        self.assertEqual(S.record_diff(a, b)["differ"], 2)
        self.assertEqual(S.split(a, 3), ([(1, 0, 0, 0, 3, 1, 1)], [(2, 0, 0, 1, 3, 2, -1)]))
        self.assertEqual(S.shift(a, 5, lo=2), [(10, 0, 0, 1, 3, 2, -1)])


class Image(unittest.TestCase):
    def ring(self, T=6, laps=6, kind="C"):
        recs = []
        for t in range(1, T * laps + 1):
            n = (t - 1) // T
            g, k, q = 5, 1, 1
            if n % 2:
                g = S.Z_TABLE[g]
                if kind == "K":
                    k, q = 2, -1
            recs.append((t, 4 + (t - 1) % T, 4, 4, g, k, q))
        return recs

    def test_c_and_k_rings_and_plain_repeat(self):
        c = S.c_image(self.ring(kind="C"), 6)
        self.assertEqual((c["image_steps_n"], c["plain_repeat_steps"], c["unmatched_records"]), (30, 0, 0))
        k = S.c_image(self.ring(kind="K"), 6, kind="K")
        self.assertEqual((k["image_steps_n"], k["plain_repeat_steps"]), (30, 0))
        self.assertEqual(S.c_image(self.ring(kind="K"), 6, kind="C")["image_steps_n"], 0)
        plain = [(t, 4 + (t - 1) % 6, 4, 4, 5, 1, 1) for t in range(1, 37)]
        p = S.c_image(plain, 6)
        self.assertEqual((p["image_steps_n"], p["plain_repeat_steps"]), (0, 30))
        boxed = S.c_image(self.ring(kind="C"), 6, region=((4, 5), (4, 4), (4, 4)))
        self.assertEqual(boxed["records_in_region"], 12)

    def test_z_table_is_z_times_g(self):
        from universe24.core.group_2o import group
        m = group().multiplication
        self.assertEqual(list(S.Z_TABLE), [m[14][g] for g in range(48)])


class Reading(unittest.TestCase):
    def test_records_read_only_the_four_fields(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "log.jsonl"
            write_log(p, [(4, 1, 2, 3, 9, 2, -1)], extra=True)
            self.assertEqual(S.records(p), [(4, 1, 2, 3, 9, 2, -1)])


# ------------------------------------------------------------------ beat_clock_v1 (r25's synthetic tests)
def line_events(L, steps, waves, amp=10 ** 6):
    """Synthetic records on the line (0,0,z), channel 0: q = sum A cos(k z - w t) (rounded, zeros dropped)."""
    ev = []
    for t in range(1, steps + 1):
        for z in range(L):
            q = round(sum(amp * math.cos(k * z - w * t) for k, w in waves))
            if q:
                ev.append((t, 0, 0, z, 0, 0, q))
    return ev


def clock(K1, K2, c=C):
    return {"name": "t", "K1": [0, 0, K1], "K2": [0, 0, K2], "axis": [0, 0, 1], "c": c}


class BeatClock(unittest.TestCase):
    L, steps = 64, 200
    sites = [(0, 0, z) for z in range(64)]

    def test_relativistic_pair_gives_ratio_one(self):
        m, kap = 0.07, 2 * math.pi / self.L
        k1, k2 = 2 * kap, 3 * kap
        w1, w2 = (math.sqrt(m * m + C * C * k * k) for k in (k1, k2))
        out = B.beat_clock(line_events(self.L, self.steps, [(k1, w1), (k2, w2)]), self.L, self.steps, 0,
                           clock(k1, k2), self.sites)
        self.assertAlmostEqual(out["ratio"], 1.0, places=6)
        self.assertAlmostEqual(out["u"], (w2 - w1) / (k2 - k1), places=7)
        self.assertEqual(out["projection"], ["rotating", "rotating"])

    def test_standing_wave_is_a_rest_clock(self):
        kap = 2 * math.pi / self.L
        w = 0.05
        out = B.beat_clock(line_events(self.L, self.steps, [(kap, w), (-kap, w)]), self.L, self.steps, 0,
                           clock(-kap, kap), self.sites)
        self.assertEqual(out["projection"], ["standing", "standing"])
        self.assertAlmostEqual(out["u"], 0.0, places=9)
        self.assertAlmostEqual(out["Omega"], w, places=6)

    def test_nonrelativistic_dispersion_is_detected(self):
        m, kap = 0.07, 2 * math.pi / self.L
        k1, k2 = 2 * kap, 3 * kap
        w1, w2 = (m + k * k / (2 * m) * C * C for k in (k1, k2))
        out = B.beat_clock(line_events(self.L, self.steps, [(k1, w1), (k2, w2)]), self.L, self.steps, 0,
                           clock(k1, k2), self.sites)
        self.assertGreater(abs(out.get("ratio", 0) - 1), 1e-3)

    def test_empty_log_is_no_clock(self):
        out = B.beat_clock([], self.L, 10, 0, clock(0.1, 0.2), self.sites)
        self.assertIn("no clock", out["verdict"])

    def test_dict_and_tuple_records_agree(self):
        kap = 2 * math.pi / self.L
        ev = line_events(self.L, 50, [(kap, 0.06), (2 * kap, 0.09)])
        dicts = [{"step": e[0], "address": list(e[1:5]), "kind": e[5], "quotient": e[6]} for e in ev]
        a = B.beat_clock(ev, self.L, 50, 0, clock(kap, 2 * kap), self.sites)
        b = B.beat_clock(dicts, self.L, 50, 0, clock(kap, 2 * kap), self.sites)
        self.assertEqual(a["omega"], b["omega"])


if __name__ == "__main__":
    unittest.main()
