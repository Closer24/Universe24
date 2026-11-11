"""End-to-end evidence integrity for the single generic execution path."""
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from universe24.core import State, Tensor
from universe24.system.bundle import create_bundle, save_bundle
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run


def fixture(huge=False, bits=100):
    tensor = Tensor(["local", "neighbor"], [
        ("local", 3, [("local", (0, 0, 0), "b")]),
        ("neighbor", 3, [("local", (1, 0, 0), "a")]),
    ], strict_support=True)
    a = [[(n % 5) - 2 for n in range(27)] for _ in range(2)]
    b = [[(n % 7) - 3 for n in range(27)] for _ in range(2)]
    if huge:
        b[0][0] = 2 ** bits
    seed = State(3, a, b, [[n % 6 for n in range(27)] for _ in range(2)])
    channels = [dict(index=i, name=name, owner="mechanical-fixture", purpose="test-only state",
                     label="official") for i, name in enumerate(tensor.names)]
    return create_bundle(tensor, seed, channels=channels, protocol=default_protocol(),
                         model={"id": "test-only", "version": "1", "domain": "mechanical test"})


def replace_records(path, records):
    with gzip.open(path, "wt", encoding="utf-8") as stream:
        for item in records:
            stream.write(json.dumps(item) + "\n")


def read_records(path):
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream]


def refresh_file_hash(run, name):
    path = run / "validation.json"
    report = json.loads(path.read_text())
    report["files"][name] = hashlib.sha256((run / name).read_bytes()).hexdigest()
    path.write_text(json.dumps(report))


class SystemRuntimeTests(unittest.TestCase):
    def test_integer_transport_beyond_python_decimal_digit_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "run"
            report = run_bundle(fixture(huge=True, bits=20000), run, 2)
            self.assertEqual(report, verify_run(run))
            self.assertGreaterEqual(max(report["maximum_integer_bits_by_step"]), 20001)

    def test_complete_saved_run_replays_bigints_and_remainders(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "run"
            report = run_bundle(fixture(huge=True), run, 5)
            self.assertEqual(report, verify_run(run))
            self.assertEqual(report["channels_per_node"], 2)
            self.assertGreaterEqual(max(report["maximum_integer_bits_by_step"]), 101)
            self.assertGreater(report["click_count"], 0)
            self.assertTrue(all(value == "passed" for value in report["checks"].values()))
            self.assertTrue(all(report["acceptance_gates"][key]["status"] == "not_tested"
                                for key in "CDEF"))

    def test_zero_step_and_saved_bundle_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            save_bundle(fixture(), source)
            report = run_bundle(source, Path(tmp) / "run", 0)
            self.assertEqual(report["steps"], 0)
            self.assertEqual(report["click_count"], 0)

    def test_runs_are_byte_deterministic_and_never_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            first, second = Path(tmp) / "a", Path(tmp) / "b"
            self.assertEqual(run_bundle(fixture(), first, 2), run_bundle(fixture(), second, 2))
            for name in ("full_trace.jsonl.gz", "clicks.jsonl.gz", "validation.json"):
                self.assertEqual((first / name).read_bytes(), (second / name).read_bytes())
            with self.assertRaises(ValueError):
                run_bundle(fixture(), first, 2)

    def test_bad_steps_rejected_before_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            for steps in (-1, True, 1.5):
                run = Path(tmp) / str(steps)
                with self.assertRaises(ValueError):
                    run_bundle(fixture(), run, steps)
                self.assertFalse(run.exists())

    def test_modified_trace_rejected_even_with_recomputed_file_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "run"
            run_bundle(fixture(), run, 2)
            records = read_records(run / "full_trace.jsonl.gz")
            records[0]["after"]["r"][0][0] = (records[0]["after"]["r"][0][0] + 1) % 6
            replace_records(run / "full_trace.jsonl.gz", records)
            refresh_file_hash(run, "full_trace.jsonl.gz")
            with self.assertRaisesRegex(ValueError, "trace mismatch"):
                verify_run(run)

    def test_missing_duplicate_and_reordered_trace_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            for mode in ("missing", "duplicate", "reordered"):
                with self.subTest(mode=mode):
                    run = Path(tmp) / mode
                    run_bundle(fixture(), run, 3)
                    records = read_records(run / "full_trace.jsonl.gz")
                    if mode == "missing":
                        records.pop()
                    elif mode == "duplicate":
                        records.append(records[-1])
                    else:
                        records[0], records[1] = records[1], records[0]
                    replace_records(run / "full_trace.jsonl.gz", records)
                    refresh_file_hash(run, "full_trace.jsonl.gz")
                    with self.assertRaises(ValueError):
                        verify_run(run)

    def test_missing_extra_and_changed_clicks_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            for mode in ("missing", "extra", "changed"):
                with self.subTest(mode=mode):
                    run = Path(tmp) / mode
                    run_bundle(fixture(), run, 2)
                    records = read_records(run / "clicks.jsonl.gz")
                    if mode == "missing":
                        records.pop()
                    elif mode == "extra":
                        records.append(records[-1])
                    else:
                        records[0]["quotient"] += 1
                    replace_records(run / "clicks.jsonl.gz", records)
                    refresh_file_hash(run, "clicks.jsonl.gz")
                    with self.assertRaises(ValueError):
                        verify_run(run)

    def test_forged_physics_success_and_wrong_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            for field in ("physics", "source"):
                run = Path(tmp) / field
                run_bundle(fixture(), run, 1)
                path = run / "validation.json"
                report = json.loads(path.read_text())
                if field == "physics":
                    report["acceptance_gates"]["C"]["status"] = "passed"
                else:
                    report["source_hashes"]["core/engine.py"] = "0" * 64
                path.write_text(json.dumps(report))
                with self.assertRaisesRegex(ValueError, "validation report"):
                    verify_run(run)


if __name__ == "__main__":
    unittest.main()
