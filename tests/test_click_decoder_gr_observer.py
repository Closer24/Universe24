"""The released decoder layer gr_observer_v1 (r64's clicks-only GR observer, observer_gr.py 1.2 byte for byte): its
freeze record, its read-only contract, r64's synthetic tests (ported: the module path changed, nothing else), and one
official E09 log read through E21's declarations."""
from __future__ import annotations

import ast
import copy
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import tempfile
import unittest

from research.click_decoder_v1 import gr_observer_v1 as O

FILE = Path(O.__file__).resolve()
FROZEN = FILE.parent / "FROZEN_gr_observer_v1.json"


class Release(unittest.TestCase):
    def test_frozen_record_pins_this_file(self):
        record = json.loads(FROZEN.read_text(encoding="utf-8"))
        self.assertEqual((record["name"], record["file"]), ("gr_observer_v1", FILE.name))
        self.assertEqual(hashlib.sha256(FILE.read_bytes()).hexdigest(), record["sha256"])
        self.assertEqual(O.VERSION, "r64-observer-gr-1.2")

    def test_one_self_contained_read_only_file(self):
        src = FILE.read_text(encoding="utf-8")
        mods = set()
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, ast.Import):
                mods.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                mods.add((node.module or "").split(".")[0])
        self.assertLessEqual(mods, {"__future__", "argparse", "copy", "fractions", "hashlib", "json", "math",
                                    "pathlib", "typing"})
        self.assertNotIn("open(", src.replace("path.read_bytes()", ""))

    def test_run_declared_is_json_ready(self):
        recs = [{"step": t, "address": [1, 2, 3, 0], "kind": 1, "quotient": 1} for t in range(4, 41, 6)]
        decl = {"stations": {"c": {"sites": [[1, 2, 3]], "profile": "A", "lap": 4, "role": "clock"}},
                "readouts": [{"type": "clock", "name": "c", "clock": "c"}]}
        out = O.run_declared(O.ClickLog(recs, horizon=40), decl)
        self.assertEqual(json.loads(json.dumps(out)), out)
        self.assertEqual((out["measurements"]["c"]["period"], out["measurements"]["c"]["rate"]), (6, "2/3"))


# ------------------------------------------------------------------------------- r64's synthetic tests (ported)
class Synthetic(unittest.TestCase):
    def rec(self, times, sig=(0, 0, 1, 1)):
        return {t: (sig,) for t in times}

    def test_exact_period_smallest_and_steady(self):
        r = self.rec([2] + list(range(10, 61, 5)))       # a transient click at 2, then period 5 from 10; horizon 60
        p = O.exact_period(r, 1, 60)
        self.assertEqual(p["period"], 5)
        self.assertGreaterEqual(p["periods_covered"], 3)

    def test_exact_period_needs_three_periods(self):
        self.assertIsNone(O.exact_period(self.rec([10, 40]), 1, 60, max_period=20))

    def test_passage_direction_on_a_three_node_line(self):
        recs = [{"step": t, "address": [x, 0, 0, 0], "kind": 1, "quotient": 1, "before": [0, 0, 0], "after": [0, 0, 0]}
                for x, t in ((19, 14), (20, 15), (21, 16), (21, 94), (20, 95), (19, 96))]
        log = O.ClickLog(recs, horizon=100)
        got = O.passages(log, {"sites": [[19, 0, 0], [20, 0, 0], [21, 0, 0]]})
        self.assertEqual(got, [{"t": 15, "direction": 1}, {"t": 95, "direction": -1}])
        self.assertEqual(log.fields_ignored, ["after", "before"])

    def test_radar_and_einstein_offset(self):
        recs = [{"step": t, "address": [x, 0, 0, 0], "kind": 1, "quotient": 1}
                for x, t in ((9, 4), (10, 5), (11, 6), (40, 36), (11, 66), (10, 67), (9, 68))]
        decl = {"measurements": [{"type": "radar", "name": "r", "station": {"port": {
            "sites": [[9, 0, 0], [10, 0, 0], [11, 0, 0]]}}, "mirror": {"port": {"sites": [[40, 0, 0]]}},
            "station_rate": {"value": "2/3"}}]}
        r = O.observe(O.ClickLog(recs, horizon=80), decl)["measurements"]["r"]
        self.assertEqual((r["t1"], r["t2"], r["t3"], r["round_trip"]), (5, 36, 67, 62))
        self.assertEqual(r["einstein_offset"], 0)
        self.assertEqual(r["radar_distance_proper"], F(2, 3) * 31)

    def test_alpha_exact_flags(self):
        self.assertEqual(O.alpha_exact(F(4, 9), F(2, 3)), "2")
        self.assertEqual(O.alpha_exact(F(2, 3), F(2, 3)), "1")
        self.assertIsNone(O.alpha_exact(F(1, 2), F(2, 3)))

    def test_profile_key_and_deprecated_species_alias(self):
        old = {"stations": {"d": {"sites": [[1, 2, 3]], "species": "A"}},
               "readouts": [{"type": "detector", "name": "a", "detector": "d", "window": [1, 5]}]}
        self.assertEqual(O.validate(old), [])
        recs = [{"step": 2, "address": [1, 2, 3, 0], "kind": 1, "quotient": 1}]
        self.assertEqual(O.observe(O.ClickLog(recs, horizon=5), old)["measurements"]["a"]["profile"], "A")
        clash = {**old, "stations": {"d": {"sites": [[1, 2, 3]], "species": "A", "profile": "B"}}}
        self.assertEqual(len(O.validate(clash)), 1)


class DeclarationFormat(unittest.TestCase):
    GOOD = {"format": "r64-observer-declaration-1", "name": "t",
            "stations": {"d1": {"sites": [[1, 2, 3]], "profile": "A", "role": "detector"},
                         "d2": {"sites": [[4, 5, 6]], "kinds": [1], "profile": "B", "role": "detector"}},
            "readouts": [{"type": "detector", "name": "a", "detector": "d1", "window": [1, 10]},
                         {"type": "outcome", "name": "o", "detectors": ["d1", "d2"], "window": [1, 10]}]}

    def test_valid_and_resolved(self):
        self.assertEqual(O.validate(self.GOOD), [])
        res = O.resolve(self.GOOD)["measurements"]
        self.assertEqual(res[0]["detector"]["sites"], [[1, 2, 3]])
        self.assertEqual(res[1]["detector_names"], ["d1", "d2"])
        self.assertEqual(O.station_sites(self.GOOD), {(1, 2, 3), (4, 5, 6)})

    def test_invalid_declarations_are_refused(self):
        bad = copy.deepcopy(self.GOOD)
        bad["readouts"][0]["type"] = "telepathy"
        bad["stations"]["d1"]["profile"] = "Z"
        bad["stations"]["d2"]["sites"] = [[1, 2]]
        bad["readouts"][1]["detectors"] = ["d1", "nowhere"]
        self.assertEqual(len(O.validate(bad)), 4)
        with self.assertRaises(ValueError):
            O.observe(O.ClickLog([], horizon=10), bad)

    def test_qm_style_detector_and_outcome_readouts(self):
        recs = [{"step": t, "address": [x, y, z, 0], "kind": k, "quotient": q}
                for t, (x, y, z), k, q in ((3, (1, 2, 3), 1, 1), (7, (1, 2, 3), 2, -1), (5, (4, 5, 6), 1, 1))]
        m = O.observe(O.ClickLog(recs, horizon=10), self.GOOD)["measurements"]
        self.assertEqual((m["a"]["clicks"], m["a"]["first"], m["a"]["signature"], m["a"]["profile"]),
                         (2, 3, [(1, 1), (2, -1)], "A"))
        self.assertEqual((m["o"]["fired"], m["o"]["first_to_fire"], m["o"]["exclusive"]), (["d1", "d2"], ["d1"], False))


class ReggeSynthetic(unittest.TestCase):
    """The curvature machinery on exactly known geometries (lengths given, no board)."""

    @staticmethod
    def grid(n, point, wrap=None):
        T, m = [], wrap or n
        for i in range(n):
            for j in range(m if wrap else n):
                a, b, c, d = (i, j), (i + 1, j), (i, (j + 1) % m if wrap else j + 1), \
                    (i + 1, (j + 1) % m if wrap else j + 1)
                T += [(a, b, d), (a, d, c)]
        L = {}
        for t in T:
            for u, v in itertools.combinations(t, 2):
                L[O._key(u, v)] = math.dist(point(*u), point(*v))
        return L, T

    def test_flat_lattice_has_zero_deficits(self):
        L, T = self.grid(4, lambda i, j: (i, j))
        self.assertEqual(max(abs(x) for x in O.deficits_2d(L, T).values()), 0.0)

    def test_flamm_paraboloid_deficit_is_minus_M_over_r3(self):
        M, n = 1.0, 48
        rs = [4 + i * 8.0 / n for i in range(n + 1)]
        pt = lambda i, j: (rs[i] * math.cos(math.pi * j / n), rs[i] * math.sin(math.pi * j / n),   # noqa: E731
                           2 * math.sqrt(2 * M * (rs[i] - 2 * M)))
        L, T = self.grid(n, pt, wrap=2 * n)
        D = O.deficits_2d(L, T)
        i, area = n // 2, 0.0
        for t in T:
            if (i, 0) in t:
                a, b, c = (L[O._key(t[x], t[y])] for x, y in ((1, 2), (2, 0), (0, 1)))
                s2 = (a + b + c) / 2
                area += math.sqrt(s2 * (s2 - a) * (s2 - b) * (s2 - c)) / 3
        self.assertAlmostEqual(D[(i, 0)] / (-M / rs[i] ** 3 * area), 1.0, delta=0.005)

    def test_shell_relations_on_exact_schwarzschild_numbers(self):
        M = 1.0
        rs = [6 + 0.05 * i for i in range(400)]
        ell, shells = 0.0, []
        f = lambda x: math.sqrt(x * (x - 2 * M)) + 2 * M * math.log(math.sqrt(x) + math.sqrt(x - 2 * M))  # noqa: E731
        for i, r in enumerate(rs):
            if i:
                ell += f(r) - f(rs[i - 1])                     # exact proper radial distance
            shells.append({"N": math.sqrt(1 - 2 * M / r), "C": 2 * math.pi * r, "ell": ell})
        rel = O.schwarzschild_relations(shells)
        self.assertTrue(all(abs(x["N_times_H_r"] - 1) < 1e-4 and abs(x["m"] - M) < 1e-3 for x in rel))
        K = O.shell_curvature(rs, [1 / math.sqrt(1 - 2 * M / r) for r in rs], rs)
        self.assertAlmostEqual(K[100] / (-M / rs[101] ** 3), 1.0, delta=1e-3)


# ------------------------------------------------------------------------------- one official E09 log, E21's stations
class OfficialE09Log(unittest.TestCase):
    def test_clock_in_the_flux_from_its_official_log(self):
        from research.matter_light_experiments_v1 import verify as X
        eid = "E21_gr_observer_clicks_only"
        man = X.manifest(eid)
        run = next(r for r in man["runs"] if r["name"] == "redshift_clock_in_flux")
        engine, initial, steps, _ = X.load_run(eid, man, run, X._composition(eid, man))
        det = json.loads((X.HERE / eid / "detectors.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "redshift_clock_in_flux.events.jsonl"
            got = X.replay(engine, initial, steps, log)
            self.assertEqual(got["log_sha256"], run["log_sha256"])                  # the official log
            out = O.run_declared(str(log), det["observer"]["E09"]["redshift"])
        m = out["measurements"]
        self.assertEqual((m["clock"]["period"], m["clock"]["rate"]), (24, "2/3"))
        self.assertEqual((m["z_exit100"]["received"]["period"], m["z_exit100"]["f_received_over_f_emitted"]), (24, "2/3"))


if __name__ == "__main__":
    unittest.main()
