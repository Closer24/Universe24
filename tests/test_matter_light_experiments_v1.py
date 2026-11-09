"""Curated matter/light experiments: manifests, data hashes, cards, decoder pin, compositions, two short decoded runs."""
import hashlib
import json
from pathlib import Path
import unittest

from universe24.experiments import from_dict
from research.matter_light_experiments_v1 import verify as X

HEADINGS = ("## On the event board", "## In the clicks", "## Claim")


class Manifests(unittest.TestCase):
    def test_every_experiment_is_complete_and_hash_locked(self):
        ids = X.experiment_ids()
        self.assertGreaterEqual(len(ids), 5)
        frozen = json.loads((X.ROOT / "research/click_decoder_v1/FROZEN.json").read_text(encoding="utf-8"))
        for eid in ids:
            with self.subTest(experiment=eid):
                man = X.manifest(eid)
                folder = X.HERE / eid
                card = (folder / man["card"]).read_text(encoding="utf-8").splitlines()
                self.assertLessEqual(len(card), 40)
                for heading in HEADINGS:
                    self.assertTrue(any(line.startswith(heading) for line in card), heading)
                self.assertEqual(man["decoder"]["code_sha256"], frozen["code_sha256"])
                self.assertIn("result", man["verdict"])
                total = sum(p.stat().st_size for p in folder.rglob("*") if p.is_file())
                self.assertLessEqual(total, 1_000_000)
                for run in man["runs"]:
                    if "init" in run:
                        blob = (folder / run["init"]).read_bytes()
                        self.assertEqual(hashlib.sha256(blob).hexdigest(), run["init_sha256"])
                        self.assertEqual(from_dict(json.loads(blob)).steps, run["steps"])
                    if "block" in run:
                        path = X.ROOT / run["block_file"]
                        if run.get("pending_append") and not path.exists():
                            continue        # appended to the published blocks at push time; checked once present
                        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), run["block_file_sha256"])
                for check in man["checks"]:
                    self.assertTrue(check.get("not_decodable") or check["op"] in X.OPS, check["claim"])

    def test_compositions_regenerate_their_runs(self):
        for eid in X.experiment_ids():
            man = X.manifest(eid)
            if not man.get("composition"):
                continue
            build = X._composition(eid, man)
            for run in man["runs"]:
                if "from_composition" in run:
                    with self.subTest(run=run["name"]):
                        engine, initial, steps, notes = X.load_run(eid, man, run, build)
                        self.assertEqual(X.state_sha256(initial), run["initial_state_sha256"])


class DerivedQuantities(unittest.TestCase):
    """The two derived quantities are pure functions of decoder outputs (synthetic counts, exact expectations)."""

    def test_alpha_from_counts(self):
        self.assertEqual(X.alpha_from_counts(8, 4, 4, 0)["alpha"], 0.0)      # exclusive
        self.assertEqual(X.alpha_from_counts(8, 4, 4, 4)["alpha"], 2.0)      # both or none
        self.assertEqual(X.alpha_from_counts(64, 32, 32, 16)["alpha"], 1.0)  # independent
        self.assertIsNone(X.alpha_from_counts(4, 0, 2, 0)["alpha"])
        with self.assertRaises(ValueError):
            X.alpha_from_counts(4, 1, 1, 2)

    def test_check_ops_on_a_synthetic_report(self):
        report = {"sources": [{"birth": {"t": 56}, "period": 20}, {"birth": {"t": 68}, "period": 20}],
                  "summary": {"periods": [20, 20]}}
        reports = {"r": report, "s": report}
        cases = (({"op": "diff", "pointers": ["/sources/0/birth/t", "/sources/1/birth/t"], "value": 12}, "pass"),
                 ({"op": "diff", "pointers": ["/sources/1/birth/t", "/sources/0/birth/t"], "value": 12}, "fail"),
                 ({"op": "eq", "pointer": "/summary/periods", "value": [20, 20]}, "pass"),
                 ({"op": "same", "pointers": ["/sources/0/period", "/sources/1/period"]}, "pass"),
                 ({"op": "len_eq", "pointer": "/sources", "value": 2}, "pass"),
                 ({"op": "eq", "pointer": "/missing", "value": 1}, "fail"))
        for spec, want in cases:
            check = {"claim": "t", "text": "t", "run": "r", **spec}
            self.assertEqual(X.evaluate(check, reports, None, None)[0].split(":")[0], want, spec)
        same_runs = {"claim": "t", "text": "t", "runs": ["r", "s"], "pointer": "/sources/0/birth/t", "op": "same"}
        self.assertEqual(X.evaluate(same_runs, reports, None, None)[0], "pass")

    def test_chsh_from_outcomes(self):
        from research.click_decoder_v1 import chsh
        pr_box = {"00": [(1, 1), (-1, -1)], "01": [(1, -1), (-1, 1)], "10": [(1, -1), (-1, 1)], "11": [(1, -1), (-1, 1)]}
        out = X.chsh_from_outcomes(pr_box, chsh)
        self.assertEqual(out["E"], {"00": 1.0, "01": -1.0, "10": -1.0, "11": -1.0})
        self.assertEqual(out["S"], 4.0)
        self.assertEqual(out["marginals_all"], [0.5])
        local = {"00": [(1, 1), (-1, -1)], "01": [(1, 1), (-1, -1)], "10": [(-1, 1), (1, -1)], "11": [(-1, 1), (1, -1)]}
        self.assertEqual(X.chsh_from_outcomes(local, chsh)["S"], 2.0)
        self.assertEqual(sorted(abs(f) for f in X.chsh_from_outcomes(local, chsh)["forms"]), [2.0, 2.0, 2.0, 2.0])


def _table(fn, N=4):
    return {f"{i},{j}": fn(i, j) for i in range(N) for j in range(N)}


class DerivedCorrelationFunctions(unittest.TestCase):
    """r12's pure derive functions (proposal research/matter_light_v1/r12/verifier_proposal, applied by r01b)."""

    def test_e_table_and_marginals(self):
        out = X.e_table({"0,0": [(1, 1), (-1, -1)], "0,1": [(1, -1), (1, 1)]})
        self.assertEqual(out["E"], {"0,0": 1.0, "0,1": 0.0})
        self.assertEqual(out["marginals_all"], [0.5, 1.0])

    def test_covariant_curve_and_best_chsh(self):
        import math
        E = _table(lambda a, b: float(round(math.cos(math.pi * (a - b) / 2))))
        c = X.covariant_curve(E, 4)
        self.assertTrue(c["covariant"])
        self.assertEqual(c["E_of_delta"], [1.0, 0.0, -1.0, 0.0])
        self.assertAlmostEqual(c["fourier_l1"], 1.0, places=12)
        self.assertEqual(c["P_same_of_delta"], [1.0, 0.5, 0.0, 0.5])
        b = X.best_chsh(E, 4)
        self.assertAlmostEqual(b["S_max"], 2.0, places=12)
        Eq = _table(lambda a, b: math.cos(math.pi * (a - b) / 2 - math.pi / 4))
        self.assertAlmostEqual(X.best_chsh(Eq, 4)["S_max"], 2 * math.sqrt(2), places=12)
        Epr = _table(lambda a, b: 1.0 if (a - b) % 4 in (0, 1) else -1.0)
        self.assertAlmostEqual(X.best_chsh(Epr, 4)["S_max"], 4.0, places=12)
        self.assertAlmostEqual(X.covariant_curve(Epr, 4)["fourier_l1"], math.sqrt(2), places=12)

    def test_tlm(self):
        import math
        self.assertAlmostEqual(X.tlm(1, 1, 1, -1)["TLM"], 2 * math.pi, places=12)
        self.assertFalse(X.tlm(1, 1, 1, -1)["quantum_consistent"])
        r = 1 / math.sqrt(2)
        self.assertAlmostEqual(X.tlm(r, r, r, -r)["TLM"], math.pi, places=12)
        self.assertAlmostEqual(X.tlm(1, 1, 1, 1)["TLM"], math.pi, places=12)

    def test_plane_spectrum(self):
        s = X.plane_spectrum([0, 6912, 6912, 0, 6912, 6912])
        self.assertEqual(s["period"], 3)
        self.assertEqual(s["dark_planes"], [0, 3])
        self.assertAlmostEqual(s["fourier_abs"][1], 0.0, places=9)
        self.assertGreater(s["fourier_abs"][2], 0.0)
        self.assertEqual(X.plane_spectrum([6912] * 6)["period"], 1)


class ShortDecodedRuns(unittest.TestCase):
    def test_fast_runs_replay_and_their_checks_pass(self):
        for eid in ("E02_clicktime_chsh",):
            with self.subTest(experiment=eid):
                out = X.verify(eid, fast=True)
                self.assertTrue(out["ok"], out)
                self.assertEqual(out["decoder"], "frozen")
                evaluated = [c for c in out["checks"] if c["result"] in ("pass", "fail")]
                self.assertTrue(evaluated)
                self.assertTrue(all(c["result"] == "pass" for c in evaluated), out["checks"])


if __name__ == "__main__":
    unittest.main()
