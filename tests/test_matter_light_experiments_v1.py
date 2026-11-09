"""Curated matter/light experiments: manifests, data hashes, cards, decoder pin, compositions, two short decoded runs."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from universe24.experiments import from_dict
from research.matter_light_experiments_v1 import verify as X

HEADINGS = ("## On the event board", "## In the clicks", "## Claim")
SHORT_REWIND = 16           # longer exact-rewind preparations are left to verify (unit tests stay under 10 s)


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
                self.assertTrue(any(line.startswith("- referee:") for line in card), "referee line")
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
                    if "layer" in check and not check.get("not_decodable"):   # a listed layer and call, pinned
                        self.assertIn(check.get("call"), X.LAYERS.get(check["layer"], {}), check["claim"])
                        self.assertIn(check["layer"], man.get("layers", {}), check["claim"])
                for name, pin in man.get("layers", {}).items():
                    record = X.ROOT / f"research/click_decoder_v1/FROZEN_{name}.json"
                    self.assertEqual(pin, json.loads(record.read_text(encoding="utf-8"))["sha256"], name)

    def test_compositions_regenerate_their_runs(self):
        """For every experiment made from compositions, its first composition run (in manifest order, normally the
        main run) regenerates its recorded initial state with the current registry.  ``verify`` regenerates every run,
        and the registry's own tests pin its generators; one board per experiment keeps this file under 10 s as
        experiments are added.  A run prepared by more than SHORT_REWIND exact rewinds is only composed here; its
        rewind and initial-state hash are checked by ``verify`` (about 10 s per 240 rewinds on a 640-site board)."""
        for eid in X.experiment_ids():
            man = X.manifest(eid)
            if not X._uses_composition(man):                 # composition.json or the declared compositions
                continue
            build = X._composition(eid, man)
            run = next((r for r in man["runs"] if r.get("from_composition") is not None), None)
            if run is None:
                continue
            fc = run["from_composition"]
            with self.subTest(experiment=eid, run=run["name"]):
                if fc.get("rewind", 0) > SHORT_REWIND:
                    self.assertIsNotNone(build(fc.get("control"), fc.get("composition")))
                    continue
                engine, initial, steps, notes = X.load_run(eid, man, run, build)
                self.assertEqual(X.state_sha256(initial), run["initial_state_sha256"])


class CompositionRuns(unittest.TestCase):
    """Runs made from compositions: declared keys and files inside the folder only, a recorded initial-state hash, and
    an optional exact rewind before t = 0."""

    def _with_composition(self):
        for eid in X.experiment_ids():
            man = X.manifest(eid)
            if man.get("composition"):
                return eid, man
        self.skipTest("no experiment with a composition.json")

    def test_refusals(self):
        eid, man = self._with_composition()
        build = X._composition(eid, {"composition": man["composition"], "runs": [],
                                     "compositions": {"up": "../README.md", "abs": "/etc/hostname"}})
        for key in ("up", "abs", "undeclared"):
            with self.assertRaises(ValueError):
                build(None, key)
        with self.assertRaises(ValueError):
            build("no such control")
        with self.assertRaises(ValueError):
            X._composition(eid, {"composition": None, "runs": []})()
        run = {"name": "r", "steps": 1, "from_composition": {"control": None}}
        with self.assertRaises(ValueError):              # a composition-only run must record its initial-state hash
            X.load_run(eid, man, run, X._composition(eid, man))

    def test_rewind_preparation(self):
        eid, man = self._with_composition()
        build = X._composition(eid, man)
        board = build()
        earlier = X.rewind_preparation(board.engine, board.initial, 3)
        state = earlier
        for _ in range(3):
            state = board.engine.advance(state)
        self.assertEqual(state, board.initial)
        run = {"name": "r", "steps": 1, "from_composition": {"control": None, "rewind": 3},
               "initial_state_sha256": X.state_sha256(earlier)}
        self.assertEqual(X.load_run(eid, man, run, build)[1], earlier)
        with self.assertRaises(ValueError):
            X.load_run(eid, man, dict(run, initial_state_sha256="0" * 64), build)
        for k in (-1, 1.5, True):
            with self.assertRaises(ValueError):
                X.rewind_preparation(board.engine, board.initial, k)


class CommandLine(unittest.TestCase):
    """argparse: an unknown or abbreviated flag stops with exit status 2 and a usage line, --help prints the usage,
    and an unknown experiment stops with one line; none of them replays a run."""

    def _stop(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), self.assertRaises(SystemExit) as stop:
            X.main(argv)
        return stop.exception.code, out.getvalue(), err.getvalue()

    def test_usage_errors_exit_2_and_help(self):
        usage = "usage: python -m research.matter_light_experiments_v1.verify"
        for argv in (["--bogus"], ["--quik"], ["--fas"], ["E03_exclusive_detection", "--keep"]):
            code, out, err = self._stop(argv)
            self.assertEqual((code, out), (2, ""), argv)
            self.assertIn(usage, err)
        code, out, err = self._stop(["--help"])
        self.assertEqual(code, 0)
        self.assertIn(usage, out)
        for flag in ("--all", "--fast", "--keep DIR"):
            self.assertIn(flag, out)
        code, out, err = self._stop(["E99_no_such_experiment"])
        self.assertEqual(code, "unknown experiment(s): ['E99_no_such_experiment']")


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


class DecoderLayers(unittest.TestCase):
    """Released decoder layers: a closed list, each pinned by its FROZEN file and by the manifest; a call reads the
    official logs of the check's runs first, its arguments are literal or detectors.json values and never write."""

    def _released(self, name):
        from research.click_decoder_v1 import decoder as dmod
        frozen = dmod.HERE / f"FROZEN_{name}.json"
        if not frozen.exists():
            self.skipTest(f"{name} is not released")
        record = json.loads(frozen.read_text(encoding="utf-8"))
        self.assertEqual(record["name"], name)
        self.assertTrue((dmod.HERE / record["file"]).exists(), record["file"])
        return record["sha256"]

    @staticmethod
    def _log(folder, name, records):              # the official record form (compact JSON)
        path = Path(folder) / name
        path.write_text("".join(json.dumps({"step": t, "address": [x, y, z, g], "kind": k, "quotient": q},
                                           separators=(",", ":")) + "\n" for t, x, y, z, g, k, q in records),
                        encoding="utf-8")
        return path

    def _results(self, checks, logs, names, detectors=None, pins=None):
        layers = {c["layer"] for c in checks}
        man = {"layers": pins or {n: self._released(n) for n in layers if n in X.LAYERS}}
        lstat = {n: X.layer_status(man, n) for n in layers}
        values = X.layer_values(checks, lstat, logs, detectors)
        return [X.layer_result(c, lstat, values, names, detectors) for c in checks]

    def test_status_closed_list_and_pins(self):
        for name, calls in X.LAYERS.items():                # every listed layer is released with every listed call
            with self.subTest(layer=name):
                status, mod = X.layer_status({"layers": {name: self._released(name)}}, name)
                self.assertEqual(status, "frozen")
                self.assertTrue(all(callable(getattr(mod, call, None)) for call in calls), calls)
        sha = self._released("log_symmetry_v1")
        self.assertTrue(X.layer_status({"layers": {"log_symmetry_v1": "0" * 64}}, "log_symmetry_v1")[0]
                        .startswith("decoder layer changed"))
        self.assertTrue(X.layer_status({}, "log_symmetry_v1")[0].startswith("decoder layer pending"))
        self.assertTrue(X.layer_status({"layers": {"other": sha}}, "other")[0].startswith("decoder layer pending"))

    def test_arguments_and_call_shapes(self):
        self.assertEqual(X.layer_args({"tau": 2, "lo": None}, None), {"tau": 2, "lo": None})
        self.assertEqual(X.layer_args({"declaration": {"detectors": "/d/x"}}, {"d": {"x": [1, 2]}}),
                         {"declaration": [1, 2]})
        with self.assertRaises(ValueError):
            X.layer_args({"write_prefix": "out"}, None)
        with self.assertRaises(KeyError):
            X.layer_args({"declaration": {"detectors": "/missing"}}, {"d": 1})
        mirror, diff = {"layer": "log_symmetry_v1", "call": "mirror"}, {"layer": "log_symmetry_v1", "call": "record_diff"}
        self.assertEqual(X.layer_calls({**mirror, "run": "a"}), [("a",)])
        self.assertEqual(X.layer_calls({**mirror, "runs": ["a", "b"]}), [("a",), ("b",)])
        self.assertEqual(X.layer_calls({**diff, "runs": ["a", "b"]}), [("a", "b")])
        for bad in ({**mirror, "run": "a", "runs": ["b"]}, {**diff, "run": "a"}, {**diff, "runs": ["a"]},
                    {**diff, "runs": ["a", "b", "c"]}, {**mirror}):
            self.assertIsNone(X.layer_calls(bad), bad)

    def test_log_symmetry_checks(self):
        records = [(1, 0, 0, 0, 0, 1, 1), (4, 0, 0, 0, 0, 2, -1), (2, 1, 0, 0, 3, 1, 2), (3, 1, 0, 0, 3, 2, -2)]
        base = {"claim": "t", "text": "t", "layer": "log_symmetry_v1"}
        checks = [  # a is mirrored about tau = 2 (t -> 5 - t, k -> -k mod 3, q -> -q); b lacks one record
            {**base, "run": "a", "call": "mirror", "args": {"tau": 2}, "pointer": "/unpaired", "op": "eq", "value": 0},
            {**base, "runs": ["a", "b"], "call": "mirror", "args": {"tau": 2}, "pointer": "/unpaired", "op": "eq",
             "value": [0, 1]},
            {**base, "run": "b", "call": "mirror", "args": {"tau": 2}, "pointer": "/unpaired_per_update/2",
             "op": "eq", "value": 1},                                     # the JSON form: integer keys as strings
            {**base, "runs": ["a", "b"], "call": "record_diff", "pointers": ["/only_a", "/only_b"], "op": "eq",
             "value": [1, 0]},
            {**base, "runs": ["a", "b"], "call": "best_tau", "pointer": "/tau", "op": "same"},
            {**base, "run": "a", "call": "record_diff", "pointer": "/differ", "op": "eq", "value": 0},
            {**base, "run": "a", "call": "split", "pointer": "/0", "op": "len_eq", "value": 1},
            {**base, "run": "a", "call": "period", "args": {"P": 2, "write_prefix": "x"}, "pointer": "/cycles",
             "op": "ge", "value": 0},
            {**base, "run": "c", "call": "mirror", "args": {"tau": 2}, "pointer": "/unpaired", "op": "eq", "value": 0},
            {**base, "run": "d", "call": "mirror", "args": {"tau": 2}, "pointer": "/unpaired", "op": "eq", "value": 0},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            logs = {"a": self._log(tmp, "a.jsonl", records), "b": self._log(tmp, "b.jsonl", records[:3])}
            got = [r for r, _ in self._results(checks, logs, {"a", "b", "d"})]
            changed = self._results(checks[:1], logs, {"a"}, pins={"log_symmetry_v1": "0" * 64})[0][0]
        self.assertEqual(got[:5], ["pass"] * 5)
        self.assertTrue(got[5].startswith("not decodable: record_diff reads 2 logs"), got[5])
        self.assertTrue(got[6].startswith("not decodable: log_symmetry_v1 has no call"), got[6])
        self.assertTrue(got[7].startswith("fail: layer call failed (ValueError"), got[7])
        self.assertEqual(got[8], "skipped (runs not selected)")
        self.assertEqual(got[9], "fail: run did not replay")
        self.assertEqual(changed, "decoder layer changed: re-validate")

    def test_beat_clock_run_declared(self):
        import math
        L, steps, c, m = 32, 120, 1 / math.sqrt(3), 0.07
        k1, k2 = 2 * math.pi / L, 4 * math.pi / L
        w = [math.sqrt(m * m + c * c * k * k) for k in (k1, k2)]
        records = [(t, 0, 0, z, 0, 0, q) for t in range(1, steps + 1) for z in range(L)
                   for q in [round(sum(10 ** 6 * math.cos(k * z - wk * t) for k, wk in ((k1, w[0]), (k2, w[1]))))] if q]
        declaration = {"side": L, "steps": steps, "channel": 0, "sites": [[0, 0, z] for z in range(L)],
                       "clocks": [{"name": "pair", "K1": [0, 0, k1], "K2": [0, 0, k2], "axis": [0, 0, 1], "c": c}]}
        check = {"claim": "t", "text": "t", "run": "r", "layer": "beat_clock_v1", "call": "run_declared",
                 "args": {"declaration": {"detectors": "/decl"}}, "clock": "pair", "pointer": "/clocks/0/ratio"}
        with tempfile.TemporaryDirectory() as tmp:          # an exactly relativistic pair: ratio 1
            logs = {"r": self._log(tmp, "r.jsonl", records)}
            got = self._results([{**check, "op": "approx", "value": 1.0, "tol": 1e-6},
                                 {**check, "op": "not_approx", "value": 1.0, "tol": 1e-6}], logs, {"r"},
                                {"decl": declaration})
        self.assertEqual([r for r, _ in got], ["pass", "fail"])
        self.assertAlmostEqual(got[0][1], 1.0, places=6)


class ProjectionLayers(unittest.TestCase):
    """A run decoded on a declared projection of its official log (r18b): the declaration is checked, the projection
    keeps the records verbatim, and its hash is checked."""

    def test_declaration_is_checked(self):
        good = {"name": "r", "layer": {"name": "line_y0z0", "keep": {"y": 0, "z": 0}}, "layer_sha256": "0" * 64}
        self.assertEqual(X.projection(good, 8), good["layer"])
        self.assertIsNone(X.projection({"name": "r"}, 8))
        for layer in ({"name": "p", "keep": {}}, {"name": "p", "keep": {"w": 0}}, {"name": "p", "keep": {"xy": 0}},
                      {"name": "p", "keep": {"y": "0"}}, {"name": "p", "keep": {"y": True}},
                      {"name": "p", "keep": {"y": 8}}, {"name": "p", "keep": {"y": -1}}, {"name": "", "keep": {"y": 0}},
                      {"keep": {"y": 0}}, {"name": "p", "keep": {"y": 0}, "extra": 1}, "y0"):
            with self.assertRaises(ValueError, msg=layer):
                X.projection({**good, "layer": layer}, 8)
        with self.assertRaises(ValueError):
            X.projection({"name": "r", "layer": good["layer"]}, 8)            # no layer_sha256

    def test_projection_and_its_hash(self):
        from research import click_decoder_v1 as dec
        records = [(1, 0, 0, 0, 0, 1, 1), (1, 2, 0, 1, 5, 1, 2), (2, 3, 0, 0, 7, 2, -1), (3, 1, 2, 0, 0, 1, 1)]
        with tempfile.TemporaryDirectory() as tmp:
            log = DecoderLayers._log(tmp, "r.events.jsonl", records)
            lines = log.read_text(encoding="utf-8").splitlines(keepends=True)
            kept = "".join(lines[i] for i in (0, 2)).encode("utf-8")             # y = 0 and z = 0
            run = {"name": "r", "layer": {"name": "line_y0z0", "keep": {"y": 0, "z": 0}},
                   "layer_sha256": hashlib.sha256(kept).hexdigest()}
            report = X.decode_run(dec, log, 4, 3, run, None)
            self.assertEqual(Path(str(log) + ".layer.jsonl").read_bytes(), kept)
            self.assertEqual(report["input"]["layer"], "line_y0z0")
            self.assertEqual(report["input"]["log"]["events"], 2)
            Path(str(log) + ".layer.jsonl").unlink()
            with self.assertRaises(ValueError):
                X.decode_run(dec, log, 4, 3, {**run, "layer_sha256": "0" * 64}, None)


if __name__ == "__main__":
    unittest.main()
